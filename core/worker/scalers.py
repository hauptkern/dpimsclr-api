from PIL import Image
from schemas.scale import NormalScaleTask


async def normal_scale_image(img, nsq: NormalScaleTask) -> Image.Image:
    original_width, original_height = img.size
    if nsq.percentage is not None and nsq.percentage > 0:
        new_width = int(original_width * nsq.percentage / 100)
        new_height = int(original_height * nsq.percentage / 100)
    elif None not in [nsq.width, nsq.height] and 0 not in [nsq.width, nsq.height]:
        new_width = max(1, nsq.width if nsq.width is not None else original_width)
        new_height = max(1, nsq.height if nsq.height is not None else original_height)
        if nsq.lockAspectRatio:
            if nsq.width is not None and nsq.height is None:
                new_height = max(1, int(original_height * (new_width / original_width)))
            elif nsq.height is not None and nsq.width is None:
                new_width = max(1, int(original_width * (new_height / original_height)))
            else:
                # If both width and height are provided, use width to determine the scaling factor
                scaling_factor = new_width / original_width
                new_height = max(1, int(original_height * scaling_factor))
    else:
        return img
    new_width = max(1, new_width)
    new_height = max(1, new_height)
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_img


async def vision_scale_image(img, detail='low') -> Image.Image:
    if detail == 'low':
        return img  # No scaling for low detail
    width, height = img.size
    if width <= 512 and height <= 512:
        return img
    if width > 2048 or height > 2048:
        img.thumbnail((2048, 2048))
        width, height = img.size
    if width < height:
        new_width = 768
        new_height = int(height * (768 / width))
    else:
        new_height = 768
        new_width = int(width * (768 / height))
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
