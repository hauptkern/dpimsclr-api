from pydantic import BaseModel


class NormalScaleTask(BaseModel):
    objName: str
    width: int | None = None
    height: int | None = None
    percentage: float | None = None
    lock_aspect_ratio: bool | None = None


class VisionScaleTask(BaseModel):
    objName: str
    scaleDetail: str = "low"
    countToken: bool = True
    countDetail: str = "low"


class ScaleTaskResponse(BaseModel):
    job_id: str
