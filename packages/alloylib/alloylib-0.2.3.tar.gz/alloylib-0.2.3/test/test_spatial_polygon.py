import pytest
from alloy.spatial.primitives import Polygon, Line, Ray
import numpy as np 

def test_polygon_create():
    verticies = np.array([
        [0,1,0],
        [1,0,0],
        [1,1,0]
    ])
    p1 = Polygon(verticies)
    assert len(p1._vertices) == 3
    assert np.array_equal(p1._normal, np.array([0,0,1])) 

def test_polygon_line_intersect(capsys):

    with capsys.disabled():
        # parallal line
        line = Line(np.array([0,0,1]), np.array([1,0,0]))
        verticies = np.array([
            [-1,1,0],
            [1,0,0],
            [-1,-1,0]
        ])         
        p1 = Polygon(verticies)
        assert p1.intersect_with_line(line) == None

        line2 = Line(np.array([0,0,1]), np.array([0,0,-1]))
        result = p1.intersect_with_line(line2)
        assert result is not None
        assert np.array_equal(result, np.array([0,0,0]))

        line3 = Line(np.array([0,0,2]), np.array([0.5,0,-1]))
        result = p1.intersect_with_line(line3)
        assert result is not None

def test_polygon_line_intersect_inverse(capsys):

    with capsys.disabled():
        verticies = np.array([
            [-1,1,0],
            [1,0,0],
            [-1,-1,0]
        ])               
        p1 = Polygon(verticies)


        line2 = Line(np.array([0,0,1]), np.array([0,0,1]))
        result = p1.intersect_with_line(line2)
        assert result is not None
        assert np.array_equal(result, np.array([0,0,0]))

        line3 = Line(np.array([0,0,2]), np.array([0.5,0,1]))
        result = p1.intersect_with_line(line3)
        assert result is not None

def test_polygon_line_intersect_not_center(capsys):

    verticies = np.array([
        [1,1,1],
        [2,1,1],
        [1,2,1],
        [2,2,1],
    ])
    p1 = Polygon(verticies)
    
    line = Line(np.array([0,0,1]), np.array([1,0,0]))
    assert p1.intersect_with_line(line) is None
    assert p1.intersect_with_line(Line(np.array([0,0,1]), np.array([0,0,1]))) is None 
    assert p1.intersect_with_line(Line(np.array([-1,0,0]), np.array([0,0,1]))) is None
    assert p1.intersect_with_line(Line(np.array([1.5,1.5,1.5]), np.array([-0.5,0.5,0.5]))) is not None

def test_polygon_ray_intersect():
    verticies = np.array([
        [-1,1,0],
        [1,0,0],
        [-1,-1,0]
    ])               
    p1 = Polygon(verticies)


    ray = Ray(np.array([0.2,0,1]), np.array([0,0,1]))
    assert p1.intersect_with_ray(ray) is None

    ray2 = Ray(np.array([0.2,0,1]), np.array([0,0,-1]))
    result = p1.intersect_with_ray(ray2) 
    assert result is not None
    assert np.array_equal(result, np.array([0.2,0,0]))