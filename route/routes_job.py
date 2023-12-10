
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import models_job

router = APIRouter()


#####################
#   CRUD FOR JOBS   #
#####################


@router.post("/{user_id}/", response_description="Create a new job", status_code=status.HTTP_201_CREATED,
             response_model=models_job.Job)
def create_job(request: Request, user_id: str, job: models_job.Job = Body(...)):
    job = jsonable_encoder(job)
    new_job = request.app.database["job"].insert_one(job)
    created_job = request.app.database["job"].find_one(
        {"_id": new_job.inserted_id}
    )
    # Update the user's job_ids field
    user_query = {"_id": user_id}
    user_update = {"$addToSet": {"job_ids": str(new_job.inserted_id)}}
    result = request.app.database["user"].update_one(user_query, user_update)

    if result.modified_count == 0:
        # If no user is found with the given ID, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    return created_job


@router.get("/{user_id}/", response_description="List all jobs", response_model=List[models_job.Job])
def list_jobs(request: Request):
    jobs = list(request.app.database["job"].find(limit=100))
    return jobs


@router.get("/{user_id}/{id}", response_description="Get a single job by id", response_model=models_job.Job)
def find_job(id: str, request: Request):
    if (job := request.app.database["job"].find_one({"_id": id})) is not None:
        return job

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {id} not found")


@router.put("/{user_id}/{id}", response_description="Update a job", response_model=models_job.Job)
def update_job(id: str, request: Request, job: models_job.JobUpdate = Body(...)):
    job = {k: v for k, v in job.dict().items() if v is not None}

    if len(job) >= 1:
        update_result = request.app.database["job"].update_one(
            {"_id": id}, {"$set": job}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {id} not found")

    if (
        existing_job := request.app.database["job"].find_one({"_id": id})
    ) is not None:
        return existing_job

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {id} not found")


@router.delete("/{user_id}/{id}", response_description="Delete a job")
def delete_job(id: str, user_id: str, request: Request, response: Response):
    # Find the job to be deleted
    deleted_job = request.app.database["job"].find_one({"_id": id})

    if deleted_job:
        # Delete the job from the "job" collection
        delete_result = request.app.database["job"].delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            # Remove the job ID from the corresponding user's job_ids array
            user_update_query = {"_id": user_id}
            user_update = {"$pull": {"job_ids": id}}
            request.app.database["user"].update_one(user_update_query, user_update)

            response.status_code = status.HTTP_204_NO_CONTENT
            return response

    # If the job is not found or not deleted, raise a 404 error
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {id} not found")