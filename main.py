import argparse
from depth_map import DepthMap
from disparity_estimator import DisparityEstimator
from image_input import ImageInput

from image_processor import ImagePreProcessor
from validate_depth import ValidateDepth

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--left', type=str, help='The Path of left stero image', required=True)
    parser.add_argument('-r', '--right', type=str, help='The Path of right stero image', required=True)
    parser.add_argument('-b','--baseline', type=float, help='The baseline of the stereo image', required=True)
    parser.add_argument('-f','--focal', type=float, help='The focal-length of the stereo image in pixels', required=True)
    parser.add_argument('-d', '--depth', type=str, help='The Path of the depth image (only required for validation)', required=False)
    parser.add_argument('--validate', action='store_true', help='Validate the depth map')
    parser.add_argument('--execute', action='store_true', help='Execute the disparity and depth map processing')
    return parser.parse_args()

def main():
    args = parse_args()

    if args.execute or args.validate:
        if args.validate and not args.depth:
                raise ValueError("Depth image path is required for validation")

        image_input = ImageInput(left_image=args.left, right_image=args.right)
        image_input.validate()

        processor = ImagePreProcessor(left_image=args.left, right_image=args.right)
        processor.seperate_RGB_components()

        estimator = DisparityEstimator(processor.left_image, processor.right_image)
        estimator.match_pixels(20) # 10 percent tolerance
        
        map = DepthMap(estimator.disparity, args.focal, args.baseline)

        map.calculate_depth()

        if args.execute:
            map.colorize(args.left)
    
        elif args.validate:
            # Perform validation
            validator = ValidateDepth(map.depth_df, args.depth)
            validator.validate()

    else:
        print("No action specified. Use --validate or --execute.")


if __name__ == "__main__":
    main()