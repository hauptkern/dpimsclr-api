from typing import Any
from fastapi import APIRouter
from arq.jobs import Job as ArqJob
from core.utils import queue
from schemas.scale import VisionScaleTask, NormalScaleTask, ScaleTaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/scale", status_code=201, response_model=ScaleTaskResponse)
async def create_normal_scale_task(nst: NormalScaleTask) -> ScaleTaskResponse:
    """Create a new normal scaler task.

    Parameters
    ----------
    nst: NormalScaleTask
        Data containing image scale options to be processed.
        If percentage is specified, width,height and lockAspectRatio are ignored.

    Returns
    -------
    ScaleTaskResponse
        A dictionary containing the ID of the created job.
    """
    job = await queue.pool.enqueue_job("normal_scale_task", nst)
    return ScaleTaskResponse(job_id=job.job_id)


@router.get("/scale/{job_id}")
async def get_normal_scale_job(job_id: str) -> dict[str, Any] | None:
    """Get information about a normal scaler job.

    Parameters
    ----------
    job_id: str
        The ID of the job.

    Returns
    -------
    Optional[dict[str, Any]]
        A dictionary containing information about the job if found, or None otherwise.
    """
    job = ArqJob(job_id, queue.pool)
    job_info: dict | None = await job.info()
    if job_info is None:
        return {"job_id": None}
    return vars(job_info)


@router.post("/vision-scale", status_code=201, response_model=ScaleTaskResponse)
async def create_vision_scale_task(vsq: VisionScaleTask) -> ScaleTaskResponse:
    """Create a new vision scaler task.
    It scales document images according to GPT-4V conventions.

    Parameters
    ----------
    vsq: VisionScaleTask
            Data containing image scale options to be processed.
            If scaleDetail is set to low, image scale is ignored.

    Returns
    -------
    ScaleTaskResponse
        A dictionary containing the ID of the created job.
    """
    job = await queue.pool.enqueue_job("vision_scale_task", vsq)
    return ScaleTaskResponse(job_id=job.job_id)


@router.get("/vision-scale/{job_id}")
async def get_vision_scale_job(job_id: str) -> dict[str, Any] | None:
    """Get information about a vision scaler job.

    Parameters
    ----------
    job_id: str
        The ID of the job.

    Returns
    -------
    Optional[dict[str, Any]]
        A dictionary containing information about the job if found, or None otherwise.
    """
    job = ArqJob(job_id, queue.pool)
    job_info: dict | None = await job.info()
    if job_info is None:
        return {"job_id": None}
    return vars(job_info)
