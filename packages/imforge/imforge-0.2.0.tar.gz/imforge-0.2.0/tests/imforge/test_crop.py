from io import BytesIO

# noinspection PyPackageRequirements
import cv2
from PIL import Image, ImageDraw

from imforge.crop import crop_pil, crop_cv2, crop


class TestCropPil:

    DEBUG = False

    def test_full_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_1.png"
        crop_box = [(0, 0), (389, 0), (389, 177), (0, 177)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_2.png"
        crop_box = [(389, 0), (389, 177), (0, 177), (0, 0)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_3.png"
        crop_box = [(389, 177), (0, 177), (0, 0), (389, 0)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_4.png"
        crop_box = [(0, 177), (0, 0), (389, 0), (389, 177)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_flip_1.png"
        crop_box = [(0, 0), (0, 177), (389, 177), (389, 0)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_flip_2.png"
        crop_box = [(389, 0), (0, 0), (0, 177), (389, 177)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_flip_3.png"
        crop_box = [(389, 177), (389, 0), (0, 0), (0, 177)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_flip_4.png"
        crop_box = [(0, 177), (389, 177), (389, 0), (0, 0)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_out(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_out.png"
        crop_box = [(-10, -10), (400, -10), (400, 200), (-10, 200)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "full_clip.png"
        crop_box = [(-10, -10), (400, -10), (400, 200), (-10, 200)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_1.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_2.png"
        crop_box = [(368, 78), (325, 161), (14, 71), (15, 8)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_3.png"
        crop_box = [(325, 161), (14, 71), (15, 8), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_4.png"
        crop_box = [(14, 71), (15, 8), (368, 78), (325, 161)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_1.png"
        crop_box = [(15, 8), (14, 71), (325, 161), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_2.png"
        crop_box = [(368, 78), (15, 8), (14, 71), (325, 161)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_3.png"
        crop_box = [(325, 161), (368, 78), (15, 8), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_4.png"
        crop_box = [(14, 71), (325, 161), (368, 78), (15, 8)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, fillcolor=(255, 0, 255))
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_cut_out.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, cut_out=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_cut_out_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, fillcolor=(255, 0, 255), cut_out=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_out_of_image.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_out_of_image_clip.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_out_of_image_clip.png"
        crop_box = [(-15, 0), (325, 161), (14, 71), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop_pil(image, crop_box, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_complex.png"
        crop_box = [(15, 8), (368, 78), (450, 161), (200, 200), (-15, 50)]
        with Image.open(resources / "some_text.jpg") as image:
            ImageDraw.ImageDraw(image).polygon(crop_box, outline=(0, 0, 255))
            cropped_image = crop_pil(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_flip_complex.png"
        crop_box = [(15, 8), (-15, 50), (200, 200), (450, 161), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            ImageDraw.ImageDraw(image).polygon(crop_box, outline=(0, 0, 255))
            cropped_image = crop_pil(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_near_edge(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_near_edge.png"
        crop_box = [(102, 750), (101, 529), (324, 528), (322, 750)]
        with Image.open(resources / "qrcode_multi.png") as image:
            cropped_image = crop_pil(image, crop_box, fillcolor=(255, 0, 0))
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_generic_crop_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "pil" / "crop_complex.png"
        crop_box = [(15, 8), (368, 78), (450, 161), (200, 200), (-15, 50)]
        with Image.open(resources / "some_text.jpg") as image:
            ImageDraw.ImageDraw(image).polygon(crop_box, outline=(0, 0, 255))
            cropped_image = crop(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()


class TestCropCv2:

    DEBUG = False

    def test_full_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_1.png"
        crop_box = [(0, 0), (389, 0), (389, 177), (0, 177)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_2.png"
        crop_box = [(389, 0), (389, 177), (0, 177), (0, 0)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_3.png"
        crop_box = [(389, 177), (0, 177), (0, 0), (389, 0)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_4.png"
        crop_box = [(0, 177), (0, 0), (389, 0), (389, 177)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_flip_1.png"
        crop_box = [(0, 0), (0, 177), (389, 177), (389, 0)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_flip_2.png"
        crop_box = [(389, 0), (0, 0), (0, 177), (389, 177)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_flip_3.png"
        crop_box = [(389, 177), (389, 0), (0, 0), (0, 177)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_flip_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_flip_4.png"
        crop_box = [(0, 177), (389, 177), (389, 0), (0, 0)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_out(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_out.png"
        crop_box = [(-10, -10), (400, -10), (400, 200), (-10, 200)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_full_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "full_clip.png"
        crop_box = [(-10, -10), (400, -10), (400, 200), (-10, 200)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_1.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_2.png"
        crop_box = [(368, 78), (325, 161), (14, 71), (15, 8)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_3.png"
        crop_box = [(325, 161), (14, 71), (15, 8), (368, 78)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_4.png"
        crop_box = [(14, 71), (15, 8), (368, 78), (325, 161)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_1.png"
        crop_box = [(15, 8), (14, 71), (325, 161), (368, 78)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_2.png"
        crop_box = [(368, 78), (15, 8), (14, 71), (325, 161)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_3.png"
        crop_box = [(325, 161), (368, 78), (15, 8), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_4.png"
        crop_box = [(14, 71), (325, 161), (368, 78), (15, 8)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, fillcolor=(255, 0, 255))
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_cut_out.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, cut_out=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_cut_out_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, fillcolor=(255, 0, 255), cut_out=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_out_of_image.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_out_of_image_clip.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_out_of_image_clip.png"
        crop_box = [(-15, 0), (325, 161), (14, 71), (368, 78)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_complex.png"
        crop_box = [(15, 8), (368, 78), (450, 161), (200, 200), (-15, 50)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_flip_complex.png"
        crop_box = [(15, 8), (-15, 50), (200, 200), (450, 161), (368, 78)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_near_edge(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_near_edge.png"
        crop_box = [(102, 750), (101, 529), (324, 528), (322, 750)]
        image = cv2.imread(str(resources / "qrcode_multi.png"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop_cv2(image, crop_box, fillcolor=(255, 0, 255))
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_generic_crop_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "cv2" / "crop_complex.png"
        crop_box = [(15, 8), (368, 78), (450, 161), (200, 200), (-15, 50)]
        image = cv2.imread(str(resources / "some_text.jpg"), cv2.IMREAD_UNCHANGED)
        cropped_image = crop(image, crop_box, fillcolor=(255, 0, 255), cut_out=True, clip=True)
        # Use PIL image for saving and comparison of result
        cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "RGB")
        if self.DEBUG:
            cropped_image.show()
            if not expected_result.exists():
                cropped_image.save(expected_result, optimize=True)
        image_bytes = BytesIO()
        cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()
