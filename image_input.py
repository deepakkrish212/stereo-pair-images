from PIL import Image
import os


class ImageInput:
    def __init__(self, left_image, right_image) -> None:
        self.left_image = left_image
        self.right_image = right_image

    def validate(self):
        self.validate_format()
        self.validate_size()

    def validate_format(self):
        left_format = self.extract_format(self.left_image)
        right_format = self.extract_format(self.right_image)
        if left_format != right_format:
            raise TypeError(
                "Format Error: Left format ({0}) and Right format({1}) does not match.".format(
                    left_format, right_format
                )
            )
    
    def validate_size(self):
        left_file_size = os.path.getsize(self.left_image)/1000
        right_file_size = os.path.getsize(self.right_image)/1000
        
        error_message = []

        if left_file_size > 100_000:
            error_message.append("Left image size about 100MB")
        if right_file_size > 100_000:
            error_message.append("Right image size about 100MB")

        if error_message:
            raise Exception("\n".join(error_message))

    def extract_format(self, image_path):
        with Image.open(image_path) as img:
            return img.format
