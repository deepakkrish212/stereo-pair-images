import pandas as pd
import numpy as np


class ValidateDepth:
    def __init__(self, generated_depth: pd.DataFrame, true_depth_path) -> None:
        self.generated_depth = generated_depth
        self.true_depth = pd.read_csv(true_depth_path)

    def validate(self):
        assert (
            self.generated_depth.shape == self.true_depth.shape
        ), "Depth maps are not the same size"
        
        # Fill nan if any
        self.generated_depth.fillna(0, inplace=True)
        self.true_depth.fillna(0, inplace=True)

        diff = np.abs(self.generated_depth.values - self.true_depth.values)

        # Calculate Mean Absolute Error (MAE)
        mae = np.mean(diff)

        # Calculate Root Mean Squared Error
        rmse = np.sqrt(np.mean(diff*2))

        print(f"MAE: {mae}")
        print(f"RMSE: {rmse}")
