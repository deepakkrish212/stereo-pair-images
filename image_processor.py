from PIL import Image
import pandas as pd

class ImagePreProcessor:
    def __init__(self, left_image, right_image) -> None:
        self.left_image = left_image
        self.right_image = right_image

    def seperate_RGB_components(self):
        self.left_image = self.get_image_rgb(self.left_image)
        self.right_image = self.get_image_rgb(self.right_image)


    def get_image_rgb(self, image_path):
        with Image.open(image_path) as img:
            rgb_value = list(img.getdata())
            width, height = img.size
            grid_data = []
            for i in range(height):
                grid_data.append(rgb_value[i*width : (i+1)*width])

            df = pd.DataFrame(grid_data)

            return df