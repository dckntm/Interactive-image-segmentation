import os
import sys
import unittest
from pathlib import Path

from PIL import Image
from simgppa.img_processing import Pixel
from simgppa.metrics import compare
from simgppa.segmentation import Segmentation

path = Path(os.path.abspath(__file__)).parent


class Test_Segmentation(unittest.TestCase):

    def test_banana_1(self):
        bg_pixels = []
        obj_pixels = []

        with open(os.path.join(sys.path[0], "simgppa/tests/obj_pixels.txt"), 'r') as b:
            data = b.read().splitlines()
        for pixel in data:
            x, y = pixel.split()
            obj_pixels.append(Pixel(int(x), int(y)))

        with open(os.path.join(sys.path[0], "simgppa/tests/bg_pixels.txt"), 'r') as b:
            data = b.read().splitlines()
        for pixel in data:
            x, y = pixel.split()
            bg_pixels.append(Pixel(int(x), int(y)))

        s = Segmentation(path.joinpath(
            'data/segmentation/images-320/banana1-gr-320.jpg'),
            bg_pixels=bg_pixels,
            obj_pixels=obj_pixels,
            lmbd=1,
            sgm=60.0,
            bw=True)

        s.save_img(path.joinpath(
            'data/segmentation/output/banana1-320.jpg'))

        reference = Image.open(path.joinpath(
            'data/segmentation/image-segments-320/banana1-320.jpg'
        ))

        output = Image.open(path.joinpath(
            'data/segmentation/output/banana1-320.jpg'))

        correct_obj, correct_bg, correct_total, correct_relative = compare(
            reference=reference, output=output)

        print('correct_bg ', correct_bg)
        print('correct_obj ', correct_obj)
        print('correct_total ', correct_total)
        print('correct_relative ', correct_relative)

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
            bg_pixels=[
                # Pixel(157, 66), Pixel(211, 55), Pixel(
                # 12, 77), Pixel(277, 221), Pixel(20, 222)
                Pixel(209, 96),
            Pixel(207, 95),
            Pixel(165, 80),
            Pixel(161, 77),
            Pixel(150, 68),
            Pixel(145, 65),
            Pixel(140, 65),
            Pixel(128, 59),
            Pixel(127, 58),
            Pixel(121, 56),
            Pixel(117, 54),
            Pixel(117, 54),
            Pixel(112, 52),
            Pixel(109, 50),
            Pixel(104, 49),
            Pixel(100, 47),
            Pixel(93, 45),
            Pixel(77, 38),
            Pixel(62, 40),
            Pixel(62, 40),
            Pixel(55, 46),
            Pixel(45, 58),
            Pixel(41, 61),
            Pixel(33, 63),
            Pixel(26, 54),
            Pixel(24, 49),
            Pixel(24, 45),
            Pixel(22, 32),
            Pixel(21, 26),
            Pixel(23, 20),
            Pixel(65, 22),
            Pixel(71, 19),
            Pixel(70, 19),
            Pixel(153, 5),
            Pixel(152, 5),
            Pixel(163, 9),
            Pixel(191, 15),
            Pixel(211, 8),
            Pixel(223, 27),
            Pixel(222, 37),
            Pixel(201, 61),
            Pixel(161, 82),
            Pixel(131, 99),
            Pixel(121, 102),
            Pixel(102, 99),
            Pixel(74, 96),
            Pixel(67, 93),
            Pixel(62, 92),
            Pixel(50, 86),
            Pixel(27, 88),
            Pixel(13, 94),
            Pixel(14, 95),
            Pixel(2, 117),
            Pixel(8, 137),
            Pixel(15, 149),
            Pixel(22, 171),
            Pixel(26, 183),
            Pixel(31, 193),
            Pixel(47, 209),
            Pixel(64, 210),
            Pixel(80, 218),
            Pixel(94, 222),
            Pixel(125, 227),
            Pixel(137, 227),
            Pixel(152, 228),
            Pixel(160, 228),
            Pixel(183, 225),
            Pixel(197, 223),
            Pixel(210, 224),
            Pixel(224, 223),
            Pixel(242, 219),
            Pixel(253, 217),
            Pixel(260, 210),
            Pixel(271, 198),
            Pixel(289, 176),
            Pixel(300, 169),
            Pixel(314, 163),
            Pixel(307, 195),
            Pixel(305, 207),
            Pixel(290, 224),
            Pixel(284, 222),
            Pixel(284, 222),
        ],
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
