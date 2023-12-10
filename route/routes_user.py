
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import models_job

router = APIRouter()


#####################
#   CRUD FOR USER   #
#####################


@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=models_job.User)
def create_user(request: Request, user: models_job.User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["user"].insert_one(user)
    created_user = request.app.database["user"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


@router.get("/", response_description="List all users", response_model=List[models_job.User])
def list_user(request: Request):
    users = list(request.app.database["user"].find(limit=100))
    return users


@router.get("/{id}", response_description="Get a single user by id", response_model=models_job.User)
def find_user(id: str, request: Request):
    if (user := request.app.database["user"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.put("/{id}", response_description="Update a user", response_model=models_job.User)
def update_user(id: str, request: Request, user: models_job.UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = request.app.database["user"].update_one(
            {"_id": id}, {"$set": user}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    if (
        existing_user := request.app.database["user"].find_one({"_id": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a User")
def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database["user"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")