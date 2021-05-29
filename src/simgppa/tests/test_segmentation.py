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
            bg_pixels=[],
            obj_pixels=[],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana1-gr-320.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana1-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana1-gr-320.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.7)
        self.assertGreater(correct_obj, 0.7)
        self.assertGreater(correct_total, 0.7)
        self.assertGreater(correct_relative, 0.7)

    def test_banana_2(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana2-gr-320.jpg'),
            bg_pixels=[],
            obj_pixels=[],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana2-gr-320.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana2-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana2-gr-320.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.7)
        self.assertGreater(correct_obj, 0.7)
        self.assertGreater(correct_total, 0.7)
        self.assertGreater(correct_relative, 0.7)

    def test_banana_3(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana3-gr-320.jpg'),
            bg_pixels=[],
            obj_pixels=[],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana3-gr-320.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana3-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana3-gr-320.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.7)
        self.assertGreater(correct_obj, 0.7)
        self.assertGreater(correct_total, 0.7)
        self.assertGreater(correct_relative, 0.7)

    def test_banana_1_with_user_data(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana1-gr-320.jpg'),
            bg_pixels=[Pixel(157, 66), Pixel(211, 55), Pixel(
                12, 77), Pixel(277, 221), Pixel(20, 222)],
            obj_pixels=[Pixel(158, 166), Pixel(190, 161), Pixel(
                90, 162), Pixel(36, 126), Pixel(263, 51)],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana1-gr-320_.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana1-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana1-gr-320_.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.5)
        self.assertGreater(correct_obj, 0.5)
        self.assertGreater(correct_total, 0.5)
        self.assertGreater(correct_relative, 0.5)

    def test_banana_2_with_user_data(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana2-gr-320.jpg'),
            bg_pixels=[Pixel(121, 66), Pixel(229, 87), Pixel(
                17, 216), Pixel(19, 36), Pixel(293, 19)],
            obj_pixels=[Pixel(68, 148), Pixel(122, 159), Pixel(
                39, 149), Pixel(253, 162), Pixel(270, 72)],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana2-gr-320_.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana2-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana2-gr-320_.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.5)
        self.assertGreater(correct_obj, 0.5)
        self.assertGreater(correct_total, 0.5)
        self.assertGreater(correct_relative, 0.5)

    def test_banana_3_with_user_data(self):
        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana3-gr-320.jpg'),
            bg_pixels=[Pixel(178, 71), Pixel(237, 68), Pixel(
                288, 42), Pixel(47, 211), Pixel(280, 218)],
            obj_pixels=[Pixel(65, 109), Pixel(204, 175), Pixel(
                205, 177), Pixel(51, 121), Pixel(39, 89)],
            lmbd=100,
            sgm=1.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana3-gr-320_.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana3-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana3-gr-320_.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        self.assertGreater(correct_bg, 0.5)
        self.assertGreater(correct_obj, 0.5)
        self.assertGreater(correct_total, 0.5)
        self.assertGreater(correct_relative, 0.5)
