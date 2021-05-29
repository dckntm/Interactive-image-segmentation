from typing import List

from PIL import Image

from .ppa import PPA
from .img_processing import ImageProcessor, Pixel


class Segmentation:

    def __init__(self,
                 input_path: str,
                 bg_pixels: List[Pixel],
                 obj_pixels: List[Pixel],
                 lmbd: int,
                 sgm: float,
                 bw: bool) -> None:

        print('Initalizing Segmentation...')

        self.__img_processor = ImageProcessor(
            input_path, obj_pixels, bg_pixels, lmbd, sgm, bw)

        self.__edges = self.__img_processor.get_graph_edges()
        # self.__max_out_flow = self.__img_processor.get_max_out_flow()
        self.__pixels_count = self.__img_processor.get_pixel_count()

        self.__ppa = PPA(self.__pixels_count + 2, self.__edges)

        # self.__maxflow = self.__ppa.maxflow()
        self.__mincut = self.__ppa.min_cut()
        # self.__flow = self.__ppa.flow()

        h = self.__img_processor.img_height
        w = self.__img_processor.img_width

        self.__image = Image.new("1", (w, h))

        for i in self.__mincut:
            self.__image.putpixel(((i - 1) % w, (i - 1) // w), 1)

    def save_img(self, output: str) -> None:

        self.__image.save(output)
