"""The models for criteria extraction."""

from typing import List

from pydantic import BaseModel, Field


class KeyCriterion(BaseModel):
    """
    Model that represents an important criteria of a job offer.
    """
    description: str = Field(description="A brief but exhaustive description of the key requirement.")
    importance: int = Field(
        ge=0,
        le=100,
        description="An integer from 0 to 100 indicating the importance of "
        "an applicant to this job offer to fulfill this key requirement.",
    )


class KeyCriteriaResponse(BaseModel):
    """
    Model that represents the response of a model containing the key criteria in the job offer.
    """

    key_criteria: List[KeyCriterion] = Field(
        description="An exhaustive list of all the key requirements or "
        "criteria that are explicit or implicit in the job offer."
    )
