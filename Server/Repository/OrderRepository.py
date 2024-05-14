from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import Order, OrderToDrone, StatusOrder
from ..Models import BaseOrder


class OrderRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add(self, order: BaseOrder) -> Order | None:
        try:
            order_entity = Order(
                user_id=order.user_id,
                type_order=order.type_order,
                status_order=order.status_order,
                address=order.address,
                description=order.description
            )

            self.__session.add(order_entity)
            self.__session.commit()

            order_to_drone_list = []

            for i in order.drone_products:
                order_to_drone_list.append(OrderToDrone(
                    id_order=order_entity.id,
                    id_drone=i.id_drone,
                    price=i.price,
                    count=i.count
                ))
            self.__session.add_all(order_to_drone_list)
            self.__session.commit()
            return order_entity
        except:
            self.__session.rollback()
            return None

    def get_list_order_by_user_id(self, id_user: int) -> list[Order] | None:
        return self.__session.query(Order).filter(Order.user_id == id_user).order_by(Order.datatime_order).all()

    def get_list_order(self) -> list[Order] | None:
        return self.__session.query(Order).order_by(Order.datatime_order).all()

    def get_list_order_by_state_order(self, state_order: str) -> list[Order] | None:

        return self.__session.query(Order).where(Order.status_order == state_order).order_by(Order.datatime_order).all()

    def get_by_uuid(self, uuid: str) -> Order | None:
        return self.__session.query(Order).filter(Order.trace_id == uuid).first()

    def delete_by_id_order_and_drone(self, id_order: int, id_drone: int):
        order_entity = self.__session.query(OrderToDrone).where(OrderToDrone.id_order == id_order)\
            .where(OrderToDrone.id_drone == id_drone).first()
        try:
            self.__session.delete(order_entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get(self, id: int) -> Order | None:
        return self.__session.get(Order, id)

    def get_by_id_order_and_drone(self, id_order: int, id_drone: int) -> OrderToDrone | None:
        return self.__session.query(OrderToDrone).\
            where(OrderToDrone.id_order == id_order).\
            where(OrderToDrone.id_drone == id_drone).first()

    def update_drone(self, id_order: int, id_drone: int, count: int):
        order_drone = self.get_by_id_order_and_drone(id_order, id_drone)
        order_drone.count = count
        self.__session.commit()

    def update(self, order: Order):
        try:
            self.__session.add(order)
            self.__session.commit()
        except:
            self.__session.rollback()