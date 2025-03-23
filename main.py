import json
import os

from colorama import init, Fore
from loguru import logger

from db_handler import initialize_database, is_file_sent
from ftp_uploader import upload_file_to_multiple_ftps
from metadata_handler import ImageMetadate
from resize_and_copy_files import compress_image

# Удаляем стандартный обработчик
logger.remove()
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "ftp_upload_log.log")
logger.add(log_file_path, format="{time} {level} {message}", level="INFO", retention="1 day", rotation="1 day")

init(autoreset=True)  # Автоматически сбрасывает стиль после каждого print


def main():
    initialize_database()  # Убедиться, что база данных существует

    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    # Далее идет основной процесс обработки и отправки файлов
    with open(config_path) as f:
        config = json.load(f)

    image_dir = config["image_directory"]
    logger.info(f'{image_dir = }')
    ftp_details = config['ftp_details']

    for file_name in os.listdir(image_dir):
        logger.info(f'check file {file_name}')

        if file_name.lower().endswith(('jpg', 'jpeg')):
            logger.info(file_name)
            file_path = os.path.join(image_dir, file_name)
            image_data = ImageMetadate(file_path)
            metadata = image_data.read_tags(
                                          tags=['XMP:Description', 'XMP:Label'])

            if metadata.get('XMP:Label') == 'Green' and metadata.get('XMP:Description'):
                if not is_file_sent(file_name):
                    image_data.clear_exif()
                    image_data.write_metadate("Label Green")
                    upload_file_to_multiple_ftps(file_path, ftp_details)
                    compress_image(file_path)
            elif not metadata.get('XMP:Description'):
                image_data.write_metadate("Label Purple")
                print(Fore.RED + f"File {file_name} has NO CAPTION !!!\n"
                                 f"Label changed to PURPLE\n")


if __name__ == "__main__":
    main()
