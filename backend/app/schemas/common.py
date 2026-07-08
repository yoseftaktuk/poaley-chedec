from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str


class ApiRootResponse(BaseModel):
    message: str
    docs: str


class UploadImageResponse(BaseModel):
    url: str
    public_id: str
