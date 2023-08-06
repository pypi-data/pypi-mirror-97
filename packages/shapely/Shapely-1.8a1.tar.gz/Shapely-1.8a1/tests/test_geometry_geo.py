"""Tests of shape and mapping"""

import json

from shapely.geometry import mapping, shape
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon, Point


def test_multipolygon():
    """A two-polygon multipolygon round trips correctly"""
    geom = MultiPolygon([Point(-1, -1).buffer(0.5), Point(1, 1).buffer(0.5)])
    assert len(geom) == 2
    geoj = mapping(geom)
    assert len(geoj['coordinates']) == 2
    geom2 = shape(geoj)
    assert len(geom2) == 2
