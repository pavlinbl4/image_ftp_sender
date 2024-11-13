# pip install PyExifTool
import exiftool


def get_image_metadata(file_path,
                      tags ):
    """
        Извлекает значения указанных тегов из изображения.

        :param file_path: Путь к файлу изображения.
        :param tags: Список тегов, которые нужно получить.
        :return: Словарь с тегами и их значениями.
        """
    with exiftool.ExifToolHelper() as et:
        result = {}
        for tag in tags:
            metadata = et.get_tags(file_path, tag)
            if metadata and tag in metadata[0]:
                result[tag] = metadata[0][tag]
            else:
                result[tag] = None  # Если тег отсутствует
        return result


def clear_exif(file_path):
    with exiftool.ExifTool() as et:
        et.execute(b'-all=', b'-XMP:Creator=Photographer_name', file_path.encode())


if __name__ == '__main__':
    print(get_image_metadata('./test_image/20241112PB125826.jpg',
                             tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))
