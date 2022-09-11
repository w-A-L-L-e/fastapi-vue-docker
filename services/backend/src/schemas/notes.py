from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Notes


NoteInSchema = pydantic_model_creator(
    Notes, 
    name="NoteInSchema", 
    exclude=["author_id"], 
    exclude_readonly=True
)

NoteOutSchema = pydantic_model_creator(
    Notes, name="Note", exclude =[
      "modified_at", "author.password", "author.created_at", "author.modified_at"
    ]
)

# these are totally not needed now
# class UpdateNote(BaseModel):
#     title: str # make this required
#     content: Optional[str]
# 
# class CreateNote(BaseModel):
#     title: str # make this required
#     content: Optional[str]

#more inspiration:
# job_pydantic = pydantic_model_creator(Job)
# job_pydantic_no_ids = pydantic_model_creator(Job, exclude_readonly=True)
# # ...
# @app.put("/job/{job_id}", response_model=job_pydantic, responses={404: {"model": HTTPNotFoundError}})
# async def update_job(job_id: int, job: job_pydantic):
#     await Job.filter(id=job_id).update(**job.dict())
#     return await job_pydantic_no_ids.from_queryset_single(Job.get(id=job_id))

