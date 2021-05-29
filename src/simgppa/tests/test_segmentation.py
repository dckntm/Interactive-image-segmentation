import os
from pathlib import Path
import unittest

from PIL import Image
from simgppa.img_processing import Pixel

from simgppa.segmentation import Segmentation
from simgppa.metrics import compare
path = Path(os.path.abspath(__file__)).parent


class Test_Segmentation(unittest.TestCase):

    def test_banana_1(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana1-gr-320.jpg'),
            bg_pixels=[Pixel(0, 0)],
            obj_pixels=[Pixel(280, 120)],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana1-gr-320.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana1-gr.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana1-gr-320.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.7)
        self.assertGreater(correct_obj, 0.7)
        self.assertGreater(correct_total, 0.7)
        self.assertGreater(correct_relative, 0.7)
