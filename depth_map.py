from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


class DepthMap:
    def __init__(self, disparity: pd.DataFrame, focal_length, baseline) -> None:
        self.disparity = disparity
        self.focal_length = focal_length
        self.baseline = baseline

    def calculate_depth(self):
        self.disparity.replace(0, np.nan, inplace=True)
        
        self.depth_df = (self.focal_length * self.baseline)/ self.disparity

    def colorize(self, left_image_path):
        with Image.open(left_image_path) as left_image:
            normalized_depth = (self.depth_df - self.depth_df.min())/ (self.depth_df.max() - self.depth_df.min())
            cmap = plt.get_cmap('coolwarm')

            colored_image = Image.new('RGB', left_image.size)

            for (row_index, col_index), depth in np.ndenumerate(normalized_depth):
                if not np.isnan(depth):
                    color = cmap(depth)[:3]
                    color = tuple(int(255 * c) for c in color)
                else:
                    color = left_image.getpixel((col_index, row_index))

                colored_image.putpixel((col_index, row_index), color)

            colored_image.save('test.png')