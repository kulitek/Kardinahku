import pathlib as pl
from fastapi import Response

def return_image(path: str, filename: str):
    try:
        img = pl.Path(path + filename).resolve().read_bytes()
        extension = filename.split(r'.')[-1]
        media_type = "image/png" if r'.png' in extension else "image/jpeg"
        return Response(content=img, media_type=media_type)
    except Exception as e:
        return {r'error': str(e)}
    else:
        del img
        del extension
        del media_type
