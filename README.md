# voronoi-art

Command-line-tool to generate customizable Voronoi art from any image.

![Voronoi regions art on color gradient](imgs/presentation.png "Example 1")
![Voronoi regions art on japanese text](imgs/presentation_jap.png "Example 2")

## GUI:
![GUI of the program](imgs/GUI.png "GUI of the program")

## USAGE:

    python3 gui.py

or for command-line execution:

    python3 main.py [-h] [--i I] [--o O] [--n N] [--pad PAD] [--pcolor PCOLOR] [--round ROUND]

optional arguments:

-h, --help     show this help message and exit

--i I          Input file name on which to pick colors from

--o O          Output file name

--n N          Number of Voronoi regions

--pad PAD      Padding amount for each Voronoi region

--pcolor PCOLOR  Padding color in-between Voronoi regions (in hex #RRGGBB)

--round ROUND  Rounding/smoothing amount for each Voronoi region
