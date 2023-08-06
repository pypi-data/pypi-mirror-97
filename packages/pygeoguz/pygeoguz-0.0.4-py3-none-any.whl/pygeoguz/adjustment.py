import math
import typing
import numpy as np

from .objects import Point2D
from .simplegeo import true_angle


class EquationSystem:
    """
    Система линейных уравнений, класс для решения системы матричным способом
    """

    def __init__(self,
                 a_matrix: np.ndarray,
                 l_matrix: np.ndarray = None,
                 p_matrix: np.ndarray = None):

        self._a_matrix = a_matrix
        self._l_matrix = l_matrix
        self._p_matrix = p_matrix

    def normalize(self) -> tuple:
        """
        Приведение системы линейных уравнений к нормальному виду
        :return: Нормальная матрица A, Нормальная матрица L
        """
        # Проверка системы на неравноточные измерения
        if self._p_matrix is None:
            rows, _ = np.shape(self._a_matrix)
            self._p_matrix = np.eye(rows)

        # Приведении системы уравнений к нормальному виду
        a_matrix_transposed = self._a_matrix.transpose()
        normal_coefficient = a_matrix_transposed.dot(self._p_matrix)
        normal_a_matrix = normal_coefficient.dot(self._a_matrix)
        if self._l_matrix is not None:
            normal_l_matrix = normal_coefficient.dot(self._l_matrix)
        else:
            normal_l_matrix = None
        return normal_a_matrix, normal_l_matrix

    def solve(self) -> tuple:
        """
        Решение системы нормальных уравнений и вычисление вектора поправок
        :return: Матрица неизвестных нормальных уравнений X, Решение исходной системы уоавнений V
        """
        normal_a_matrix, normal_l_matrix = self.normalize()
        if normal_l_matrix is not None:
            # Решение системы нормальных уравнений
            x_matrix = np.linalg.solve(normal_a_matrix, -normal_l_matrix)
            # Вычисление матрицы поправок
            v_matrix = self._a_matrix.dot(x_matrix) + self._l_matrix
            return x_matrix, v_matrix
        else:
            raise ValueError("l_matrix is None")

    def errors(self, extra_measures: int) -> np.ndarray:
        """
        Вычисление ковариационной матрицы системы нормальных линейных уравнений
        :return: Ковариационная матрица К
        """
        # Оценка точности решения системы нормальных уравнений
        # Вычисление обратной весовой матрицы

        normal_a_matrix, _ = self.normalize()
        q_matrix = np.linalg.inv(normal_a_matrix)

        _, v_matrix = self.solve()

        # Вычисление СКП единицы веса
        v_matrix_transposed = v_matrix.transpose()
        normal_coefficient = v_matrix_transposed.dot(self._p_matrix)
        pvv_sum = normal_coefficient.dot(v_matrix)
        mu = math.sqrt(pvv_sum / extra_measures)

        # Вычисление ковариационной матрицы К
        k_matrix = mu ** 2 * q_matrix
        return k_matrix

    def condition(self) -> float:
        """
        Вычисление числа обусловленности задачи
        :return: nu
        """
        normal_a_matrix, _ = self.normalize()
        # Эвквидова норма матриц А и А-1
        norma_a = math.sqrt(np.sum(normal_a_matrix ** 2))
        norma_a_inv = math.sqrt(np.sum(np.linalg.inv(normal_a_matrix) ** 2))
        nu = norma_a * norma_a_inv
        return nu


