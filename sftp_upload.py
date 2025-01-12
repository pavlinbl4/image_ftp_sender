import json
import os
from pathlib import Path
import paramiko
from tqdm import tqdm


def sftp_uploader(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    sftp_details = config['sftp_details']

    try:
        ssh_client.connect(
            hostname=sftp_details["hostname"],
            port=sftp_details.get("port", 22),
            username=sftp_details["username"],
            password=sftp_details["password"]
        )

        with ssh_client.open_sftp() as sftp:
            total_size = os.path.getsize(file_path)
            file_name = Path(file_path).name
            remote_file_path = sftp_details.get("remote_directory", "/") + '/' + file_name

            # Проверка и создание удалённой директории
            remote_dir = str(Path(remote_file_path).parent)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                sftp.mkdir(remote_dir)

            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as pbar:
                def callback(bytes_transferred, _):
                    pbar.update(bytes_transferred)

                sftp.put(file_path, remote_file_path, callback=callback)

            files = sftp.listdir(remote_dir)
            # print("Содержимое директории:", files)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if ssh_client.get_transport() is not None:
            ssh_client.close()
        print(f'Файл {file_name} успешно загружен на сервер {sftp_details["hostname"]}.')


if __name__ == '__main__':
    _local_file = '/Users/evgeniy/Desktop/prevue/20241211PC118110-Edit.JPG'


    # _sftp_details = config['sftp_details']
    sftp_uploader(_local_file)