from fastapi import FastAPI
from routes import products
from routes import orders

app = FastAPI()

# Include the router
app.include_router(products.router)
app.include_router(orders.router)