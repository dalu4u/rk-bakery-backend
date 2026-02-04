from fastapi import APIRouter, HTTPException
from models import Product, ProductCreate
import os

router = APIRouter()


def get_db():
    """Get database connection"""
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]


@router.get("/products", response_model=list[Product])
async def get_products(category: str = None):
    """Get all products, optionally filtered by category"""
    try:
        db = get_db()
        query = {}
        if category and category.lower() != 'all':
            query['category'] = category
        
        products = await db.products.find(query).to_list(1000)
        return [Product(**product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a single product by ID"""
    try:
        db = get_db()
        product = await db.products.find_one({"id": product_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return Product(**product)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        db = get_db()
        product_obj = Product(**product.dict())
        await db.products.insert_one(product_obj.dict())
        return product_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")
