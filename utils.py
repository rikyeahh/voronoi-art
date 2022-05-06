import argparse
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

def setup_argparse() -> argparse.Namespace:
    '''Sets up and uses argument parsing, returns argument'''

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
    # rounding of regions argument
    parser.add_argument('--round',
                    type=float,
                    required=False, 
                    help='Rounding/smoothing amount for each Voronoi region')
    # get/parse arguments
    args = parser.parse_args()
    return args

def flip_and_resize(img_path : str, x : int, y : int) -> None:
    '''Flips vertically and resized the image in the specified path'''

    # load and resize
    img = Image.open(img_path)
    img = img.resize((x, y))
    # flip and save
    img = ImageOps.flip(img)
    img.save(img_path)


def setup_plot(x : int, y : int):
    '''Sets up matplotlib print canvas and returns it'''

    _, ax = plt.subplots()
    ax.axis([0, x, 0, y])
    ax.axis('off')
    ax.set_facecolor('black')
    ax.add_artist(ax.patch)
    ax.patch.set_zorder(-1)
    return ax