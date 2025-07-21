from fastapi import APIRouter, HTTPException, status
from schemas import OrderRequest, OrderResponse
from database import order_collection
from bson import ObjectId
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from database import order_collection, product_collection
from bson import ObjectId
from pymongo import ASCENDING

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderRequest):
    order_data = order.model_dump()
    result =await order_collection.insert_one(order_data)
    return OrderResponse(id=str(result.inserted_id))


#get
@router.get("/orders/{user_id}", status_code=200)
async def get_orders(
    user_id: str,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": ASCENDING}},
        {"$skip": offset},
        {"$limit": limit},
        {
            "$unwind": "$items"
        },
        {
            "$lookup": {
                "from": "products",
                "let": {"pid": "$items.productId"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": [{"$toString": "$_id"}, "$$pid"]}
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "name": 1,
                            "price":1,
                            "id": {"$toString": "$_id"}
                        }
                    }
                ],
                "as": "productDetails"
            }
        },
        {
            "$unwind": {
                "path": "$productDetails",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "items": {
                    "$push": {
                        
                        "productDetails": "$productDetails",
                        "qty": "$items.qty"
                    }
                }
            }
        },
        {
            "$addFields": {
                "id": {"$toString": "$_id"},
                "total": {
                    "$sum": {
                        "$map": {
                            "input": "$items",
                            "as": "item",
                            "in": {
                                "$multiply": [
                                    "$$item.qty",
                                    {
                                        "$toDouble": {
                                            "$ifNull": ["$$item.productDetails.price", 0]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        },
        {
  "$project": {
    "_id": 0,
    "userId": 1,
    "id": 1,
    "items": {
      "$map": {
        "input": "$items",
        "as": "item",
        "in": {
          
          "productDetails": {
            "name": {
              "$ifNull": ["$$item.productDetails.name", None]
            },
            "id": {
              "$ifNull": ["$$item.productDetails.id", None]
            }
          },"qty": "$$item.qty"
        }
      }
    },
      "total":1
  }
}

    ]

    results = []
    cursor = order_collection.aggregate(pipeline)
    async for doc in cursor:
        results.append(doc)


    response = {
        "data": results,
        "page": {
        "next": offset + limit,
        "limit": len(results), 
        "previous": max(offset - limit, 0)
    }
    }
    return response
    
