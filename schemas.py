from pydantic import BaseModel
from datetime import date
from fastapi import Form

class Formdata(BaseModel):
    task_title: str
    task_body: str

    @classmethod
    def as_form(
        cls,
        task_title: str = Form(...),
        task_body: str = Form(...)
    ):
        return cls(task_title=task_title,task_body=task_body)