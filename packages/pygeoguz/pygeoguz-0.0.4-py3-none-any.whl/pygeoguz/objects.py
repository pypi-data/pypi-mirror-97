from dataclasses import dataclass


@dataclass
class Point2D:
    """
    Точка в плоской прямоугольной системе координат (XY)
    """
    x: float
    y: float


@dataclass
class Point3D(Point2D):
    """
    Точка в пространственной прямоугольной системе координат (XYZ)
    """
    z: float


@dataclass
class PointBL:
    """
    Точка в геодезической системе координат (BL)
    """
    b: float
    l: float


@dataclass
class Line2D:
    length: float
    direction: float


@dataclass
class Angle:
    degrees: int
    minutes: int
    seconds: float
