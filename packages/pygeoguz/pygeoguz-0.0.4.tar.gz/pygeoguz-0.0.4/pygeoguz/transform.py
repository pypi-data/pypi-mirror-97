from math import sin, cos, radians, degrees

import numpy as np

from .objects import PointBL, Point2D, Point3D


def pz2wgs(point: Point3D) -> Point3D:
    """
    Преобразование координат точки из СК ПЗ-90 в СК WGS-84
    :param point: Точка в СК ПЗ-90
    :return: Точка в СК WGS-84
    """
    koeff_m = 1 - 0.12e-6
    rotation = np.array([
        [1, -0.9696e-6, 0],
        [0.9696e-6, 1, 0],
        [0, 0, 1]
    ])
    delta = np.array([[-1.1], [-0.3], [-0.9]])
    coords = np.array([[point.x], [point.y], [point.z]])
    answer = rotation.dot(coords) * koeff_m + delta
    return Point3D(float(answer[0]), float(answer[1]), float(answer[2]))


def wgs2pz(point: Point3D) -> Point3D:
    """
    Преобразование координат точки из СК WGS-84 в СК ПЗ-90
    :param point: Точка в СК WGS-84
    :return: Точка в СК ПЗ-90
    """
    koeff_m = 1 + 0.12e-6
    rotation = np.array([
        [1, 0.9696e-6, 0],
        [-0.9696e-6, 1, 0],
        [0, 0, 1]
    ])
    delta = np.array([[-1.1], [-0.3], [-0.9]])
    coords = np.array([[point.x], [point.y], [point.z]])
    answer = rotation.dot(coords) * koeff_m - delta
    return Point3D(float(answer[0]), float(answer[1]), float(answer[2]))


def bl2xy(point: PointBL) -> Point2D:
    """
    Преобразование координат точки из геодезической СК в плоскую прямоугольную СК Гаусса-Крюгера
    :param point: Точка в геодезической СК
    :return: Точка в плоской прямоуголькой СК Гаусса-Крюгера
    """
    number_of_zone = int(round((6 + point.l) / 6, 2))

    l = radians((point.l - (3 + 6 * (number_of_zone - 1))))
    b = radians(point.b)

    x = 6367558.4968 * b - sin(2 * b) * (16002.8900 + 66.9607 * (sin(b)) ** 2 + 0.3515 * (sin(b)) ** 4 - (l ** 2) * (
            1594561.25 + 5336.535 * (sin(b)) ** 2 + 26.790 * sin(b) ** 4 + 0.149 * sin(b) ** 6 + (l ** 2) * (
            672483.4 - 811219.9 * sin(b) ** 2 + 5420.0 * sin(b) ** 4 - 10.6 * sin(b) ** 6 + (l ** 2) * (
            278194 - 830174 * sin(b) ** 2 + 572434 * sin(b) ** 4 - 16010 * sin(b) ** 6 + (l ** 2) * (
            109500 - 574700 * sin(b) ** 2 + 863700 * sin(b) ** 4 - 398600 * sin(b) ** 6)))))

    y = (5 + 10 * number_of_zone) * (10 ** 5) + l * cos(b) * (
            6378245 + 21346.1415 * sin(b) ** 2 + 107.1590 * sin(b) ** 4 + 0.5977 * sin(b) ** 6 + (l ** 2) * (
            1070204.16 - 2136826.66 * sin(b) ** 2 + 17.98 * sin(b) ** 4 - 11.99 * sin(b) ** 6 + (l ** 2) * (
            270806 - 1523417 * sin(b) ** 2 + 1327645 * sin(b) ** 4 - 21701 * sin(b) ** 6 + (l ** 2) * (
            79690 - 866190 * sin(b) ** 2 + 1730360 * sin(b) ** 4 - 945460 * sin(b) ** 6))))
    return Point2D(x, y)


def xy2bl(point: Point2D) -> PointBL:
    """
    Преобразование координат точки из плоской прямоугольной СК Гаусса-Крюгера в геодезическую СК
    :param point: очка в плоской прямоуголькой СК Гаусса-Крюгера
    :return: Точка в геодезической СК
    """
    number_of_zone = int(round(point.y * 10**(-6), 2))

    betta = point.x / 6367558.4968
    b_0 = betta + sin(2 * betta) * (0.00252588685 - 0.00001491860 * sin(betta)**2 + 0.00000011904 * sin(betta)**4)
    z_0 = (point.y - (10 * number_of_zone + 5) * 10**5) / (6378245 * cos(b_0))

    delta_b = -(z_0)**2 * sin(2 * b_0) * (0.251684631 - 0.003369263 * sin(b_0)**2 + 0.000011276 * sin(b_0)**4 -
                (z_0)**2 * (0.10500614 - 0.04559916 * sin(b_0)**2 + 0.00228901 * sin(b_0)**4 - 0.00002987 * sin(b_0)**6 -
                (z_0)**2 * (0.042858 - 0.025318 * sin(b_0)**2 + 0.014346 * sin(b_0)**4 - 0.001264 * sin(b_0)**6 -
                (z_0)**2 * (0.01672 - 0.00630 * sin(b_0)**2 + 0.01188 * sin(b_0)**4 - 0.00328 * sin(b_0)**6))))

    l = z_0 * (1 - 0.0033467108 * sin(b_0)**2 - 0.0000056002 * sin(b_0)**4 - 0.0000000187 * sin(b_0)**6 -
        (z_0)**2 * (0.16778975 + 0.16273586 * sin(b_0)**2 - 0.00052490 * sin(b_0)**4 - 0.00000846 * sin(b_0)**6 -
        (z_0)**2 * (0.0420025 + 0.1487407 * sin(b_0)**2 + 0.0059420 * sin(b_0)**4 - 0.0000150 * sin(b_0)**6 -
        (z_0)**2 * (0.01225 + 0.09477 * sin(b_0)**2 + 0.03282 * sin(b_0)**4 - 0.00034*sin(b_0)**6 -
        (z_0)**2 * (0.0038 + 0.0524 * sin(b_0)**2 + 0.0482 * sin(b_0)**4 + 0.0032 * sin(b_0)**6)))))

    l = radians(6 * (number_of_zone - 0.5)) + l
    b = b_0 + delta_b
    return PointBL(degrees(b), degrees(l))

