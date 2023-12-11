
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import model_candidate
from models import model_job
from utils import util
router = APIRouter()

#######################
#     APPLY JOB       #
#######################


@router.post("/{candidate_id}/{job_id}", response_description="JobApplication", status_code=status.HTTP_201_CREATED,)
def apply_job(request: Request, candidate_id: str, job_id: str):
    job = request.app.database["job"].find_one({"_id": job_id})
    candidate = request.app.database["candidate"].find_one({"_id": candidate_id})

    if not job or not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {candidate_id} or"
                                                                          f" Job with ID {job_id} not found")

    # Update the job's candidates field
    job_update = {"$addToSet": {"candidates": str(candidate)}}
    request.app.database["job"].update_one(job, job_update)

    return jsonable_encoder(job)


@router.get("/{user_id}/{candidate_id}/{job_id}", response_description="Match Report")
def get_match_report(request: Request, user_id: str, candidate_id: str, job_id: str):
    user = request.app.database["user"].find_one({"_id": user_id})

    if job_id not in user['job_ids']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")

    job = request.app.database["job"].find_one({"_id": job_id})
    candidate = request.app.database["candidate"].find_one({"_id": candidate_id})

    if not job or not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with ID {candidate_id} or"
                                                                          f" Job with ID {job_id} not found")

    match_report = util.job_match(job, candidate)

    return jsonable_encoder(match_report)

