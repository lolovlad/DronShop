from ..Repository import DroneRepository, WorkshopRepository, OrderRepository
from ..database import db, Workshop, TypeOrder, Order, Type
from ..Models import GetDrone, OrderToDrone, BaseOrder, GetOrder, OrderView


class ShopService:
    def __init__(self):
        self.__drone_repository: DroneRepository = DroneRepository(db.session)
        self.__workshop_repository: WorkshopRepository = WorkshopRepository(db.session)
        self.__order_repository: OrderRepository = OrderRepository(db.session)
        self.__count_drone: int = 20
        self.__count_row: int = self.__drone_repository.count_row()

    def get_drone_page(self, page: int):
        pass

    def get_list_workshop(self) -> list[Workshop]:
        return self.__workshop_repository.get_list()

    def get_address_by_workshop_uuid(self, uuid: str) -> str:
        return self.__workshop_repository.get_by_uuid(uuid).address

    def get_list_tag(self) -> list[Type]:
        return self.__drone_repository.get_list_tag()

    def get_drone_by_tag(self, tag: int):
        drone_entity = self.__drone_repository.get_drone_by_tag(tag)
        drone = [GetDrone.model_validate(i, from_attributes=True) for i in drone_entity]
        for i in drone:
            name, ext = i.image.split(".")
            i.image = f"{name}_thumb.{ext}"
        return drone

    def get_drone(self) -> list[GetDrone]:
        drone_entity = self.__drone_repository.get_drone()
        drone = [GetDrone.model_validate(i, from_attributes=True) for i in drone_entity]
        for i in drone:
            name, ext = i.image.split(".")
            i.image = f"{name}_thumb.{ext}"
        return drone

    def get_product(self, uuid: str) -> GetDrone | None:
        drone_entity = self.__drone_repository.get_by_uuid(uuid)
        try:
            drone_product = GetDrone.model_validate(drone_entity, from_attributes=True)
        except:
            drone_product = None

        return drone_product

    def get_list_product_by_uuid(self, uuids: list[str], counts: dict) -> list[OrderToDrone]:
        list_drones = []
        for uuid in uuids:
            list_drones.append(self.__drone_repository.get_by_uuid(uuid))
        return [OrderToDrone(
            id_drone=drone.id,
            drone=GetDrone.model_validate(drone, from_attributes=True),
            price=drone.price_drone,
            count=counts[drone.trace_id]
        ) for drone in list_drones]

    def create_order(self, type_order: TypeOrder, address: str, description: str, cart: dict, user_id: int) -> Order:
        list_order_to_drone = self.get_list_product_by_uuid(list(cart.keys()), cart)
        order = BaseOrder(
            user_id=user_id,
            type_order=type_order,
            address=address,
            description=description,
            drone_products=list_order_to_drone
        )
        order = self.__order_repository.add(order)
        return order

    def get_list_order_by_user_id(self, id_user: int) -> list[OrderView]:
        list_order_entity = self.__order_repository.get_list_order_by_user_id(id_user)
        orders = [OrderView.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.drone_products])
            order.sum_price = sum_price

        return orders

    def get_order_by_uuid(self, uuid: str) -> Order:
        return self.__order_repository.get_by_uuid(uuid)
