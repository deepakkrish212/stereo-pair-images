import pandas as pd
import numpy as np


class DisparityEstimator:
    def __init__(
        self, left_image: pd.DataFrame, right_image: pd.DataFrame) -> None:
        self.left_image = left_image.values
        self.right_image = right_image.values
        self.height, self.width = left_image.shape

    def match_pixels(self, tolerance):
        tolerance_value = tolerance * 255 / 100
        self.disparity = np.zeros((self.height, self.width))
        block_size = 2

        for row_index in range(0, self.height - block_size + 1, block_size):
            for left_col_index in range(0, self.width - block_size + 1, block_size):
                # Get the 3x3 block from the left image
                left_block = self.left_image[
                    row_index : row_index + block_size,
                    left_col_index : left_col_index + block_size
                ].flatten()
                best_match_col = None
                min_sad = float('inf')

                for right_col_index in range(0, self.width - block_size + 1, block_size):
                    # Get the 3x3 block from the right image
                    right_block = self.right_image[
                        row_index : row_index + block_size,
                        right_col_index : right_col_index + block_size
                    ].flatten()

                     # Calculate SAD
                    total_sad = np.sum(np.abs(np.array([tuple(np.array(a) - np.array(b)) for a, b in zip(left_block, right_block)])))

                    if total_sad <= tolerance_value and total_sad < min_sad:
                        min_sad = total_sad
                        best_match_col = right_col_index

                if best_match_col is not None:
                    disparity_value = self.calcualte_disparity(left_col_index, best_match_col)
                    # Assign disparity to the central pixel of the block
                    self.disparity[
                        row_index : row_index + block_size,
                        left_col_index : left_col_index + block_size
                    ] = disparity_value
        
        self.disparity = pd.DataFrame(self.disparity)

        

    def calcualte_disparity(self, left_index, right_index):
        return abs(left_index - right_index)
