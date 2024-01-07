import math
import re
from abc import ABC
from abc import abstractmethod
from typing import Any
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


def make_func(op: str, part: str = "a") -> Callable:
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
    :param part: part of the problem to solve
    :return: function carrying out the operation
    """
    if ":" not in op:
        if part == "a":

            def fa(d: Dict[str, int]) -> Optional[str]:
                return op

        else:

            def fb(d: Dict[str, List[int]]) -> Tuple[Optional[str], Dict[str, List[int]], Dict[str, List[int]]]:
                return op, d, {}

    else:
        sign = op[1]
        answer = op.split(":")[1]
        other = int(op.split(":")[0].split(sign)[1])
        key = op.split(":")[0].split(sign)[0]

        def fa(d: Dict[str, int]) -> Optional[str]:
            if sign == "<" and d[key] < other:
                return answer
            if sign == ">" and d[key] > other:
                return answer
            return None

        def fb(d: Dict[str, List[int]]) -> Tuple[Optional[str], Dict[str, List[int]], Dict[str, List[int]]]:
            s, e = d[key]
            if sign == "<":
                if other < s:
                    in_range = []
                    out_range = [s, e]
                elif other > e:
                    in_range = [s, e]
                    out_range = []
                else:
                    in_range = [s, other - 1]
                    out_range = [other, e]
                if in_range:
                    d_in = d.copy()
                    d_in[key] = in_range
                else:
                    d_in = {}
                if out_range:
                    d_out = d.copy()
                    d_out[key] = out_range
                else:
                    d_out = {}
                return answer, d_in, d_out
            if sign == ">":
                if other > e:
                    in_range = []
                    out_range = [s, e]
                elif other < s:
                    in_range = [s, e]
                    out_range = []
                else:
                    in_range = [other + 1, e]
                    out_range = [s, other]
                if in_range:
                    d_in = d.copy()
                    d_in[key] = in_range
                else:
                    d_in = {}
                if out_range:
                    d_out = d.copy()
                    d_out[key] = out_range
                else:
                    d_out = {}
                return answer, d_in, d_out
            return None, {}, {}

    if part == "a":
        return fa
    else:
        return fb


class AbstractPipeline(ABC):
    """
    A class for handling a pipeline
    """

    def __init__(self, config: str, part: str) -> None:
        """
        Initialise the pipeline with a config string
        :param config:
        """
        self.config: str = config
        self.part: str = part
        self._name: Optional[str] = None
        self.operations: Optional[List[Callable]] = None

        self.extract_name()
        self.extract_operations()

    @property
    def name(self) -> str:
        if self._name is None:
            raise ValueError("Name is None")
        return self._name

    def extract_name(self) -> None:
        """
        Extract the pipeline name from config
        :return: void
        """
        self._name = self.config.split("{")[0]

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
        self.operations = [make_func(op, part=self.part) for op in ops]

    @abstractmethod
    def execute(self, obj: Dict[str, int]) -> Any:
        """
        Iterate over the operations for this pipeline until an answer is reached which is not None
        :param obj: the object to perform operations on
        :return: answer
        """
        pass


class Pipeline_A(AbstractPipeline):
    """
    A class for handling a pipeline
    """

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


class Pipeline_B(AbstractPipeline):
    """
    A class for handling a pipeline in part B
    """

    def execute(self, obj: Dict[str, int]) -> List[Tuple[str, Dict[str, List[int]]]]:
        """
        Iterate over the operations for this pipeline until an answer is reached which is not None
        :param obj: the object to perform operations on
        :return: answer
        """
        if self.operations is None:
            raise ValueError("Operations not initialised!")
        results: List[Tuple[str, Dict[str, List[int]]]] = []
        for op in self.operations:
            ans, in_d, out_d = op(obj)
            if in_d:
                results.append((ans, in_d))
            if out_d:
                obj = out_d
            else:
                break
        return results


def pipeline_factory(pipeline_config: str, part: str = "a") -> AbstractPipeline:
    """
    Create pipeline instance using config for the provided part
    :param pipeline_config: config for the pipeline
    :param part: problem part - indicates which type of pipeline to instantiate
    :return: pipeline object
    """
    return (
        Pipeline_A(config=pipeline_config, part=part) if part == "a" else Pipeline_B(config=pipeline_config, part=part)
    )


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
    pipelines = [pipeline_factory(p, part="a") for p in pipeline_str]
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


def get_range(
    start: dict, pipelines_dict: Dict[str, AbstractPipeline], pipeline_name: str = "in"
) -> Tuple[List[Dict[str, List[int]]], ...]:
    """
    Find accepted and rejected ranges

    Provided with a starting dict of ranges, a dictionary of pipelines and an initial pipeline name,
    recursively work through the number ranges until all are accepted or rejected
    :param start: a dictionary of ranges
    :param pipelines_dict: dictionary of pipelines {"pipeline_name": pipeline}
    :param pipeline_name: initial pipeline name
    :return: accepted_ranges, rejected_ranges
    """
    pipeline = pipelines_dict[pipeline_name]
    results = pipeline.execute(start)
    accepted_ranges = []
    rejected_ranges = []
    for pn, obj in results:
        if pn == "A":
            accepted_ranges.append(obj)
        elif pn == "R":
            rejected_ranges.append(obj)
        else:
            acc, rej = get_range(start=obj, pipelines_dict=pipelines_dict, pipeline_name=pn)
            accepted_ranges.extend(acc)
            rejected_ranges.extend(rej)
    return accepted_ranges, rejected_ranges


def count_combinations(data: List[str]) -> int:
    """
    Take the pipelines and determine how many unique combinations of [x, m, a, s] will be accepted

    x, m, a and s can take any integer from 1 to 4000 inclusive.
    To calculate this number, pass ranges through the pipelines until all ranges are accepted or rejected
    :param data: input data
    :return: number of combinations
    """
    pipeline_str, _ = get_pipelines_and_objects(data)
    pipelines = [pipeline_factory(p, part="b") for p in pipeline_str]
    pipelines_dict: Dict[str, AbstractPipeline] = {p.name: p for p in pipelines}
    start: Dict[str, List[int]] = {i: [1, 4000] for i in ["x", "m", "a", "s"]}
    acc_ranges, rej_ranges = get_range(start, pipelines_dict)
    total = 0
    for r in acc_ranges:
        total += math.prod([(v[1] - v[0]) + 1 for _, v in r.items()])
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
        return count_combinations(data)
