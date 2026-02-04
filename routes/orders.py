from fastapi import APIRouter, HTTPException
from models import Order, OrderCreate
import os

router = APIRouter()


def get_db():
    """Get database connection"""
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]


@router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Create a new order"""
    try:
        if not order_data.customer_name or not order_data.phone or not order_data.address:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        if not order_data.items or len(order_data.items) == 0:
            raise HTTPException(status_code=400, detail="Order must contain at least one item")
        
        order = Order(**order_data.dict())
        
        db = get_db()
        await db.orders.insert_one(order.dict())
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")


@router.get("/orders", response_model=list[Order])
async def get_orders(status: str = None):
    """Get all orders"""
    try:
        db = get_db()
        query = {}
        if status:
            query['status'] = status
        
        orders = await db.orders.find(query).sort("created_at", -1).to_list(1000)
        return [Order(**order) for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")
