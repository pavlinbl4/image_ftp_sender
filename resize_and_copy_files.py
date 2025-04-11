from pathlib import Path

from PIL import Image
from loguru import logger

from metadata_handler import ImageMetadate

logger.disable('metadata_handler')

import subprocess
import json


def process_image_with_xmp(input_path):
    """
    Считывает XMP-метаданные, сжимает изображение и переносит caption с добавлением keywords.
    """
    # 1. Считываем нужные поля: Description и Subject
    read_cmd = [
        "exiftool",
        "-j",  # JSON-вывод для удобства
        "-XMP:Description",
        "-XMP:Subject",
        input_path
    ]

    result = subprocess.run(read_cmd, capture_output=True, text=True, check=True)
    metadata = json.loads(result.stdout)[0]
    logger.debug(metadata)

    original_description = metadata.get("Description", "").strip()
    logger.info(f"Original description: {original_description}")
    keywords = metadata.get("Subject", [])
    logger.info(f"Keywords: {keywords}")

    if isinstance(keywords, str):  # бывает, что Subject строка
        keywords = [keywords]

    # 2. Формируем новый Description
    if keywords:
        keyword_line = "keywords: " + ", ".join(keywords)
        new_description = f"{original_description}\n\n{keyword_line}" if original_description else keyword_line
    else:
        new_description = original_description

    # 3. Сжимаем изображение (внешняя функция)
    compressed_path = compress_image(input_path)

    # 4. Записываем новый Description в сжатое изображение
    write_cmd = [
        "exiftool",
        "-overwrite_original",
        f"-XMP:Description={new_description}",
        compressed_path
    ]

    # Используем shell quoting для безопасного ввода строки
    subprocess.run(write_cmd, check=True)

    return compressed_path




def compress_image(input_path,
                   output_path='/Users/evgeniy/My Drive (photo.new.prospect@gmail.com)/NP/Фотоархив/new_',
                   quality=75, new_width=1000):
    # /Users/evgeniy/My Drive (photo.new.prospect@gmail.com)/NP/Фотоархив/new_
    logger.info(f'Compressing {input_path}')

    image_metadate = ImageMetadate(input_path)
    logger.info(image_metadate.read_tags(
        tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))

    # Открываем изображение
    img = Image.open(input_path)
    file_name = Path(input_path).name

    # Если задана новая ширина, то изменяем размер изображения
    if new_width:
        wpercent = (new_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((new_width, hsize), Image.Resampling.LANCZOS)

    # Сохраняем изображение с заданным качеством
    img.save(f'{output_path}/{file_name}', "JPEG", quality=quality)
    # logger.info(f'Compressed {output_path}/{file_name}')
    return f'{output_path}/{file_name}'


    # # copy_metadata(input_path, f'{output_path}/{file_name}')
    # compressed_image_metadate = ImageMetadate(f'{output_path}/{file_name}')
    # # compressed_image_metadate = image_metadate
    # logger.info(image_metadate.extract_all_metadate()[0])
    # compressed_image_metadate.write_all_metadate(image_metadate.extract_all_metadate()[0])
    #
    # logger.info(compressed_image_metadate.read_tags(
    #     tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))



    # заливаю файл на новый сайт
    # sftp_uploader(f'{output_path}/{file_name}')
    # print(f"Изображение сохранено: {output_path}, качество: {quality}")


if __name__ == '__main__':
    # Пример использования функции
    input_image_path = 'test_image/20240830PEV_4742.JPG'  # Путь к исходному изображению
    output_image_path = '/Users/evgeniy/Desktop/prevue'  # Путь к сохраненному изображению
    # compress_image(input_image_path, output_image_path, quality=75, new_width=800)
    # compress_image(input_image_path, output_image_path)
    process_image_with_xmp(input_image_path)
