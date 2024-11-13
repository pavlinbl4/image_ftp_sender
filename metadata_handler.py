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
        # Удаляем только EXIF данные и обновляем XMP:Creator
        creator_name = "Семен Лиходеев"
        et.execute(
            b'-EXIF:all=',
            f'-XMP:Creator={creator_name}'.encode('utf-8'),
            b'-overwrite_original',
            file_path.encode('utf-8')
        )


if __name__ == '__main__':
    file_path = './test_image/20241109PEV_8316.JPG'
    clear_exif(file_path)
    print(get_image_metadata(file_path,
                             tags=['XMP:Description', 'XMP:Label', 'XMP:Creator']))
