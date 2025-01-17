from fastapi import APIRouter, Depends, Response
from queries.items_queries import ItemIn, ItemRepository, ItemOut, Error
from typing import Union, Optional, List
router = APIRouter()


@router.post("/items", response_model=Union[ItemOut, Error])
def add_item(item: ItemIn, response: Response, repo: ItemRepository = Depends()):
    itemss = repo.add_item(item)
    if itemss is None:
        response.status_code = 400
    return itemss

@router.get("/items", response_model=Union[List[ItemOut], Error])
def get_all_items(
    repo: ItemRepository=Depends(),
):
    return repo.get_all_items()

@router.put("/items/{item_id}", response_model=Union[ItemOut, Error])
def update_inventory(item_id: int, item: ItemIn, repo: ItemRepository = Depends()) -> Union[Error, ItemOut]:
    return repo.update_inventory(item_id, item)

@router.delete("/items/{item_id}", response_model=bool)
def delete_item(item_id: int, repo: ItemRepository = Depends()) -> bool:
    return repo.delete_item(item_id)

@router.get("/items/{item_id}", response_model=Optional[ItemOut])
def get_item(item_id: int, response: Response, repo: ItemRepository = Depends()) -> ItemOut:
    item = repo.get_item(item_id)
    if item is None:
        response.status_code = 404
    return item
