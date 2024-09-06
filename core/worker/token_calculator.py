from math import ceil, floor


def calculate_image_token_cost(width, height, detail='low'):
    if detail == 'low':
        return 85
    if width > 2048 or height > 2048:
        aspect_ratio = width / height
        if width > height:
            width = 2048
            height = int(width / aspect_ratio)
        else:
            height = 2048
            width = int(height * aspect_ratio)
    if height > width > 768:
        scale_factor = 768 / width
    elif width >= height > 768:
        scale_factor = 768 / height
    else:
        scale_factor = 1
    scaled_width = floor(width * scale_factor)
    scaled_height = floor(height * scale_factor)
    num_squares = ceil(scaled_width / 512) * ceil(scaled_height / 512)
    token_cost = 170 * num_squares + 85
    return token_cost
