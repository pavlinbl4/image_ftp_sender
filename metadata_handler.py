# pip install PyExifTool
import exiftool
from loguru import logger

"""
    Извлекает значения указанных тегов из изображения.

    :param file_path: Путь к файлу изображения.
    :param tags: Список тегов, которые нужно получить.
    :return: Словарь с тегами и их значениями.
    """


class ImageMetadate:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_all_metadate(self):
        with exiftool.ExifToolHelper() as et:
            metadate = et.get_metadata(self.file_path)
        return metadate

    def extract_iptc(self):
        with exiftool.ExifToolHelper() as eth:
            metadate = eth.get_tags(self.file_path, 'IPTC:*')
        return metadate

    def extract_xmp(self):
        with exiftool.ExifToolHelper() as eth:
            metadate = eth.get_tags(self.file_path, 'XMP:*')
        return metadate

    def extract_exif(self):
        with exiftool.ExifToolHelper() as eth:
            metadate = eth.get_tags(self.file_path, 'EXIF:*')
        return metadate

    def clear_exif(self):
        with exiftool.ExifTool() as et:
            # Удаляем только EXIF данные
            et.execute(
                b'-EXIF:all=',
                b'-overwrite_original',
                self.file_path.encode('utf-8')
            )

    def write_metadate(self, label_color):
        creator_name = "Валентин Антонов"

        # Формируем список команд
        commands = [
            f'-XMP:Label={label_color}'.encode('utf-8'),
            f'-XMP:Creator={creator_name}'.encode('utf-8'),
            f'-XMP:ImageCreator={creator_name}'.encode('utf-8'),
            f'-XMP:ImageCreatorImageCreatorName={creator_name}'.encode('utf-8'),
            f'-XMP:CaptionWriter={creator_name}'.encode('utf-8'),
            f'-XMP:Credit={creator_name}'.encode('utf-8'),
            f'-XMP:Rights={creator_name}'.encode('utf-8'),
            f'-XMP:CreatorWorkEmail={creator_name}'.encode('utf-8'),
            f'-XMP:CreatorWorkTelephone={creator_name}'.encode('utf-8'),
            f'-IPTC:By-line={creator_name}'.encode('utf-8'),
            f'-IPTC:Credit={creator_name}'.encode('utf-8'),
            f'-IPTC:Writer-Editor={creator_name}'.encode('utf-8'),
            f'-IPTC:CopyrightNotice={creator_name}'.encode('utf-8'),
            f'-XMP:WebStatement={creator_name}'.encode('utf-8'),
            # f'-XMP:Subject={'ключевое слово 1, ключевое слово 2, ключевое слово 3'}'.encode('utf-8'),
            b'-overwrite_original',
            self.file_path.encode('utf-8')
        ]
        with exiftool.ExifTool() as et:
            et.execute(*commands)

    def write_all_metadate(self, metadata):

        commands = ["-overwrite_original",
                    self.file_path.encode('utf-8')]

        for key, value in metadata[0].items():

            if 'XMP' in key:
                commands.append(f"-{key}={value}")  # Формируем параметры
                logger.info(f"-{key}={value}")

        with exiftool.ExifToolHelper() as et:
            et.execute(*commands)  # Передаём аргументы в exiftool

    def read_tags(self, tags):
        result = {}
        with exiftool.ExifToolHelper() as et:
            for tag in tags:
                logger.info(tag)
                metadata = et.get_tags(self.file_path, tag)
                if metadata and tag in metadata[0]:
                    result[tag] = metadata[0][tag]
                else:
                    result[tag] = None  # Если тег отсутствует
            return result


if __name__ == '__main__':
    _file_path = '/Users/evgeniy/Pictures/2025/06_June/20250619_ПМЭФ/20250619PEV_7187.NEF'
    # _file_path_target = '/Users/evgeniy/_Python/_test_images/20250319 copy.JPG'

    source_image = ImageMetadate(_file_path)
    source_image.write_metadate("Purple")
    saved_metadate = source_image.extract_all_metadate()
    xmp = source_image.extract_xmp()
    for key, value in xmp[0].items():
        logger.info(f"{key}={value}")

    # target_image = ImageMetadate(_file_path_target)
    # # target_image.write_all_metadate(saved_metadate)
    # target_image.write_metadate('Blue')
    # xmp = target_image.extract_xmp()
    # for key, value in xmp[0].items():
    #     logger.info(f"{key}={value}")

    # clear_exif(_file_path)
    # print(image_metadate.read_tags(
    #     tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))
    # image_metadate.clear_exif()
    # image_metadate.write_metadate("Green")
    # print(image_metadate.read_tags(
    #     tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))
    # all_metadata = image_metadate.extract_all_metadate()[0]
    # for k, v in all_metadata.items():
    #     print(k, v)

    # for k, v in xmp.items():
    #     print(k, v)
    # print(type(xmp))

    # xmp = image_metadate.extract_iptc()[0]
    # for k, v in xmp.items():
    #     print(k, v)
    # print(type(xmp))
    # xmp = image_metadate.extract_exif()[0]
    # for k, v in xmp.items():
    #     print(k, v)
    # print(type(xmp))
