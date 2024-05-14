from pydantic import BaseModel


class Type(BaseModel):
    id: int
    name: str
    description: str | None


class Component(BaseModel):
    id: int
    name: str
    description: str


class BaseDrone(BaseModel):
    name: str
    price_drone: float
    weight_drone: int
    width: float
    length: float
    height: float
    description: str
    image: str
    instructions: str
    components: list[Component]


class GetDrone(BaseDrone):
    id: int
    trace_id: str
    type_id: int
    type: Type


class OrderToDrone(BaseModel):
    id_order: int | None = None
    id_drone: int | None = None
    drone: GetDrone
    price: float
    count: int = 0
