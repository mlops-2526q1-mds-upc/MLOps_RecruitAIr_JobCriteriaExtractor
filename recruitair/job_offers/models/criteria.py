from typing import List

from pydantic import BaseModel, Field


class KeyCriterion(BaseModel):
    name: str = Field(description="The brief description of the key requirement or criterion in a few words.")
    importance: int = Field(
        ge=0,
        le=100,
        description="An integer from 0 to 100 indicating the importance of "
        "an applicant to this job offer to fulfill this key requirement.",
    )


class KeyCriteriaResponse(BaseModel):
    key_criteria: List[KeyCriterion] = Field(
        description="An exhaustive list of all the key requirements or criteria that are explicit or implicit in the job offer."
    )
