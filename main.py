from utils import setup_argparse, fix_missing_params
from voronoi import generate_voronoi

def main() -> None:
    args = setup_argparse()
    input_path, output_path, n_regions, padding, pad_color, rounding = fix_missing_params(args)
    generate_voronoi(input_path, output_path, n_regions, padding, pad_color, rounding)

if __name__ == '__main__':
    main()