import math
from collections import namedtuple
from pathlib import Path
from typing import List

from PIL import Image

from .ppa import Edge

Pixel = namedtuple('Pixel', 'x y')


class ImageProcessor():

    def __init__(self,
                 path: str,
                 obj: List[Pixel],
                 bg: List[Pixel],
                 lmbd: float = 100.0,
                 sgm: float = 1.0,
                 bw: bool = True) -> None:

        img_path = Path(path)

        if not img_path.exists():
            raise Exception('Invalid path to image file')

        with Image.open(img_path) as file:

            self.__img = file.load()
            self.img_height = file.height
            self.img_width = file.width

        self.__lambda = lmbd
        self.__sigma = sgm
        self.__bw = bw

        self.__raw_obj_pixels = obj
        self.__raw_bg_pixels = bg
        self.__object_pixels = [self.__img[pixel.x, pixel.y] for pixel in obj]
        self.__background_pixels = [
            self.__img[pixel.x, pixel.y] for pixel in bg]
        self.__edges: List[Edge] = []
        self.__runoff = self.img_height * self.img_width + 1
        self.__max_out_flow = None

    def __get_pixel_index(self, pixel: Pixel) -> int:
        return self.img_width * pixel.y + pixel.x

    def __edge_weight(self, pixel1: Pixel, pixel2: Pixel) -> int:
        k = 100
        px1 = self.__img[pixel1.x, pixel1.y]
        px2 = self.__img[pixel2.x, pixel2.y]

        dt = (abs(px1 - px2) ** 2) if self.__bw else \
            abs(px1[0] - px2[0]) ** 2 + \
            abs(px1[1] - px2[1]) ** 2 + \
            abs(px1[2] - px2[2]) ** 2

        return int(k * math.exp(-dt / (2 * self.__sigma ** 2)))

    def __get_obj_distr(self, max_flow: float):

        pixels_number: int = len(self.__object_pixels)
        groups_number: int = 51

        groups: List[int] = [0 for i in range(groups_number)]
        k: float = groups_number / 256

        for intensity in self.__object_pixels:
            groups[math.floor(intensity * k)] += 1

        for i in range(groups_number):
            if groups[i] != 0:
                groups[i] = - \
                    self.__lambda * math.log(groups[i] / pixels_number)
            else:
                groups[i] = max_flow

        def distribution(intensity: int, groups: List[int], k: int) -> int:

            scaled_intensity: int = math.floor(intensity * k)
            return groups[scaled_intensity]

        return lambda x: distribution(x, groups, k)

    def __get_bg_distr(self, max_flow: float):

        pixels_number: int = len(self.__background_pixels)
        groups_number: int = 51

        groups: List[int] = [0 for i in range(groups_number)]
        k: float = groups_number / 256

        for intensity in self.__background_pixels:
            groups[math.floor(intensity * k)] += 1

        for i in range(groups_number):
            if groups[i] != 0:
                groups[i] = - \
                    self.__lambda * math.log(groups[i] / pixels_number)
            else:
                groups[i] = max_flow

        def distribution(intensity: int, groups: List[int], k: int) -> int:

            scaled_intensity: int = math.floor(intensity * k)
            return groups[scaled_intensity]

        return lambda x: distribution(x, groups, k)

    def __get_edges_for_pixel(self, pixel: Pixel) -> List[Edge]:

        idx = self.__get_pixel_index(pixel)
        on_right, on_left, on_top, on_bottom = pixel.x == \
            self.img_width - 1, \
            pixel.x == 0, \
            pixel.y == 0, \
            pixel.y == self.img_height - 1

        edges = []

        rpixel = Pixel(x=pixel.x + 1, y=pixel.y)
        bpixel = Pixel(x=pixel.x, y=pixel.y + 1)
        lpixel = Pixel(x=pixel.x - 1, y=pixel.y)
        tpixel = Pixel(x=pixel.x, y=pixel.y - 1)

        ridx = self.__get_pixel_index(rpixel)
        bidx = self.__get_pixel_index(bpixel)
        lidx = self.__get_pixel_index(lpixel)
        tidx = self.__get_pixel_index(tpixel)

        if not on_right:
            edges.append(
                Edge(idx + 1, ridx + 1, self.__edge_weight(pixel, rpixel)))

        if not on_left:
            edges.append(
                Edge(idx + 1, lidx + 1, self.__edge_weight(pixel, lpixel)))

        if not on_bottom:
            edges.append(
                Edge(idx + 1, bidx + 1, self.__edge_weight(pixel, bpixel)))

        if not on_top:
            edges.append(
                Edge(idx + 1, tidx + 1, self.__edge_weight(pixel, tpixel)))

        edges.append(Edge(0, idx + 1, 0))
        edges.append(Edge(idx + 1, self.__runoff, 0))

        return edges

    def get_max_out_flow(self) -> float:
        if self.__max_out_flow:
            return self.__max_out_flow

        flow = [0] * (self.img_width * self.img_height + 1)

        for edge in self.__edges:
            flow[edge.start - 1] += edge.capacity
        return max(flow) + 1.0

    def __get_index_pixel(self, idx: int):
        y = int(idx / self.img_width)
        x = idx - self.img_width * y

        return Pixel(x, y)

    def get_graph_edges(self):

        if len(self.__edges) > 0:
            return self.__edges

        # add edges between pixels
        for h in range(self.img_height):
            for w in range(self.img_width):

                pixel: Pixel = Pixel(x=w, y=h)

                self.__edges += self.__get_edges_for_pixel(pixel)

        self.__max_out_flow = self.get_max_out_flow()

        obj_hist_distr = self.__get_obj_distr(self.__max_out_flow)
        bg_hist_distr = self.__get_bg_distr(self.__max_out_flow)

        # fill in capacities for edges from source
        for edge in [e for e in self.__edges if e.start == 0]:
            pixel = self.__get_index_pixel(edge.end - 1)

            if pixel in self.__raw_obj_pixels:
                edge.capacity = self.__max_out_flow

            elif pixel in self.__raw_bg_pixels:
                edge.capacity = 0

            else:
                edge.capacity = bg_hist_distr(self.__img[pixel.x, pixel.y])

        # fill in capacities for edges from source
        for edge in [e for e in self.__edges if e.end == self.__runoff]:
            pixel = self.__get_index_pixel(edge.start - 1)

            if pixel in self.__raw_obj_pixels:
                edge.capacity = 0

            elif pixel in self.__raw_bg_pixels:
                edge.capacity = self.__max_out_flow

            else:
                edge.capacity = obj_hist_distr(self.__img[pixel.x, pixel.y])

        return self.__edges

    def get_pixel_count(self):
        return self.img_width * self.img_height
