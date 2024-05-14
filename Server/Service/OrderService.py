from ..Repository import OrderRepository, WorkshopRepository
from ..database import db, Order, OrderToDrone, Workshop, StatusOrder
from ..Models import OrderViewAdmin


class OrderService:
    def __init__(self):
        self.__repository: OrderRepository = OrderRepository(db.session)
        self.__repository_workshop: WorkshopRepository = WorkshopRepository(db.session)

    def get_list_order(self) -> list[OrderViewAdmin]:
        list_order_entity = self.__repository.get_list_order()
        orders = [OrderViewAdmin.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.drone_products])
            order.sum_price = sum_price
        return orders

    def get_list_order_by_state_order(self, state_order: str) -> list[OrderViewAdmin]:
        print(state_order)
        list_order_entity = self.__repository.get_list_order_by_state_order(state_order)
        orders = [OrderViewAdmin.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.drone_products])
            order.sum_price = sum_price
        return orders

    def get_order(self, uuid: str) -> OrderViewAdmin:
        order_entity = self.__repository.get_by_uuid(uuid)
        order = OrderViewAdmin.model_validate(order_entity, from_attributes=True)

        sum_price = sum([i.price * i.count for i in order.drone_products])
        order.sum_price = sum_price
        return order

    def get_order_by_id(self, id_order: int) -> Order:
        return self.__repository.get(id_order)

    def get_order_drone(self, id_order: int, id_sweet_product: int) -> OrderToDrone:
        return self.__repository.get_by_id_order_and_drone(id_order, id_sweet_product)

    def get_workshop_by_address(self, address: str) -> Workshop | None:
        return self.__repository_workshop.get_by_address(address)

    def delete_order_drone(self, id_order: int, id_drone: int):
        self.__repository.delete_by_id_order_and_drone(id_order, id_drone)

    def update_order_drone(self, id_order: int, id_drone: int, count: int):
        self.__repository.update_drone(id_order, id_drone, count)

    def update(self, uuid: str, address: str, state_order: object):
        order = self.__repository.get_by_uuid(uuid)
        order.address = address
        order.status_order = state_order

        self.__repository.update(order)

    def order_update_status(self, uuid: str) -> Order:
        order = self.__repository.get_by_uuid(uuid)
        if order.status_order == StatusOrder.confirmed:
            order.status_order = StatusOrder.prepared
        elif order.status_order == StatusOrder.prepared:
            order.status_order = StatusOrder.ready
        elif order.status_order == StatusOrder.ready:
            order.status_order = StatusOrder.waiting_for_the_courier

        self.__repository.update(order)
        return order

