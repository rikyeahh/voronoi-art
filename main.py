import cv2

from utils import setup_argparse, fix_missing_params
from voronoi import generate_voronoi

def main() -> None:
    args = setup_argparse()
    input_path, output_path, n_regions, padding, pad_color, rounding = fix_missing_params(args)
    result = generate_voronoi(input_path, n_regions, padding, pad_color, rounding)
    cv2.imwrite(output_path, result)

if __name__ == '__main__':
    main()