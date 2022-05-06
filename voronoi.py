import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, path
from scipy.spatial import Voronoi
import cv2
from tqdm import tqdm

from utils import flip_and_resize, setup_plot

def shrink(polygon : np.ndarray, pad : float) -> np.ndarray:
    '''Returns the shrinked polygon by applying the specified pad'''

    center = np.mean(polygon, axis=0)
    resized = np.zeros_like(polygon)

    # reduce distance from the region center
    for i, point in enumerate(polygon):
        vector = point - center
        unit_vector = vector / np.linalg.norm(vector)
        resized[i] = point - pad * unit_vector

    return resized


class RoundedPolygon(patches.PathPatch):

    def __init__(self, xy : np.ndarray, pad : float, **kwargs):
        p = path.Path(*self.__round(xy=xy, pad=pad))
        super().__init__(path=p, **kwargs)

    def __round(self, xy : np.ndarray, pad : float):
        n = len(xy)

        for i in range(0, n):

            x0, x1, x2 = np.atleast_1d(xy[i - 1], xy[i], xy[(i + 1) % n])

            d01, d12 = x1 - x0, x2 - x1
            l01, l12 = np.linalg.norm(d01), np.linalg.norm(d12)
            u01, u12 = d01 / l01, d12 / l12

            x00 = x0 + min(pad, 0.5 * l01) * u01
            x01 = x1 - min(pad, 0.5 * l01) * u01
            x10 = x1 + min(pad, 0.5 * l12) * u12

            if i == 0:
                verts = [x00, x01, x1, x10]
            else:
                verts += [x01, x1, x10]

        codes = [path.Path.MOVETO] + n*[path.Path.LINETO, path.Path.CURVE3, path.Path.CURVE3]

        verts[0] = verts[-1]

        return np.atleast_1d(verts, codes)


def generate_voronoi(img_path : str, output_path : str, n : int, pad_amount : float, pad_color : str, rounding_amount : float) -> None:
    '''Generates Voronoi picture with specified parameters'''

    # load image via opencv and fix color channels
    img = cv2.imread(img_path)
    img = img[:, :, [2, 1, 0]]

    # image dimentions
    max_y = img.shape[0]
    max_x = img.shape[1]

    # points of the region centroids
    points = np.c_[np.random.randint(0, max_x, size=n),
                np.random.randint(0, max_y, size=n)]

    # add 4 distant dummy points
    points = np.append(points, [[2 * max_x, 2 * max_y],
                                [   -max_x, 2 * max_y],
                                [2 * max_x,    -max_y],
                                [   -max_x,    -max_y]], axis = 0)

    # compute Voronoi tesselation
    vor = Voronoi(points)

    ax = setup_plot(max_x, max_y, pad_color)

    # for each voronoi region, apply specified padding and rounding
    for region in tqdm(vor.regions, unit='regions'):
        if region and (not -1 in region):

            # get polygon vertices and shrink based on them
            polygon = np.array([vor.vertices[i] for i in region])
            resized = shrink(polygon, pad_amount)

            # compute x and y of pixel to pick color from
            x, y = np.mean(polygon, axis=0).astype(int)
            # minding of the border limitations
            x = max(0, min(x, max_x - 1))
            y = max(0, min(y, max_y - 1))
            color = img[y, x] / 255

            ax.add_patch(RoundedPolygon(resized, rounding_amount, color=color))

                
    print('FINISHING TOUCHES...')
    
    # save partial result
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

    # fix the partial result: flip and resize the output of savefig
    flip_and_resize(output_path, max_x, max_y)