class TraverseAdjustment:
    """
    Уравнивание простого теодолитного хода
    """
    def __init__(self, first_dir_angle: float, last_dir_angle: float, angles: list, layings: list, first_point: Point2D,
                 last_point: Point2D, left_angles=True):
        """
        :param first_dir_angle: Начальный дир угол
        :param last_dir_angle: Последний дир угол
        :param angles: Список гор углов
        :param layings: Список горизонтальных проложений
        :param first_point: Начаьльная точка хода
        :param last_point: Последяя точка хода
        :param left_angles: Левые горизонтальные углы?
        """
        self.first_dir_angle = first_dir_angle
        self.last_dir_angle = last_dir_angle
        self.angles = np.array(angles)
        self.layings: np.ndarray = np.array(layings)
        self.first_point = first_point
        self.last_point = last_point
        self.left_angles = left_angles
        self.count_of_angles = len(angles)

    def _calc_theory_angles_sum(self) -> float:
        """
        Расчет теоритической суммы гор углов в зависимости от измеряемых ушлов (левые-правые)
        :return: Теоритическая сумма
        """
        if self.left_angles:
            theory_sum = self.last_dir_angle - self.first_dir_angle + 180 * self.count_of_angles
        else:
            theory_sum = self.first_dir_angle - self.last_dir_angle + 180 * self.count_of_angles
        return theory_sum

    def _calc_corrected_angles(self, theory_sum: float) -> np.ndarray:
        """
        Расчет горизонтальных углов с введенными поправками
        :param theory_sum: Теоритическая сумма гор углов
        :return: Массив гор углов с поправками
        """
        practical_sum_of_angles = np.sum(self.angles)
        angular_residual = practical_sum_of_angles - theory_sum
        correction = -angular_residual / self.count_of_angles
        corrected_angles = self.angles + correction
        return corrected_angles

    def _calc_dir_angles(self) -> np.ndarray:
        """
        Расчет дир углов хода
        :return: Массив дир углов
        """
        dir_angles = list()
        if self.left_angles:
            dir_angles.append(self.first_dir_angle + self.angles[0] - 180)
            for i in range(self.count_of_angles - 2):
                dir_angle = dir_angles[i] + self.angles[i + 1] - 180
                dir_angles.append(true_angle(dir_angle, 360))
        else:
            dir_angles.append(self.first_dir_angle - self.angles[0] + 180)
            for i in range(self.count_of_angles - 2):
                dir_angles = dir_angles[i] - self.angles[i + 1] + 180
                dir_angles.append(dir_angles[i] - self.angles[i + 1] + 180)
        return np.array(dir_angles)

    def _calc_deltas(self, dir_angles: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
        """
        Расчет приразений координат по дир углам хода
        :param dir_angles: Дир углы
        :return: Прирахения по координатам X и Y
        """
        deltas_x: np.ndarray = self.layings * np.cos(np.radians(dir_angles))
        deltas_y: np.ndarray = self.layings * np.sin(np.radians(dir_angles))
        return deltas_x, deltas_y

    def _calc_corrected_deltas(self, dir_angles: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
        """
        Расчет приращений координат с введенными поправками
        :param dir_angles: Дир углы хода
        :return: Приращения по координатам X и Y с поправками
        """
        deltas_x, deltas_y = self._calc_deltas(dir_angles)
        theory_sum_of_deltas_x = self.last_point.x - self.first_point.x
        theory_sum_of_deltas_y = self.last_point.y - self.first_point.y
        practical_sum_of_deltas_x = np.sum(deltas_x)
        practical_sum_of_deltas_y = np.sum(deltas_y)
        delta_x_residual = practical_sum_of_deltas_x - theory_sum_of_deltas_x
        delta_y_residual = practical_sum_of_deltas_y - theory_sum_of_deltas_y
        sum_of_layings = np.sum(self.layings)
        correction_to_deltas_x = -delta_x_residual * self.layings / sum_of_layings
        correction_to_deltas_y = -delta_y_residual * self.layings / sum_of_layings
        corrected_delta_x = np.round(deltas_x + correction_to_deltas_x, 3)
        corrected_delta_y = np.round(deltas_y + correction_to_deltas_y, 3)
        return corrected_delta_x, corrected_delta_y

    def _calc_coordinates(self, deltas_x: np.ndarray, deltas_y: np.ndarray) -> typing.Tuple[
                            typing.List[float], typing.List[float]]:
        """
        Расчет координат пунктов хода
        :param deltas_x: Приращения по X
        :param deltas_y: Приращения по Y
        :return: X и Y координаты хода
        """

        x_coordinates = list()
        x_coordinates.append(self.first_point.x + deltas_x[0])
        count_of_deltas = len(deltas_x)
        for i in range(count_of_deltas - 2):
            x_coordinates.append(x_coordinates[i] + deltas_x[i + 1])

        y_coordinates = list()
        y_coordinates.append(self.first_point.y + deltas_y[0])
        for i in range(count_of_deltas - 2):
            y_coordinates.append(y_coordinates[i] + deltas_y[i + 1])

        return x_coordinates, y_coordinates

    def adjust(self) -> typing.List[Point2D]:
        """
        Раздельное уравнивание простого теодеолитного хода
        :return: Уравненные координаты пунктов хода
        """
        self.angles = self._calc_corrected_angles(theory_sum=self._calc_theory_angles_sum())
        deltas_x, deltas_y = self._calc_corrected_deltas(dir_angles=self._calc_dir_angles())
        x_coordinates, y_coordinates = self._calc_coordinates(deltas_x, deltas_y)

        points = [Point2D(x, y) for x, y in zip(x_coordinates, y_coordinates)]
        return points
