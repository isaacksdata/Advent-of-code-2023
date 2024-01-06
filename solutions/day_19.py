import re
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


def obj_str_to_dict(s: str) -> Dict[str, int]:
    """
    Convert a str object to a dictionary

    The strings are expected to be of the format "{x=787,m=2655,a=1222,s=2876}"
    :param s: input string
    :return: dict
    """
    return {(parts := sub.split("="))[0].strip(): int(parts[1]) for sub in s[1:-1].split(",")}


def make_func(op: str) -> Callable:
    """
    Take a string which describes an operation to be carried out

    The operation can do one of two things:
    1) Return a string
    2) Take a dictionary an input and extract a value from the dictionary and check if this value if greater or
        smaller than another value described in the op string. If the condition is met then the answer contained
        within the op is returned, else None

    Example:
        op -> "a<2006:qkq"
        Then the function returned should get the value for "a" from the dictionary and return qkq if smaller than
        2006, otherwise return None
    :param op: the operation string
    :return: function carrying out the operation
    """
    if ":" not in op:

        def f(d: Dict[str, int]) -> Optional[str]:
            return op

    else:
        sign = op[1]
        ans = op.split(":")[1]
        other = int(op.split(":")[0].split(sign)[1])
        key = op.split(":")[0].split(sign)[0]

        def f(d: Dict[str, int]) -> Optional[str]:
            if sign == "<" and d[key] < other:
                return ans
            if sign == ">" and d[key] > other:
                return ans
            return None

    return f


class Pipeline:
    """
    A class for handling a pipeline
    """

    def __init__(self, config: str) -> None:
        """
        Initialise the pipeline with a config string
        :param config:
        """
        self.config: str = config
        self.name: Optional[str] = None
        self.operations: Optional[List[Callable]] = None

        self.extract_name()
        self.extract_operations()

    def extract_name(self) -> None:
        """
        Extract the pipeline name from config
        :return: void
        """
        self.name = self.config.split("{")[0]

    def extract_operations(self) -> None:
        """
        Extract operations from the config and create functions from the operation string
        :return: void
        """
        pattern = r"\{(.*?)\}"
        m = re.search(pattern, self.config)
        if m is None:
            raise ValueError("No operations found!")
        ops = self.config[m.start() + 1 : m.end() - 1].split(",")
        self.operations = [make_func(op) for op in ops]

    def execute(self, obj: Dict[str, int]) -> str:
        """
        Iterate over the operations for this pipeline until an answer is reached which is not None
        :param obj: the object to perform operations on
        :return: answer
        """
        if self.operations is None:
            raise ValueError("Operations not initialised!")
        ans = ""
        for op in self.operations:
            ans = op(obj)
            if ans is not None:
                break
        return ans


def get_pipelines_and_objects(data: List[str]) -> Tuple[List[str], List[str]]:
    """
    Extract the configs for pipelines and objects from the input data
    :param data: input data
    :return: pipelines, objects
    """
    idx = [i for i, x in enumerate(data) if not x][0]
    pipelines = data[:idx]
    objects = data[idx + 1 :]
    return pipelines, objects


def sum_accepted_objects(data: List[str]) -> int:
    """
    Execute pipelines over a list of objects and sum the data for accepted objects

    Each object will be processed by some sequence of pipelines and result in A or R.
    If A, then add the object to accepted else Reject it.
    Sum the dictionary values for each accepted objects and sum these object totals
    :param data: input data
    :return: sum
    """
    pipeline_str, obj_str = get_pipelines_and_objects(data)
    pipelines = [Pipeline(p) for p in pipeline_str]
    pipelines_dict = {p.name: p for p in pipelines}
    obj_dicts = [obj_str_to_dict(s) for s in obj_str]
    accepted_objs = []
    for obj in obj_dicts:
        a = "in"
        while a not in ["A", "R"]:
            pipeline = pipelines_dict[a]
            a = pipeline.execute(obj)
        if a == "A":
            accepted_objs.append(obj)
    total = sum([sum(obj.values()) for obj in accepted_objs])
    return total


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return sum_accepted_objects(data)
    else:
        return 1


# if __name__ == "__main__":
#     test_data = [
#         "px{a<2006:qkq,m>2090:A,rfg}",
#         "pv{a>1716:R,A}",
#         "lnx{m>1548:A,A}",
#         "rfg{s<537:gd,x>2440:R,A}",
#         "qs{s>3448:A,lnx}",
#         "qkq{x<1416:A,crn}",
#         "crn{x>2662:A,R}",
#         "in{s<1351:px,qqz}",
#         "qqz{s>2770:qs,m<1801:hdj,R}",
#         "gd{a>3333:R,R}",
#         "hdj{m>838:A,pv}",
#         "",
#         "{x=787,m=2655,a=1222,s=2876}",
#         "{x=1679,m=44,a=2067,s=496}",
#         "{x=2036,m=264,a=79,s=2244}",
#         "{x=2461,m=1339,a=466,s=291}",
#         "{x=2127,m=1623,a=2188,s=1013}",
#     ]
#     solve(test_data)
