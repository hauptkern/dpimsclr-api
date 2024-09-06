from core.logger import logging
from typing import Dict
from PIL import Image
from schemas.scale import VisionScaleTask, NormalScaleTask
from storage import s3
from io import BytesIO
from arq.worker import Worker, Retry
from .scalers import vision_scale_image, normal_scale_image
from .filters import crop_blank_spaces
from .token_calculator import calculate_image_token_cost
from .settings import settings

# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# -------- background tasks --------
async def normal_scale_task(ctx: Worker, nsq: NormalScaleTask) -> Dict[str, bool] | Dict[str, str]:
    try:
        buff = BytesIO()
        s3.download_fileobj(settings.S3_QUEUE_BUCKET_NAME, nsq.objName, buff)
        if nsq.cropBlankSpaces:
            bl_crop_output = crop_blank_spaces(Image.open(buff))
            buff = BytesIO()
            bl_crop_output.save(buff, format="PNG")
        scaled_img = await normal_scale_image(Image.open(buff), nsq)
        scaled_img_buff = BytesIO()
        scaled_img.save(scaled_img_buff, format="PNG")
        scaled_img_buff.seek(0)
        s3.upload_fileobj(scaled_img_buff, settings.S3_RESULT_BUCKET_NAME, nsq.objName)
        return {"success": True}
    except Exception as e:
        if settings.JOB_LOGGING_ENABLED:
            logger.error(e, exc_info=True)
        if settings.JOB_RETRY_ENABLED and settings.JOB_RETRY_DEFER > 0:
            if ctx['job_try'] == settings.JOB_MAX_TRY_COUNT:
                return {"success": False}
            raise Retry(defer=ctx['job_try'] * settings.JOB_RETRY_DEFER)
        return {"success": False}


async def vision_scale_task(ctx: Worker, vsq: VisionScaleTask) -> Dict[str, bool] | Dict[str, int]:
    try:
        buff = BytesIO()
        s3.download_fileobj(settings.S3_QUEUE_BUCKET_NAME, vsq.objName, buff)
        if vsq.cropBlankSpaces:
            bl_crop_output = crop_blank_spaces(Image.open(buff))
            buff = BytesIO()
            bl_crop_output.save(buff, format="PNG")
        scaled_img = await vision_scale_image(Image.open(buff), vsq.scaleDetail)
        scaled_img_buff = BytesIO()
        scaled_img.save(scaled_img_buff, format="PNG")
        scaled_img_buff.seek(0)
        s3.upload_fileobj(scaled_img_buff, settings.S3_RESULT_BUCKET_NAME, vsq.objName)
        if vsq.countToken:
            token_cost = calculate_image_token_cost(scaled_img.width, scaled_img.height, vsq.countDetail)
            return {"success": True, "cost": token_cost}
        else:
            return {"success": True}
    except Exception as e:
        if settings.JOB_LOGGING_ENABLED:
            logger.error(e, exc_info=True)
        if settings.JOB_RETRY_ENABLED and settings.JOB_RETRY_DEFER > 0:
            if ctx['job_try'] == settings.JOB_MAX_TRY_COUNT:
                return {"success": False}
            raise Retry(defer=ctx['job_try'] * settings.JOB_RETRY_DEFER)
        return {"success": False}


# -------- base functions --------
async def startup(ctx: Worker) -> None:
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker End")
