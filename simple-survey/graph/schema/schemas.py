from typing import List

from pydantic import BaseModel, Field


class ExtractedAnswer(BaseModel):
    """Answer the question."""
    answer: str = Field(description="The extracted answer for the question")
    extracted: bool = Field(
        description="True if the answer is extracted from the user's response, False otherwise")

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"


class OutputAnswer(BaseModel):
    """Answer the question."""
    message: str = Field(description="Message to the user")

    def __str__(self):
        return f"Message: {self.message}"
