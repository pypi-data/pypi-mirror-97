
def is_clockwise(polygon, check_convexity=False):
    """
    Return whether or not given polygon is clockwise oriented or not.

    If ``check_convexity`` is False (the default), it's assumed that given polygon is convex, so we only check for
    orientation based on the first vertex.
    If ``check_convexity`` is True, then we check orientation for all vertices and they must all have the same
    orientation (i.e. the polygon is convex)

    :param list[tuple[int, int]] polygon: the list of polygon vertices which for we want orientation
    :param bool check_convexity: specify whether or not we have to check convexity of polygon. If False (the default)
      we compute orientation based on the first vertex.
    :return: ``True`` if polygon is clockwise oriented. ``False`` if it is counterclockwise oriented.
    :rtype: bool
    :raises ValueError:
      - if polygon does not contain at least 3 distinct vertices
      - if ``check_convexity`` is True, and the polygon is not convex
      - if 3 consecutive vertices of polygon are aligned
    """
    if len(polygon) < 3:
        raise ValueError(f"Polygon {polygon} contains less than 3 vertices")

    polygon = [polygon[-1]] + polygon + [polygon[0]]
    found_results = set()
    for idx in range(1, len(polygon) - 1):
        result = _is_clockwise(polygon[idx - 1], polygon[idx], polygon[idx + 1])
        if result is not None:
            if not check_convexity:
                return result
            found_results.add(result)
    if not found_results:
        raise ValueError(f"Polygon {polygon} does not contain 3 distinct vertices")
    if len(found_results) > 1:
        raise ValueError(f"Polygon {polygon} is not convex")
    return found_results.pop()


def _is_clockwise(v1, v2, v3):
    """
    Return whether or not polygon around v2 vertex is clockwise oriented or not.

    :param tuple[int, int] v1: the previous vertex
    :param tuple[int, int] v2: the vertex which for we want the angle
    :param tuple[int, int] v3: the next vertex
    :return: whether or not v2 vertex is clockwise oriented. If angle is 180°, return ``None``
    :rtype: bool|None
    :raises ValueError: if angle is 0° (the polygon is not convex)
    """
    v2_v1 = (v1[0] - v2[0], v1[1] - v2[1])
    v2_v3 = (v3[0] - v2[0], v3[1] - v2[1])
    cross_product = v2_v1[0] * v2_v3[1] - v2_v1[1] * v2_v3[0]
    if cross_product == 0:
        if v1 == v2 or v2 == v3:
            return None  # not real angle as 2 consecutive vertices are combined
        # Collinear vectors. Check if angle is 0° or 180°
        if v2_v1[0] == 0:
            is_null_angle = (v2_v1[1] > 0) == (v2_v3[1] > 0)  # same sign
        else:
            is_null_angle = (v2_v1[0] > 0) == (v2_v3[0] > 0)  # same signe
        if is_null_angle:
            raise ValueError(f"Polygon is not convex for consecutive vertices [{v1}, {v2}, {v3}]")
        return None  # flat angle
    return cross_product < 0
