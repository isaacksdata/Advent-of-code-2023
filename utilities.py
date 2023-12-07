import os

from dotenv import load_dotenv
from aocd import get_data, submit


load_dotenv()


def get_session() -> str:
    """
    Get the AOC session key from local environment
    :return: AOC session key
    """
    return os.environ["AOC_SESSION"]


def get_puzzle(year: int, day: int) -> str:
    """
    Use the AOC API to get the challenge data
    :param year: year of the challenge
    :param day: day of the challenge
    :return:
    """
    return get_data(session=get_session(), day=day, year=year)


def submit_answer(answer, part: str, day: int, year: int):
    """
    Submit and answer to AOC
    :param answer: Answer to the problem
    :param part: part of the problem e.g. A or B
    :param day: The day of the problem
    :param year: The year of the problem
    :return:
    """
    submit(answer, part=part, day=day, year=year, session=get_session())


def read_sample_data(path: str):
    """
    Read some sample data for testing with
    :param path: path to sample data
    :return: data from file
    """
    with open(path, 'r') as file:
        data = file.readlines()
    data = [x.replace("\n", "") for x in data]
    return data
