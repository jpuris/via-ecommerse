from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from config import settings

from .models import ItemModel

router = APIRouter()


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


@router.delete("/all", response_description="Delete all items")
async def delete_all_items(request: Request):
    # Delete all docs in collection
    delete_result = await request.app.mongodb["items"].delete_many({})
    # If delete feedback returns at least one deleted doc, all is good
    if delete_result.deleted_count > 0:
        return JSONResponse(status_code=status.HTTP_200_OK)
    # Else rise 404 as nothing was found to be deleted
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing to delete")


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


@router.post("/sync", response_description="Sync catalog with warehouse")
async def sync_items(request: Request):
    # get all items from WH
    response = requests.get(f'http://{settings.WH_API_HOST}:{settings.WH_API_PORT}/api/v1/items/')
    if response.status_code == 200:
        wh_items = response.json()
        await request.app.mongodb["items"].delete_many({})
        if len(wh_items) > 0:
            insert_result = await request.app.mongodb["items"].insert_many(wh_items)
            inserted_count = len(insert_result.inserted_ids)
            if inserted_count > 0:
                return f"Synced {inserted_count} items!"
        else:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"There is a problem with Warehouse service!")
    # Get and return all docs packaged in an array from "items" collection
    return [doc for doc in await request.app.mongodb["items"].find().to_list(length=100)]


@router.post("/{id}/sync", response_description="Sync single item with warehouse")
async def sync_item(id: str, request: Request):

    # get all items from WH
    response = requests.get(f'http://{settings.WH_API_HOST}:{settings.WH_API_PORT}/api/v1/items/{id}')
    if response.status_code == 200:
        wh_item = response.json()
        if (existing_item := await request.app.mongodb["items"].find_one({"_id": id})) is not None and existing_item != wh_item:
            update_result = await request.app.mongodb["items"].update_one({"_id": id}, {"$set": response.json()})
            if update_result.modified_count == 1:
                return f"Item {id} sync successful!"
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unable to store the new version of item!")
        else:
            return JSONResponse(status_code=status.HTTP_205_RESET_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
