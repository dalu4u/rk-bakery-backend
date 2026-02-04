from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: str
    description: str
    price: int
    image: str
    features: List[str]
    inStock: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProductCreate(BaseModel):
    name: str
    category: str
    description: str
    price: int
    image: str
    features: List[str]
    inStock: bool = True


class OrderItem(BaseModel):
    id: str
    name: str
    price: int
    quantity: int
    image: str


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    phone: str
    email: Optional[str] = None
    address: str
    delivery_option: str
    delivery_charge: int
    special_instructions: Optional[str] = None
    items: List[OrderItem]
    subtotal: int
    total: int
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    email: Optional[str] = None
    address: str
    delivery_option: str
    delivery_charge: int
    special_instructions: Optional[str] = None
    items: List[OrderItem]
    subtotal: int
    total: int
