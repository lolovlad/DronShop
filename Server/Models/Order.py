from pydantic import BaseModel, Extra
from ..database import TypeOrder, StatusOrder
from .Drone import OrderToDrone
from datetime import datetime


class BaseOrder(BaseModel):
    user_id: int
    type_order: TypeOrder = TypeOrder.in_hall
    status_order: StatusOrder = StatusOrder.waiting_for_confirmation
    address: str
    description: str = ""
    drone_products: list[OrderToDrone]


class GetOrder(BaseOrder):
    id: int
    trace_id: str
    datatime_order: datetime
    sum_price: float = 0


class OrderView(BaseModel, extra=Extra.forbid):
    id: int
    trace_id: str
    datatime_order: datetime
    sum_price: float = 0
    user_id: int
    type_order: TypeOrder = TypeOrder.in_hall
    status_order: StatusOrder = StatusOrder.waiting_for_confirmation
    address: str
    description: str = ""
    drone_products: object


class OrderViewAdmin(OrderView):
    user: object


state_order = {
    1: "Ждет оплаты",
    2: "Оплачено",
    3: "Ждет подтверждения",
    4: "Подтверждено",
    5: "Сборка",
    6: "Готово",
    7: "Ждет отгрузки",
    8: "Доставльяеться",
    9: "Завершен"
               }

type_order = {
    1: "Самовывоз со склада",
    2: "Доставка"
}
