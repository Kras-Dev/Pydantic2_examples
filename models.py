#models.py
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator

class Role(str, Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class BaseUser(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    second_name: str = Field(..., min_length=1)

    @field_validator("first_name", "second_name", mode="before")
    @classmethod
    def capitalize_name(cls, name: str) -> str:
        return name.strip().capitalize()

class User(BaseUser):
    age: int = Field(..., ge=18, le=120)
    password: str = Field(min_length=8, pattern=r".*[0-9].*[!@#$%^&*].*")

class AdminUser(User):
    role: Role
    # role: Literal["admin", "superadmin"]

    def has_permission(self, permission: str) -> bool:
        permissions = {
            "admin": ["read", "write", "delete"],
            "superadmin": ["read", "write", "delete", "manage_users"]
        }
        return permission in permissions.get(self.role.value, [])



