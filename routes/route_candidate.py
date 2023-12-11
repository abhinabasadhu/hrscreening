
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import model_candidate

router = APIRouter()

#######################
#  CRUD FOR CANDIDATE #
#######################


@router.post("/", response_description="Create a new candidate", status_code=status.HTTP_201_CREATED, response_model=model_candidate.Candidate)
def create_candidate(request: Request, candidate: model_candidate.Candidate = Body(...)):
    candidate = jsonable_encoder(candidate)
    new_candidate = request.app.database["candidate"].insert_one(candidate)
    created_candidate = request.app.database["candidate"].find_one(
        {"_id": new_candidate.inserted_id}
    )

    return created_candidate


@router.get("/", response_description="List all candidates", response_model=List[model_candidate.Candidate])
def list_candidates(request: Request):
    candidates = list(request.app.database["candidate"].find(limit=100))
    return candidates


@router.get("/{id}", response_description="Get a single candidate by id", response_model=model_candidate.Candidate)
def find_candidate(id: str, request: Request):
    if (candidate := request.app.database["candidate"].find_one({"_id": id})) is not None:
        return candidate

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {id} not found")


@router.put("/{id}", response_description="Update a candidate", response_model=model_candidate.Candidate)
def update_candidate(id: str, request: Request, candidate: model_candidate.CandidateUpdate = Body(...)):
    candidate = {k: v for k, v in candidate.dict().items() if v is not None}

    if len(candidate) >= 1:
        update_result = request.app.database["candidate"].update_one(
            {"_id": id}, {"$set": candidate}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {id} not found")

    if (
        existing_candidate := request.app.database["candidate"].find_one({"_id": id})
    ) is not None:
        return existing_candidate

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {id} not found")


@router.delete("/{id}", response_description="Delete a candidate")
def delete_candidate(id: str, request: Request, response: Response):
    delete_result = request.app.database["candidate"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {id} not found")

