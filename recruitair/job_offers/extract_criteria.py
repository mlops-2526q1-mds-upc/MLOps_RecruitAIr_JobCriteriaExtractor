import os
import string
from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class KeyCriterion(BaseModel):
    title: str = Field(description="The title of the key requirement or criterion in one or two words at most.")
    description: str = Field(description="A brief but exhaustive description of the key requirement.")
    importance: int = Field(
        ge=1,
        le=5,
        description="An integer from 1 to 5 indicating the importance of "
        "an applicant to this job offer to fulfill this key requirement.",
    )


class KeyCriteriaResponse(BaseModel):
    key_criteria: List[KeyCriterion] = Field(
        description="An exhaustive list of all the key requirements or criteria that are explicit or implicit in the job offer."
    )


with open(os.path.join(os.path.dirname(__file__), "prompts", "extract_criteria.txt")) as f:
    PROMPT_TEMPLATE = string.Template(f.read())


def extract_key_criteria_from_job_offer(job_offer_text: str) -> KeyCriteriaResponse:
    llm = ChatOllama(model="dolphin3", temperature=0)
    prompt = PROMPT_TEMPLATE.substitute(job_offer_text=job_offer_text)
    response = llm.with_structured_output(KeyCriteriaResponse, method="json_schema").invoke(prompt)
    return response


if __name__ == "__main__":
    sample_job_offer = """
    We are looking for a Software Engineer with experience in Python and machine
    learning. The ideal candidate should have at least 3 years of experience in
    software development, a strong understanding of algorithms and data structures,
    and the ability to work in a fast-paced environment. Familiarity with cloud
    platforms like AWS or GCP is a plus. Excellent communication skills and the
    ability to work in a team are essential.
    """
    criteria = extract_key_criteria_from_job_offer(sample_job_offer)
    for criterion in criteria.key_criteria:
        print(f"Title: {criterion.title}")
        print(f"Description: {criterion.description}")
        print(f"Importance: {criterion.importance}")
        print()
