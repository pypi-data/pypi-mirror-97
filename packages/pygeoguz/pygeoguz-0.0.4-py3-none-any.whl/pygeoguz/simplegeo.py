import math
from random import normalvariate

from sympy import Segment, Point

from pygeoguz.objects import Point2D, Line2D, Angle


def _ground(number: float, n: int = 0) -> float:
    """
    Округление по Гауссу
    :param number: Число для округления
    :param n: Количество знаков после запятой (по умолчанию = 0)
    :return: Округленное число
    """
    if n < 0:
        raise ValueError

    def is_odd(num) -> bool:
        """
        Нечетное ли число?
        """
        if num % 2 == 0:
            return False
        else:
            return True
    # Предварительное округление до знака n+1
    number = round(number, n + 1)
    string = str(number).split('.')
    before, after = list(string[0]), list(string[1])
    # Добавление недостающих до разряда округления цифр
    if len(after) - n <= 0:
        need_to_add = abs(len(after) - n) + 1
        after += ['0'] * need_to_add
    #
    if after[n] != '5':
        return round(number, n)
    else:
        if n != 0:
            rounding_fractional = int(after[n - 1])
            if is_odd(rounding_fractional):
                return math.ceil(number * 10**n) / 10**n
            return math.floor(number * 10**n) / 10**n

        else:
            last_integer = int(before[-1])
            if is_odd(last_integer):
                return math.ceil(number)
            return math.floor(number)


def ground(number: float, n: int = 0) -> float:
    """
    Округление по Гауссу
    :param number: Число для округления
    :param n: Количество знаков после запятой (по умолчанию = 0)
    :return: Округленное число
    """
    if n < 0:
        raise ValueError

    def is_odd(num) -> bool:
        """
        Нечетное ли число?
        """
        return False if num % 2 == 0 else True

    def is_five(num, order) -> bool:
        """
        Проверяем разрядное число на равенство 5
        """
        num = num * 10**order
        five = (num - math.trunc(num)) * 10
        return True if five == 5 else False

    # Предварительное округление до n+1
    number = round(number, n + 1)

    if is_five(number, n):
        if is_odd(math.trunc(number * 10**n)):
            # Повышение
            return math.ceil(number * 10**n) / 10**n
        # Понижение
        return math.floor(number * 10**n) / 10**n
    return round(number, n)


def true_angle(angle: float, max_value: int) -> float:
    """
    Возвращает верное значение угла
    :param angle: Угол
    :param max_value: Максимальное допустимое значение (180, 360)
    :return: Верное значение угла
    """
    if angle > max_value:
        return angle - max_value
    elif angle < 0:
        return angle + max_value
    else:
        return angle


def left_angle(dir_a: float, dir_b: float) -> float:
    """
    Вычисление левых углов хода
    :param dir_a: Начальный дир угол
    :param dir_b: Конечный дир угол
    :return: Левый горизонтальный угол хода
    """
    angle = dir_b - dir_a + 180
    return true_angle(angle, 360)
    

def from_h_to_d(hours: float) -> float:
    """
    Трансформирует угол из часовой меры в угловую
    :param hours: Угол в часовой мере
    :return: Угол в градусной мере
    """
    return hours * 15


def from_d_to_h(degrees: float) -> float:
    """
    Трансформирует угол из градусной меры в часовую
    :param degrees: Угол в градусной мере
    :return: Угол в часовой мере
    """
    return degrees / 15


def to_degrees(degrees: int, minutes: float, seconds: float = 0) -> float:
    """
    Преобразование dms -> d
    :param degrees: Градусы
    :param minutes: Минуты
    :param seconds: Секунды
    :return: Градусы
    """
    return degrees + minutes / 60 + seconds / 3600


def to_dms(degrees: float, n_sec: int = 0) -> Angle:
    """
    Преобразвоание d -> dms
    :param n_sec: Количество знаков после заяртой у значения секунд
    :param degrees: Градусы
    :return: Кортеж (градусы, минуты, секунды)
    """
    d = math.trunc(degrees)
    m = math.trunc((degrees - d) * 60)
    s = ground(((degrees - d) - m / 60) * 60 * 60, n_sec)
    return Angle(d, m, s)


