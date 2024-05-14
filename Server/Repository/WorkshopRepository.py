from sqlalchemy.orm import Session
from ..database import Workshop

from uuid import uuid4


class WorkshopRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_list(self) -> list[Workshop] | None:
        return self.__session.query(Workshop).all()

    def get_by_uuid(self, uuid: str) -> Workshop | None:
        return self.__session.query(Workshop).filter(Workshop.trace_id == uuid).first()

    def get_by_address(self, address: str) -> Workshop | None:
        return self.__session.query(Workshop).where(Workshop.address == address).first()