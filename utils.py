import argparse
import matplotlib.pyplot as plt
import re
import imagesize
import os

def setup_argparse() -> argparse.Namespace:
    '''Sets up and uses argument parsing, returns argument'''

    # define type to validate RGB values in hexadecimal
    def color_type(arg_value, pat=re.compile(r"^#[a-f0-9A-F]{6}$")):
        if not pat.match(arg_value):
            raise argparse.ArgumentTypeError
        return arg_value

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Generate Voronoi art')
    # input filename argument
    parser.add_argument('--i',
                    type=str,
                    required=False,
                    default='imgs/gradient.png',
                    help='Input file name on which to pick colors from')
    # output filename argument
    parser.add_argument('--o',
                    type=str, 
                    required=False,
                    help='Output file name')
    # number of voronoi regions argument
    parser.add_argument('--n',
                    type=int,
                    required=False, 
                    help='Number of Voronoi regions')
    # padding of voronoi regions argument
    parser.add_argument('--pad',
                    type=float,
                    required=False, 
                    help='Padding amount for each Voronoi region')
    parser.add_argument('--pcolor',
                    type=color_type,
                    required=False,
                    default="#000000",
                    help='Padding color in-between Voronoi regions (in hex #RRGGBB)')
    # rounding of regions argument
    parser.add_argument('--round',
                    type=float,
                    required=False, 
                    help='Rounding/smoothing amount for each Voronoi region')
    # get/parse arguments
    args = parser.parse_args()
    return args

def fix_missing_params(args) -> tuple[str, str, int, float, str, float]:
    '''Computes and returns appropriate default values if they are not specified'''

    # extract parameters from args
    input_path = args.i
    output_path = args.o
    n_regions = args.n
    pad = args.pad
    pcolor = args.pcolor
    round = args.round

    # get image size
    x, y = imagesize.get(input_path)

    # if not specified, output filename is "inputfilename_out.***"
    if output_path is None:
        input_basename, extension = os.path.splitext(input_path)
        output_path =  input_basename + '_out' + extension
    
    # compute default number of regions
    if n_regions is None:
       n_regions = int(max(x, y) / 10)

    # compute default region padding
    if pad is None:
        pad = max(x, y) / 200
    
    # compute default region rounding
    if round is None:
        round = max(x, y) / 150

    return input_path, output_path, n_regions, pad, pcolor, round

def setup_plot(x : int, y : int, pad_color : str):
    '''Sets up matplotlib paint axes and returns it'''

    _, ax = plt.subplots(figsize=(x / 100, y / 100))
    ax.axis([0, x, 0, y])
    ax.axis('off')
    ax.set_facecolor(pad_color)
    ax.add_artist(ax.patch)
    ax.patch.set_zorder(-1)

    # setup ax size in pixels
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(x / 100) / (r - l)
    figh = float(y / 100) / (t - b)
    ax.figure.set_size_inches(figw, figh)

    return ax