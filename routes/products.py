from fastapi import APIRouter, status
from schemas import ProductRequest, ProductResponse
from database import product_collection
from bson import ObjectId
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from database import product_collection
from bson import ObjectId
import re

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductRequest):
    product_data = product.model_dump()
    result = await product_collection.insert_one(product_data)
    return ProductResponse(id=str(result.inserted_id))

#get



@router.get("/products", status_code=200)
async def get_products(
    name: str = Query(None),
    size: str = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    query = {}

    # Regex filter for name (case-insensitive)
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    # Filter by size inside the sizes array
    if size:
        query["sizes.sizes"] = size

    # Find and paginate
    cursor = product_collection.find(query).sort("_id", 1).skip(offset).limit(limit)

    data = []
    async for product in cursor:
        data.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
        })

    response = {
        "data": data,
        "page": {
            "next": offset + limit,
            "limit": len(data),
            "previous": max(offset - limit, 0)
        }
    }

    return JSONResponse(content=response, status_code=200)