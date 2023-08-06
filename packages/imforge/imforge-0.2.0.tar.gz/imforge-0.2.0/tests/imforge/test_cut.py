from io import BytesIO

import cv2
from PIL import Image

from imforge.cut import cut_out_pil, cut_out_cv2, cut_out


class TestCutoutPil:

    DEBUG = False

    def test_cut_out_one_polygon_no_fill_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "pil" / "cut_out_one_polygon_no_fill_color.png"
        polygon = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cut_out_pil(image, polygon)
            if self.DEBUG:
                image.show()
                if not expected_result.exists():
                    image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_cut_out_no_polygon(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "pil" / "cut_out_no_polygon.png"
        with Image.open(resources / "some_text.jpg") as image:
            cut_out_pil(image)
            if self.DEBUG:
                image.show()
                if not expected_result.exists():
                    image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_cut_out_multi_polygon_and_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "pil" / "cut_out_muti_polygon_and_color.png"
        polygons = (
            [(15, 8), (368, 78), (325, 161), (14, 71)],
            [(100, 0), (150, 0), (125, 20)],
            [(0, 150), (200, 150), (200, 178), (0, 178)],
        )
        with Image.open(resources / "some_text.jpg") as image:
            cut_out_pil(image, *polygons, fillcolor=(255, 0, 255))
            if self.DEBUG:
                image.show()
                if not expected_result.exists():
                    image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_generic_cut_out_multi_polygon_and_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "pil" / "cut_out_muti_polygon_and_color.png"
        polygons = (
            [(15, 8), (368, 78), (325, 161), (14, 71)],
            [(100, 0), (150, 0), (125, 20)],
            [(0, 150), (200, 150), (200, 178), (0, 178)],
        )
        with Image.open(resources / "some_text.jpg") as image:
            cut_out(image, *polygons, fillcolor=(255, 0, 255))
            if self.DEBUG:
                image.show()
                if not expected_result.exists():
                    image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()


class TestCutoutCv2:

    DEBUG = False

    def test_cut_out_one_polygon_no_fill_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "cv2" / "cut_out_one_polygon_no_fill_color.png"
        polygon = [(15, 8), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cut_out_cv2(image, polygon)
        # Use PIL image for saving and comparison of result
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            image.show()
            if not expected_result.exists():
                image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_cut_out_no_polygon(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "cv2" / "cut_out_no_polygon.png"
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cut_out_cv2(image)
        # Use PIL image for saving and comparison of result
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            image.show()
            if not expected_result.exists():
                image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_cut_out_multi_polygon_and_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "cv2" / "cut_out_muti_polygon_and_color.png"
        polygons = (
            [(15, 8), (368, 78), (325, 161), (14, 71)],
            [(100, 0), (150, 0), (125, 20)],
            [(0, 150), (200, 150), (200, 178), (0, 178)],
        )
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cut_out_cv2(image, *polygons, fillcolor=(255, 0, 255))
        # Use PIL image for saving and comparison of result
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            image.show()
            if not expected_result.exists():
                image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_generic_out_multi_polygon_and_color(self, resources):
        expected_result = resources / "imforge" / "cut" / "expected" / "cv2" / "cut_out_muti_polygon_and_color.png"
        polygons = (
            [(15, 8), (368, 78), (325, 161), (14, 71)],
            [(100, 0), (150, 0), (125, 20)],
            [(0, 150), (200, 150), (200, 178), (0, 178)],
        )
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cut_out(image, *polygons, fillcolor=(255, 0, 255))
        # Use PIL image for saving and comparison of result
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            image.show()
            if not expected_result.exists():
                image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()
