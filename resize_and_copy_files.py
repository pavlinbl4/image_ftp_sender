from pathlib import Path

from PIL import Image

from sftp_upload import sftp_uploader


def compress_image(input_path,
                   output_path='/Users/evgeniy/My Drive (photo.new.prospect@gmail.com)/NP/Фотоархив/new_',
                   quality=75, new_width=1000):
    # /Users/evgeniy/My Drive (photo.new.prospect@gmail.com)/NP/Фотоархив/new_
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

    # заливаю файл на новый сайт
    # sftp_uploader(f'{output_path}/{file_name}')
    # print(f"Изображение сохранено: {output_path}, качество: {quality}")


if __name__ == '__main__':
    # Пример использования функции
    input_image_path = '/Users/evgeniy/Desktop/Images_for_FTP_batch/20241114PB146762.JPG'  # Путь к исходному изображению
    # output_image_path = '/Users/evgeniy/Desktop'  # Путь к сохраненному изображению
    # compress_image(input_image_path, output_image_path, quality=75, new_width=800)
    compress_image(input_image_path)
