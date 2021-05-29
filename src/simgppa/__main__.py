'''Entrypoint to program'''

# use relative imports here
import os
from pathlib import Path

from .img_processing import ImageProcessor

path = os.path.abspath(__file__)
pathlib_path = Path(path).parent.joinpath('banana1-gr.jpg')

imgp = ImageProcessor(pathlib_path, [], [])

res = imgp.get_graph_edges()

print(len(res))
