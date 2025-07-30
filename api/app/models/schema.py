from pydantic import BaseModel
from typing import List, Optional

class Supplier(BaseModel):
    name: str
    failure_rate: float

class Product(BaseModel):
    name: str

class Location(BaseModel):
    name: str

class Warehouse(BaseModel):
    name: str

class Shipment(BaseModel):
    id: str
    origin: str
    destination: str
    product: str
    quantity: int

class Query(BaseModel):
    query: str
