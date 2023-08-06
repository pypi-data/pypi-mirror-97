import pytest
from imforge.utils import is_clockwise, clip_polygon


class TestIsClockwise:

    def test_clockwise(self):
        assert is_clockwise([(0, 0), (100, 0), (100, 200), (50, 250)])
        assert is_clockwise([(0, 0), (100, 0), (150, 200), (150, 300), (50, 500)])
        assert is_clockwise([(0, 0), (100, 0), (50, 110)])

    def test_clockwise_with_check(self):
        assert is_clockwise([(0, 0), (100, 0), (100, 200), (50, 250)], check_convexity=True)
        assert is_clockwise([(0, 0), (100, 0), (150, 200), (150, 300), (50, 500)], check_convexity=True)
        assert is_clockwise([(0, 0), (100, 0), (50, 110)], check_convexity=True)

    def test_counterclockwise(self):
        assert not is_clockwise([(0, 0), (50, 250), (100, 200), (100, 0)])
        assert not is_clockwise([(0, 0), (50, 500), (150, 300), (150, 200), (100, 0)])
        assert not is_clockwise([(0, 0), (50, 110), (100, 0)])

    def test_counterclockwise_with_check(self):
        assert not is_clockwise([(0, 0), (50, 250), (100, 200), (100, 0)], check_convexity=True)
        assert not is_clockwise([(0, 0), (50, 500), (150, 300), (150, 200), (100, 0)], check_convexity=True)
        assert not is_clockwise([(0, 0), (50, 110), (100, 0)], check_convexity=True)

    def test_insufficient_number_of_vertices(self):
        with pytest.raises(ValueError):
            is_clockwise([(0, 0), (100, 100)])

    def test_insufficient_number_of_distinct_vertices(self):
        with pytest.raises(ValueError):
            is_clockwise([(0, 0), (100, 100), (100, 100), (0, 0)])

    def test_not_convex_with_check(self):
        with pytest.raises(ValueError):
            is_clockwise([(100, 100), (150, 100), (150, 150), (200, 150)], check_convexity=True)

    def test_not_convex_without_check(self):
        assert is_clockwise([(100, 100), (150, 100), (150, 150), (200, 150), (200, 200), (100, 200)])

    def test_null_angle(self):
        with pytest.raises(ValueError):
            is_clockwise([(0, 0), (100, 0), (50, 0)])
        with pytest.raises(ValueError):
            is_clockwise([(0, 0), (0, 100), (0, 50)])

    def test_flat_angle_with_sufficient_number_of_vertices(self):
        assert is_clockwise([(0, 0), (100, 0), (200, 0), (100, 50)], check_convexity=True)
        assert not is_clockwise([(0, 0), (100, 50), (200, 0), (100, 0)], check_convexity=True)


class TestClipPolygon:

    def test_clip_polygon(self):
        polygon = [(15, 8), (-15, 50), (200, 200), (450, 161), (368, 78)]
        width, height = 390, 178
        clipped_polygon = clip_polygon(polygon, width, height)
        assert clipped_polygon == [[368, 78], [389, 99], [389, 171], [347, 177], [167, 177], [0, 60], [0, 29], [15, 8]]

    def test_clip_full(self):
        polygon = [(0, 0), (389, 0), (389, 177), (0, 177)]
        width, height = 390, 178
        clipped_polygon = clip_polygon(polygon, width, height)
        assert clipped_polygon == [[389, 177], [0, 177], [0, 0], [389, 0]]

    def test_clip_straight_rectangle_outside(self):
        polygon = [(-1, -1), (390, -1), (390, 178), (-1, 178)]
        width, height = 390, 178
        clipped_polygon = clip_polygon(polygon, width, height)
        assert clipped_polygon == [[389, 177], [0, 177], [0, 0], [389, 0]]
