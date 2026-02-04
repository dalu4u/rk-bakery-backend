"""
Seed script to populate the database with initial products
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

products = [
    {
        "id": "1",
        "name": "Ragi Chocolate Cake",
        "category": "Finger Millet Cakes",
        "description": "Rich chocolate cake made with 100% finger millet flour, naturally sweetened with jaggery",
        "price": 450,
        "image": "https://images.pexels.com/photos/35799899/pexels-photo-35799899.jpeg",
        "features": ["Zero Maida", "Finger Millet", "Jaggery Sweetened"],
        "inStock": True
    },
    {
        "id": "2",
        "name": "Millet Vanilla Sponge",
        "category": "Millet Cakes",
        "description": "Light and fluffy vanilla sponge cake made with pearl millet flour and zero refined sugar",
        "price": 400,
        "image": "https://images.pexels.com/photos/11461397/pexels-photo-11461397.jpeg",
        "features": ["Pearl Millet", "Sugar Free", "Whole Grain"],
        "inStock": True
    },
    {
        "id": "3",
        "name": "Jaggery Cookies",
        "category": "Cookies",
        "description": "Crunchy wheat cookies sweetened naturally with organic jaggery",
        "price": 200,
        "image": "https://images.pexels.com/photos/18772824/pexels-photo-18772824.jpeg",
        "features": ["Whole Wheat", "Jaggery Sweetened", "No Preservatives"],
        "inStock": True
    },
    {
        "id": "4",
        "name": "Sugar-Free Almond Cookies",
        "category": "Cookies",
        "description": "Delicious almond cookies with zero added sugar, perfect for guilt-free indulgence",
        "price": 250,
        "image": "https://images.pexels.com/photos/1374586/pexels-photo-1374586.jpeg",
        "features": ["Zero Sugar", "Almond Rich", "Diabetic Friendly"],
        "inStock": True
    },
    {
        "id": "5",
        "name": "Ragi Brownies",
        "category": "Brownies",
        "description": "Fudgy brownies made with finger millet and dark chocolate, naturally sweetened",
        "price": 300,
        "image": "https://images.pexels.com/photos/34444367/pexels-photo-34444367.jpeg",
        "features": ["Finger Millet", "Dark Chocolate", "Jaggery Sweetened"],
        "inStock": True
    },
    {
        "id": "6",
        "name": "Millet Bread Loaf",
        "category": "Bread",
        "description": "Artisan whole grain bread made with mixed millets, perfect for daily nutrition",
        "price": 150,
        "image": "https://images.pexels.com/photos/30853707/pexels-photo-30853707.jpeg",
        "features": ["Multi Millet", "Zero Maida", "High Fiber"],
        "inStock": True
    },
    {
        "id": "7",
        "name": "Banana Walnut Millet Cake",
        "category": "Millet Cakes",
        "description": "Moist banana cake with walnuts, made with finger millet and natural sweeteners",
        "price": 480,
        "image": "https://images.pexels.com/photos/35799876/pexels-photo-35799876.jpeg",
        "features": ["Finger Millet", "No Refined Sugar", "Rich in Omega-3"],
        "inStock": True
    },
    {
        "id": "8",
        "name": "Whole Wheat Cupcakes",
        "category": "Cupcakes",
        "description": "Delightful cupcakes made with 100% whole wheat flour and jaggery frosting",
        "price": 280,
        "image": "https://images.pexels.com/photos/30176148/pexels-photo-30176148.jpeg",
        "features": ["Whole Wheat", "Jaggery Frosting", "No Artificial Colors"],
        "inStock": True
    }
]


async def seed_products():
    """Seed the database with initial products"""
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        await db.products.delete_many({})
        print("Cleared existing products")
        
        result = await db.products.insert_many(products)
        print(f"Inserted {len(result.inserted_ids)} products successfully!")
        
        count = await db.products.count_documents({})
        print(f"Total products in database: {count}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    print("Starting database seed...")
    asyncio.run(seed_products())
    print("Database seed complete!")
