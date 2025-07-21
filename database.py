from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb+srv://admin:Evans24@cluster0.amzbsnb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # or your MongoDB Atlas URI

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client["ecommerce"]  # change to your DB name
product_collection = database["products"]  # change to your collection
order_collection = database["orders"]  # Collection for storing orders
