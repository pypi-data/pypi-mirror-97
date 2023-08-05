def get_image_urls(obj, field, sizes={'base': None}):
    images = {}
    for size in sizes:
        img_field = f"{field}_urls"
        try:
            images[size] = (
                getattr(obj, img_field).get(size) if getattr(obj, img_field) else None
            )
        except:
            images[size] = ""
    return images
