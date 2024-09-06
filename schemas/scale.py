from pydantic import BaseModel


class NormalScaleTask(BaseModel):
    objName: str
    width: int | None = None
    height: int | None = None
    percentage: float | None = None
    lockAspectRatio: bool | None = None
    cropBlankSpaces: bool | None = False


class VisionScaleTask(BaseModel):
    objName: str
    scaleDetail: str = "low"
    countToken: bool = True
    countDetail: str = "low"
    cropBlankSpaces: bool | None = False


class ScaleTaskResponse(BaseModel):
    job_id: str
