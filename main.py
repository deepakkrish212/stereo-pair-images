import argparse
from depth_map import DepthMap
from disparity_estimator import DisparityEstimator
from image_input import ImageInput

from image_processor import ImagePreProcessor

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--left', type=str, help='The Path of left stero image')
    parser.add_argument('--right', type=str, help='The Path of right stero image')
    return parser.parse_args()

def main():
    args = parse_args()
    image_input = ImageInput(left_image=args.left, right_image=args.right)
    image_input.validate()

    processor = ImagePreProcessor(left_image=args.left, right_image=args.right)
    processor.seperate_RGB_components()

    estimator = DisparityEstimator(processor.left_image, processor.right_image, 0.6)
    estimator.match_pixels()
    
    map = DepthMap(estimator.disparity, 645.24, 0.6)

    map.calculate_depth()
    map.colorize(args.left)


if __name__ == "__main__":
    main()