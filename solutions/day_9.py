from typing import List

import numpy as np


def get_readings(data: List[str]) -> List[List[int]]:
    """
    Extract readings from the data
    :param data: input data
    :return: list of readings for each metric
    """
    return [list(map(int, d.split(" "))) for d in data]


def get_gradients(reading: List[int]) -> List[List[int]]:
    """
    Iteratively take the gradient across the values for a reading until all the values are 0
    :param reading: input reading
    :return: a list of each gradient
    """
    gradients = []
    grad = np.array(reading)
    while not np.all(grad == 0):
        gradients.append(grad.tolist())
        grad = np.diff(grad)
    gradients.append(grad.tolist())
    gradients.reverse()
    return gradients


def predict_next_value(gradients: List[List[int]]) -> int:
    """
    Predict the next measurement by adding the below gradient to the previous number in each gradient
    :param gradients: input list of gradients
    :return: gradients with next value predicted
    """
    for i, grad in enumerate(gradients):
        if i == 0:
            grad.append(0)
        else:
            grad.append(grad[-1] + gradients[i - 1][-1])
    return gradients[-1][-1]


def predict_next_values(data: List[str]) -> List[int]:
    """
    Predict the next value for each sequence
    :param data: input data
    :return: predicted values
    """
    readings = get_readings(data)
    return [predict_next_value(get_gradients(reading)) for reading in readings]


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return sum(predict_next_values(data))
    else:
        return 1
