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
            # Define a maximum depth threshold
            max_depth_threshold = 100  # in meters

            # Clip the depth values at the threshold
            depth_df_clipped = self.depth_df.clip(upper=max_depth_threshold)
            depth_df_clipped.fillna(0, inplace=True)

            # Normalize the clipped values
            flattened_data = depth_df_clipped.values.flatten()

            # Calculate the 25th and 75th percentiles (which correspond to Q1 and Q3)
            Q1 = np.percentile(flattened_data, 25)
            Q3 = np.percentile(flattened_data, 75)
            IQR = Q3 - Q1

            # Calculate lower and upper bounds for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Filter out the outliers
            flattened_data[(flattened_data < lower_bound) | (flattened_data > upper_bound)] = 0

            # Normalize the data without outliers
            scaled_data = (flattened_data - flattened_data.min()) / (flattened_data.max() - flattened_data.min())

            # Reshape the data back to the original DataFrame shape
            normalized_depth = pd.DataFrame(scaled_data.reshape(depth_df_clipped.shape), columns=depth_df_clipped.columns)

            cmap = plt.get_cmap('coolwarm_r')

            colored_image = Image.new('RGB', left_image.size)

            for (row_index, col_index), depth in np.ndenumerate(normalized_depth):
                original_color = np.array(left_image.getpixel((col_index, row_index)))
                if depth != 0:
                    tint_color = np.array([int(255 * c) for c in cmap(depth)[:3]])
                    blended_color = (0.2 * original_color + 0.8 * tint_color).astype(int)
                else:
                    blended_color = original_color

                colored_image.putpixel((col_index, row_index), tuple(blended_color))

            colored_image.save('test.png')