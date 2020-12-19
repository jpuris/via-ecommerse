from fastapi import APIRouter, Body, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import ItemModel, UpdateItemModel

router = APIRouter()


@router.post("/", response_description="Add a new item")
async def add_item(request: Request, item: ItemModel = Body(...)):
    # Convert item model obj to JSON representation of it
    item = jsonable_encoder(item)
    # Insert item JSON dict in MongoDB collection "items"
    new_item = await request.app.mongodb["items"].insert_one(item)
    # Return inserted item
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@router.get("/", response_description="List all items")
async def list_items(request: Request):
    # Get and return all docs packaged in an array from "items" collection
    return [doc for doc in await request.app.mongodb["items"].find().to_list(length=100)]


@router.get("/{id}", response_description="Get a single item")
async def get_item(id: str, request: Request):
    # Get single doc by ID
    # If exists, return it
    # Else rise 404 error
    if (item := await request.app.mongodb["items"].find_one({"_id": id})) is not None:
        return item
    raise HTTPException(status_code=404, detail=f"item {id} not found")


@router.get("/{id}/stock", response_description="Get a single item's remaining stock")
async def get_item_stock(id: str, request: Request):
    # Get single doc by ID, stock field
    # If exists, return it
    # Else rise 404 error
    if (item := await request.app.mongodb["items"].find_one({"_id": id}, {"stock": 1})) is not None:
        return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")


@router.delete("/all", response_description="Delete all items")
async def delete_all_items(request: Request):
    # Delete all docs in collection
    delete_result = await request.app.mongodb["items"].delete_many({})
    # If delete feedback returns at least one deleted doc, all is good
    if delete_result.deleted_count > 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, )
    # Else rise 404 as nothing was found to be deleted
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing to delete")


@router.delete("/{id}", response_description="Delete an item")
async def delete_item(id: str, request: Request):
    # Ask MongoDB to delete a doc by its _id
    delete_result = await request.app.mongodb["items"].delete_one({"_id": id})
    # If there was a delete, return 204 (https://httpstatuses.com/204)
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    # Else rise 404 error
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")


@router.put("/{id}", response_description="Update an item")
async def update_item(id: str, request: Request, item: UpdateItemModel = Body(...)):
    # Convert the model object into proper JSON
    item = {k: v for k, v in item.dict().items() if v is not None}

    # Check if object has any keys
    if len(item) >= 1:
        update_result = await request.app.mongodb["items"].update_one({"_id": id}, {"$set": item})

        # Check if mongodb updated a doc
        if update_result.modified_count == 1:
            if (updated_item := await request.app.mongodb["items"].find_one({"_id": id})) is not None:
                return updated_item

    # If there is no change body, return the already existing
    if (existing_item := await request.app.mongodb["items"].find_one({"_id": id})) is not None:
        return existing_item

    # if no update body is found and no existing key was found, return 404
    raise HTTPException(status_code=404, detail=f"item {id} not found")


@router.put("/{id}/reserve", response_description="Reserve an item")
async def reserve_item(id: str, request: Request, quantity: int):
    # Check if item exists
    if (item := await request.app.mongodb["items"].find_one({"_id": id}, {"stock": 1})) is not None:
        # Check if warehouse has enough to reserve
        if (remaining := item["stock"] - quantity) >= 0:
            item["stock"] = remaining
            # Update warehouse data
            update_result = await request.app.mongodb["items"].update_one({"_id": id}, {"$set": item})

            # Check if there was any update done
            if update_result.modified_count == 1:
                if (updated_item := await request.app.mongodb["items"].find_one({"_id": id})) is not None:
                    return updated_item

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"no stock for item {id}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")
