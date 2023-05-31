import uuid


def get_product_image_name(original_name: str) -> str:
    # generate unique image name for product
    return f'{uuid.uuid4()}.{original_name.split(".")[-1]}'
