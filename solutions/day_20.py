import math
from abc import ABC
from abc import abstractmethod
from collections import deque
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


class Module(ABC):
    """
    Abstract class for basic module logic

    A module can receive a pulse, process it and emit a pulse to targets
    """

    def __init__(self, name: str, targets: List[str]) -> None:
        """
        Initialise the Module

        :param name: name of the module
        :param targets: targets of the module
        """
        self.name: str = name
        self.targets: List[str] = targets

    @staticmethod
    def validate_pulse(pulse: int) -> bool:
        """
        Validate that a pulse is valid

        :param pulse: the pulse
        :return: True if valid
        """
        if pulse not in [0, 1]:
            raise ValueError("Pulse should be 0 ir 1!")
        return True

    @abstractmethod
    def process(self, pulse: int, input_name: str) -> Optional[int]:
        pass


class FlipFlop(Module):
    """
    Flip flop modules do nothing for high input pulses, and flip between ON and OFF states for low pulses
    """

    TYPE = "%"

    def __init__(self, name: str, targets: List[str]) -> None:
        """
        Initialise the Module

        :param name: name of the module
        :param targets: targets of the module
        """
        super().__init__(name, targets)
        self.state: int = 0

    def process(self, pulse: int, input_name: str) -> Optional[int]:
        """
        Process the input pulse and emit a response pulse

        :param pulse: input pulse
        :param input_name: name of the input which sent the pulse
        :return: new pulse
        """
        _ = self.validate_pulse(pulse)
        if pulse == 1:
            return None
        if self.state == 0:
            self.state = 1
            return 1
        else:
            self.state = 0
            return 0


class Conjunction(Module):
    """
    Conjunction modules remember the last pulse sent by input modules.

    If the module remembers all inputs to be high then a low response is emitted. Else a low pulse is emitted.
    Conjunction modules need the memory to be initiated with all inputs see init_memory()
    """

    TYPE = "&"

    def __init__(self, name: str, targets: List[str]) -> None:
        """
        Initialise the Module

        :param name: name of the module
        :param targets: targets of the module
        """
        super().__init__(name, targets)
        self.memory: Dict[str, int] = {}

    def process(self, pulse: int, input_name: str) -> Optional[int]:
        """
        Process the pulse by checking with memory

        :param pulse: input pulse
        :param input_name: name of the input module
        :return: pulse
        """
        # add input to memory if not already present
        if input_name not in self.memory:
            self.memory[input_name] = 0

        # process the latest pulse
        self.memory[input_name] = pulse

        # determine output
        if all([v == 1 for v in self.memory.values()]):
            return 0
        return 1

    def init_memory(self, inputs: List[str]) -> None:
        """
        Initialise the memory with input modules

        :param inputs: list of input names
        :return: void
        """
        self.memory = {t: 0 for t in inputs}


class Broadcast(Module):
    """
    The broadcast module takes in an input and re-emits teh same signal to targets
    """

    TYPE = "broadcaster"

    def process(self, pulse: int, input_name: str) -> Optional[int]:
        """
        Process the input signal

        :param pulse: input pulse
        :param input_name: name of the input module
        :return: pulse
        """
        return pulse


class Button(Module):
    """
    Button is the start of each set of pulses. It always emits a low signal
    """

    TYPE = "button"

    def process(self, pulse: int, input_name: str) -> Optional[int]:
        """
        Process the input signal

        :param pulse: input pulse
        :param input_name: name of the input module
        :return: pulse
        """
        return 0


class Output(Module):
    """
    Output module only receives pulses
    """

    TYPE = "output"

    def process(self, pulse: int, input_name: str) -> Optional[int]:
        """
        Process the input signal

        :param pulse: input pulse
        :param input_name: name of the input module
        :return: pulse
        """
        pass


def module_factory(config: str) -> Module:
    """
    Create a module instance by parsing and interpreting a config string

    :param config: description of the module
    :return: module instance
    """
    name, targets = config.split(" -> ")
    targets_list = targets.split(", ")
    if name != "broadcaster":
        mod_type = name[0]
        name = name[1:]
    else:
        mod_type = "broadcaster"
    match mod_type:
        case "broadcaster":
            mod: Module = Broadcast(name=name, targets=targets_list)
        case "%":
            mod = FlipFlop(name=name, targets=targets_list)
        case "&":
            mod = Conjunction(name=name, targets=targets_list)
        case _:
            raise ValueError("Unexpected module type!")
    return mod


def press_button(
    modules: Dict[str, Module], button: Button, output_prev_name: Optional[str] = None
) -> Tuple[int, int, Dict[str, Module], bool, Optional[str]]:
    """
    Press the button and count number of low and high pulses

    :param modules: dictionary of modules
    :param button: the button module
    :param output_prev_name: the name of the module which precedes the output rx
    :return: n high, n low, True if a low pulse sent to rx
    """
    queue: Deque[Tuple[int, str, str]] = deque()
    pulse = button.process(pulse=0, input_name="")
    if pulse is None:
        raise ValueError("Starting pulse should not be None!")
    target = button.targets[0]
    queue.append((pulse, target, button.name))
    n_high_beams = 0
    n_low_beams = 0
    low_rx = False
    output_prev_tracker = None
    while queue:
        p, t, prev_t = queue.pop()
        if p:
            n_high_beams += 1
        else:
            n_low_beams += 1
        if t not in modules:
            continue
        m = modules[t]
        new_p = m.process(p, prev_t)
        if m.name == output_prev_name and isinstance(m, Conjunction) and sum(m.memory.values()) == 1:
            output_prev_tracker = [k for k, v in m.memory.items() if v == 1][0]
        if new_p is not None:
            for new_t in m.targets:
                if new_p == 0 and new_t == "rx":
                    low_rx = True
                queue.appendleft((new_p, new_t, t))
    return n_high_beams, n_low_beams, modules, low_rx, output_prev_tracker


def press_buttons(configs: List[str], n: int, part: str = "a") -> int:
    """
    Press the start button N times and count home many low and high pulses are sent

    :param configs: strings describing each pipeline
    :param n: number of times to press the button
    :param part: the part of puzzle to solve
    :return: n_low * n_high
    """
    module_dict: Dict[str, Module] = {}
    for c in configs:
        m: Module = module_factory(c)
        module_dict[m.name] = m
    module_dict["output"] = Output(name="output", targets=[])
    # init the conjunction modules with memory for inputs
    conjunctions: List[Conjunction] = [v for k, v in module_dict.items() if isinstance(v, Conjunction)]
    for con in conjunctions:
        inputs = [k for k, v in module_dict.items() if con.name in v.targets]
        con.init_memory(inputs)
    button = Button(name="button", targets=["broadcaster"])
    total_h, total_l = 0, 0
    if part == "a":
        for _ in range(n):
            n_h, n_l, low_rx, _, _ = press_button(module_dict, button)
            total_h += n_h
            total_l += n_l
        return total_h * total_l
    else:
        i = 0
        rx_prev = [v for v in module_dict.values() if "rx" in v.targets][0]
        assert isinstance(rx_prev, Conjunction)  # assume that the penultimate module is a conjunction
        rx_prev_states = rx_prev.memory.copy()
        while any([0 in rx_prev_states.values()]):
            _, _, _, _, resp = press_button(module_dict, button, rx_prev.name)
            if resp is not None:
                rx_prev_states[resp] = i + 1
            i += 1
        return math.prod(rx_prev_states.values())


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1

    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return press_buttons(data, 1000)
    else:
        return press_buttons(data, 1000, "b")
