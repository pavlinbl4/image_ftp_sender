import exiftool

def copy_metadata(source_image, target_image):
    with exiftool.ExifTool() as et:
        et.execute("-overwrite_original", "-charset", "UTF8", "-tagsFromFile",source_image, target_image)

