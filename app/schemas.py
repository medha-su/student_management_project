from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class StudentBase(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=30)
    course: Optional[str] = Field(default=None, max_length=120)
    address: Optional[str] = Field(default=None, max_length=300)
    enrollment_date: Optional[date] = None

    @model_validator(mode="after")
    def require_contact_method(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least one contact method: email or phone.")
        return self

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=30)
    course: Optional[str] = Field(default=None, max_length=120)
    address: Optional[str] = Field(default=None, max_length=300)
    enrollment_date: Optional[date] = None

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @model_validator(mode="after")
    def validate_update_values(self):
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("Name cannot be null.")
        if "date_of_birth" in self.model_fields_set and self.date_of_birth is None:
            raise ValueError("Date of birth cannot be null.")
        if self.name is not None and not self.name.strip():
            raise ValueError("Name cannot be blank.")
        return self

class StudentRead(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
