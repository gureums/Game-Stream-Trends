from pydantic import BaseModel, field_validator
from typing import List, Dict

class TestOutput(BaseModel):
    output: str