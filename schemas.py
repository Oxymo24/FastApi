from pydantic import BaseModel
from typing import List

class SizeQuantity(BaseModel):
    sizes: str
    quantity: int

class ProductRequest(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]

class ProductResponse(BaseModel):
    id: str
    
class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderRequest(BaseModel):
    userId: str
    items: List[OrderItem]


class OrderResponse(BaseModel):
    id: str