import json
import os

from db_handler import initialize_database, is_file_sent
from ftp_uploader import upload_file_to_multiple_ftps
from metadata_handler import get_image_metadata, clear_exif
from loguru import logger

# Удаляем стандартный обработчик
logger.remove()


def main():
    initialize_database()  # Убедиться, что база данных существует

    # Далее идет основной процесс обработки и отправки файлов
    with open('config.json') as f:
        config = json.load(f)

    image_dir = config["image_directory"]
    logger.info(f'{image_dir = }')
    ftp_details = config['ftp_details']

    for file_name in os.listdir(image_dir):

        if file_name.lower().endswith(('jpg', 'jpeg')):
            logger.info(file_name)
            file_path = os.path.join(image_dir, file_name)
            metadata = get_image_metadata(file_path,
                                          tags=['XMP:Description', 'XMP:Label'])

            if metadata.get('XMP:Label') == 'Green' and metadata.get('XMP:Description'):
                if not is_file_sent(file_name):
                    clear_exif(file_path)
                    upload_file_to_multiple_ftps(file_path, ftp_details)


if __name__ == "__main__":
    main()
