import os
from ftplib import FTP
import json
from tqdm import tqdm
from loguru import logger

from core.config_loader import ConfigLoader
from db_handler import log_file_sent
import socket

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "ftp_upload_log.log")
logger.add(log_file_path, format="{time} {level} {message}", level="INFO", retention="1 day", rotation="1 day")


def upload_file_ftp(file_path, ftp_details):
    ftp = FTP(ftp_details['host'])
    ftp.login(ftp_details['user'], ftp_details['password'])

    # Перейти в указанную удалённую папку
    remote_dir = ftp_details['remote_directory']

    # Проверка, существует ли удалённая папка
    try:
        ftp.cwd(remote_dir)  # Попытка перейти в директорию
    except Exception as e:
        print(f"Ошибка: {e}")
        print(f"Папка {remote_dir} не найдена.")
        # Если папка не существует, создаём её
        ftp.mkd(remote_dir)
        ftp.cwd(remote_dir)

    # Получаем размер файла для отслеживания прогресса
    file_size = os.path.getsize(file_path)

    # Загружаем файл
    with open(file_path, 'rb') as f:
        # Функция для отслеживания прогресса
        def upload_progress(chunk):
            progress_bar.update(len(chunk))  # Обновляем прогресс-бар на каждый чанк

            # Создание прогресс-бара с использованием tqdm

        with tqdm(total=file_size, unit='B', unit_scale=True,
                  desc=f"Загрузка {os.path.basename(file_path)}") as progress_bar:
            # Загружаем файл с прогрессом
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', f, 1024, callback=upload_progress)

    ftp.quit()
    logger.info(f"Файл {file_path} успешно загружен на сервер {ftp_details['host']}.")


def upload_file_to_multiple_ftps(file_path, ftp_details_list):
    for ftp_details in ftp_details_list:

        print(f"Загружаем файл на FTP сервер: {ftp_details['host']}")
        try:
            upload_file_ftp(file_path, ftp_details)
            log_file_sent(os.path.basename(file_path), ftp_details['host'])
        except socket.gaierror:
            logger.error(f'{ftp_details['host']} upload error')


if __name__ == '__main__':
    # Загрузка конфигурации из файла


    site = 'photoupload'
    config = ConfigLoader.load(site)
    # logger.info(f'config: {config}')


    logger.info(f'ftp_details_yaml: {config['ftp_details'][0]}')

    # upload_file_ftp('/Volumes/big4photo/Downloads/бегалиева/HQ8A4066.jpg', _ftp_details)