def ogz(point_a: Point2D, point_b: Point2D) -> Line2D:
    """
    Обратная геодезическая задача для координат пунктов
    :param point_a: Начальная точка
    :param point_b: Конечная точка
    :return: Кортеж (дирекционный угол, горизонтальное проложение)
    """
    delx = point_b.x - point_a.x
    dely = point_b.y - point_a.y
    s = math.sqrt(delx ** 2 + dely ** 2)

    if dely == 0 and delx > 0:
        alf = 0
    elif dely == 0 and delx < 0:
        alf = 180
    elif delx == 0 and dely > 0:
        alf = 90
    elif delx == 0 and dely < 0:
        alf = 270
    else:
        rumb = math.fabs(math.degrees(math.atan(dely / delx)))

        if delx > 0 and dely > 0:
            alf = rumb
        elif delx < 0 and dely > 0:
            alf = 180 - rumb
        elif delx < 0 and dely < 0:
            alf = 180 + rumb
        elif delx > 0 and dely < 0:
            alf = 360 - rumb
    return Line2D(s, alf)


def pgz(point: Point2D, degrees: int, minutes: int, seconds: float, horizontal_laying: float) -> Point2D:
    """
    Прямая геодезическая задача
    :param point: Начальная точка
    :param degrees: Дирекционный угол (градусы)
    :param minutes: Дирекционный угол (минуты)
    :param seconds: Дирекционный угол (секунды)
    :param horizontal_laying: Горизонтальное проложение
    :return: Точка на плоскости
    """
    angle = degrees + minutes / 60 + seconds / (60 * 60)
    angle = math.radians(angle)
    x = point.x + horizontal_laying * math.cos(angle)
    y = point.y + horizontal_laying * math.sin(angle)
    return Point2D(x, y)


def polygon_square(points: list) -> float:
    """
    Площадь полигона по координатам его вершин
    Формула Гаусса
    :param points: Список координат вершин полигона
    :return: Значение площади
    """
    sx = 0
    sy = 0
    n = len(points)
    for i in range(n):
        if i != n - 1:
            sx += points[i][0] * points[i + 1][1]
        elif i == n - 1:
            sx += points[i][0] * points[0][1]
    for i in range(n):
        if i != n - 1:
            sy -= points[i][1] * points[i + 1][0]
        elif i == n - 1:
            sy -= points[i][1] * points[0][0]
    square = math.fabs(sx + sy) / 2
    return square


def midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple:
    """
    Координаты середины отрезка
    :param x1: Координата х первого пункта
    :param y1: Координата у первого пункта
    :param x2: Координата х второго пункта
    :param y2: Координата у второго пункта
    :return: Кортеж координат середины отрезка
    """
    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2
    return xm, ym


def intersection_of_segments(p1_x: Point, p1_y: Point, p2_x: Point, p2_y: Point) -> tuple:
    """
    Координаты точки пересечения двух отрезков
    :param p1_x: Первая точка первого отрезка
    :param p1_y: Вторая точка первого отрезка
    :param p2_x: Первая точка второго отрезка
    :param p2_y: Вторая точка второго отрезка
    :return: Кортеж координат точки пересечения отрезков
    """
    s1 = Segment(p1_x, p1_y)
    s2 = Segment(p2_x, p2_y)
    intersection = s1.intersection(s2)
    if len(intersection) != 0:
        intersection = intersection[0]
        return float(intersection.x), float(intersection.y)
    else:
        return None, None


def generate_errors(mu: float, count: int) -> list:
    """
    Генерация списка псевдослучайных ошибок,
    подчиняющихся нормальному закону распределения
    :param mu: среднее квадартическое отклонение
    :param count: Количество ошибок для генерации
    :return: Список ошибок
    """
    errors = list()
    for i in range(count):
        errors.append(round(normalvariate(0, mu), 0))
    return errors
