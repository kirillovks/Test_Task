import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
import aiofiles
import aiofiles.os
from PIL import Image
import logging


app = FastAPI()

# making folders
TMP_FOLDER = "tmp"
IMAGES_FOLDER = "images"
os.makedirs(TMP_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)


# logger initialization
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
fh = logging.FileHandler('logs/api_image_filter.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> JSONResponse:
    """
    Uploads an image into a temporary folder.

    Args:
        file: png/jpeg file.

    Returns:
        JSONResponse: message about successful loading.
    """
    logger.info(f"POST запрос с попыткой загрузить файл {file.filename}")

    if not file.content_type == "image/png" and not file.content_type == "image/jpeg":
        logger.warning(f"Загружаемый файл {file.filename} имеет неподдерживаемый тип {file.content_type}")
        raise HTTPException(status_code=400, detail="Неверный формат загружаемого файла (необходим PNG/JPEG)")

    if file.size > 5242880:
        logger.warning(f"Размер загружаемого файла {file.filename} занимает более 5 Мб")
        raise HTTPException(status_code=413, detail="Размер загружаемого файла превышает 5 Мб")

    try:
        path = os.path.join(TMP_FOLDER, file.filename)
        async with aiofiles.open(path, "wb") as buffer:
            await buffer.write(await file.read())
        logger.info(f"Файл сохранен во временную папку и имеет путь: {path}")

        return JSONResponse(
            status_code=200,
            content={
                "Сообщение": f"Файл {file.filename} успешно зашружен",
            },
        )

    except Exception as e:
        logger.error(f"Не удалось загрузить изображение {file.filename} по причине: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Не удалось загрузить изображение: {str(e)}")


@app.get("/process")
async def filter_image() -> FileResponse:
    """
    Gets the latest uploaded image from the temporary folder, applies grayscale filter, and save to the "images" folder.

    Returns:
        FileResponse: filtered image in PNG format.
    """
    logger.info("GET запрос с попыткой обработать последнее загруженное изображение")

    files = os.listdir(TMP_FOLDER)
    if not files:
        logger.warning("Во временной папке нет загруженных изображений")
        raise HTTPException(status_code=404, detail="Нет загруженных изображений")

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(TMP_FOLDER, f)))
    path = os.path.join(TMP_FOLDER, latest_file)
    output_path = os.path.join(IMAGES_FOLDER, latest_file)

    try:
        with Image.open(path) as img:
            grayscale_image = img.convert("L")
            grayscale_image.save(output_path, format="PNG")
        logger.info(f"Изображение обработано и сохранено в: {output_path}")

        await aiofiles.os.remove(path)
        logger.info(f"Оригинал изображения удален из временной папки: {path}")

        return FileResponse(
            output_path,
            media_type="image/png",
        )

    except Exception as e:
        logger.error(f"Не удалось обработать изображение {latest_file.filename} по причине: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Не удалось обработать изображение: {str(e)}")

