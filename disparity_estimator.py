import pandas as pd
import numpy as np


class DisparityEstimator:
    def __init__(
        self, left_image: pd.DataFrame, right_image: pd.DataFrame, baseline
    ) -> None:
        self.left_image = left_image
        self.right_image = right_image
        self.baseline = baseline

    def match_pixels(self):
        self.disparity = pd.DataFrame(
            np.zeros(self.left_image.shape), columns=range(self.left_image.shape[1])
        )

        for row_index in range(self.left_image.shape[0]):
            left_row = self.left_image.iloc[row_index]
            right_row = self.right_image.iloc[row_index]

            for left_col_index, left_pixel in enumerate(left_row):
                for right_col_index, right_pixel in enumerate(right_row):
                    if left_pixel == right_pixel:
                        self.disparity.iloc[
                            row_index, left_col_index
                        ] = self.calcualte_disparity(left_col_index, right_col_index)

        

    def calcualte_disparity(self, left_index, right_index):
        return abs(left_index - right_index) / self.baseline
