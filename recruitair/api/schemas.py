from typing import List

from pydantic import BaseModel, Field


class EvalRequest(BaseModel):
    offer_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Job criteria description",
        examples=["Experience with Python", "Knowledge of ML algorithms."],
    )


class EvalResponse(BaseModel):
    class CriteriaItem(BaseModel):
        description: str = Field(..., description="Description of the extracted criterion from the job offer")
        importance: float = Field(
            ..., description="Importance of the extracted criterion on a scale from 0 to 1", ge=0, le=1
        )

    criteria: List[CriteriaItem]
