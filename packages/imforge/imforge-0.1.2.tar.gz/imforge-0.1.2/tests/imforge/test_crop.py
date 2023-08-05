from io import BytesIO

from PIL import Image, ImageDraw

from imforge.crop import crop


class TestCrop:

    DEBUG = False

    def test_crop_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_1.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_2.png"
        crop_box = [(368, 78), (325, 161), (14, 71), (15, 8)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_3.png"
        crop_box = [(325, 161), (14, 71), (15, 8), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_4.png"
        crop_box = [(14, 71), (15, 8), (368, 78), (325, 161)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_1(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_1.png"
        crop_box = [(15, 8), (14, 71), (325, 161), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_2(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_2.png"
        crop_box = [(368, 78), (15, 8), (14, 71), (325, 161)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_3(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_3.png"
        crop_box = [(325, 161), (368, 78), (15, 8), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_4(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_4.png"
        crop_box = [(14, 71), (325, 161), (368, 78), (15, 8)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box, fillcolor=(255, 0, 255))
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_cut_out.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box, cut_out=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_cut_out_fill(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_cut_out_fill.png"
        crop_box = [(15, 8), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box, fillcolor=(255, 0, 255), cut_out=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_out_of_image.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_out_of_image_clip.png"
        crop_box = [(-15, 0), (368, 78), (325, 161), (14, 71)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_flip_out_of_image_clip(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_out_of_image_clip.png"
        crop_box = [(-15, 0), (325, 161), (14, 71), (368, 78)]
        with Image.open(resources / "some_text.jpg") as image:
            cropped_image = crop(image, crop_box, clip=True)
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()

    def test_crop_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_complex.png"
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

    def test_crop_flip_complex(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_flip_complex.png"
        crop_box = [(15, 8), (-15, 50), (200, 200), (450, 161), (368, 78)]
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

    def test_crop_near_edge(self, resources):
        expected_result = resources / "imforge" / "crop" / "expected" / "crop_near_edge.png"
        crop_box = [(102, 750), (101, 529), (324, 528), (322, 750)]
        with Image.open(resources / "qrcode_multi.png") as image:
            cropped_image = crop(image, crop_box, fillcolor=(255, 0, 0))
            if self.DEBUG:
                cropped_image.show()
                if not expected_result.exists():
                    cropped_image.save(expected_result, optimize=True)
            image_bytes = BytesIO()
            cropped_image.save(image_bytes, format="png", optimize=True)
        image_bytes.seek(0)
        assert image_bytes.read() == expected_result.read_bytes()
