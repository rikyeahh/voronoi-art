from utils import setup_argparse
from voronoi import fix_missing_params, generate_voronoi

def main() -> None:
    args = setup_argparse()
    input_path, output_path, n_regions, padding, rounding = fix_missing_params(args.i, args.o, args.n, args.pad, args.round)
    generate_voronoi(input_path, output_path, n_regions, padding, rounding)

if __name__ == '__main__':
    main()