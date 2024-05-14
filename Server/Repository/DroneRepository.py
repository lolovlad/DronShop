from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import Drone, Type


class DroneRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def count_row(self) -> int:
        response = select(func.count(Drone.id))
        result = self.__session.execute(response)
        return result.scalars().first()

    def get_page_drone(self, start: int, limit: int) -> list[Drone]:
        drone = self.__session.query(Drone).offset(start).fetch(limit).order_by(Drone.id).all()
        return drone

    def get_drone(self) -> list[Drone]:
        drone = self.__session.query(Drone).order_by(Drone.id).all()
        return drone

    def get_by_uuid(self, uuid: str) -> Drone | None:
        drone = self.__session.query(Drone).filter(Drone.trace_id == uuid).first()
        return drone

    def get_list_tag(self) -> list[Type] | None:
        return self.__session.query(Type).all()

    def get_drone_by_tag(self, tag: int) -> list[Drone]:
        drone = self.__session.query(Drone).where(Drone.type_id == tag).order_by(Drone.id).all()
        return drone
