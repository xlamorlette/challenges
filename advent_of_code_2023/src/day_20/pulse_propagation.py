import abc
from collections import deque
from dataclasses import dataclass
from enum import Enum


class PulseType(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Pulse:
    pulse_type: PulseType
    sender: str
    destination: str

    def __repr__(self):
        return f"{self.sender} -{self.pulse_type.name}-> {self.destination}"


class Module:
    name: str
    destinations: list[str]

    def __init__(self,
                 name: str,
                 destinations: list[str]):
        self.name = name
        self.destinations = destinations

    @abc.abstractmethod
    def handle_pulse(self,
                     pulse: Pulse) -> list[Pulse]:
        pass


class Broadcaster(Module):
    def handle_pulse(self,
                     pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.pulse_type, self.name, destination) for destination in self.destinations]


class FlipflopState(Enum):
    OFF = 0
    ON = 1


class Flipflop(Module):
    state: FlipflopState = FlipflopState.OFF

    def handle_pulse(self,
                     pulse: Pulse) -> list[Pulse]:
        if pulse.pulse_type == PulseType.HIGH:
            return []
        self.state = FlipflopState.ON if self.state == FlipflopState.OFF else FlipflopState.OFF
        pulse_type = PulseType.HIGH if self.state == FlipflopState.ON else PulseType.LOW
        return [Pulse(pulse_type, self.name, destination) for destination in self.destinations]


class Conjunction(Module):
    most_recent_pulse_received: dict[str, PulseType]

    def __init__(self,
                 name: str,
                 destinations: list[str]):
        super().__init__(name, destinations)
        self.most_recent_pulse_received = {}

    def add_sender(self,
                   module_name: str):
        self.most_recent_pulse_received[module_name] = PulseType.LOW

    def handle_pulse(self,
                     pulse: Pulse) -> list[Pulse]:
        self.most_recent_pulse_received[pulse.sender] = pulse.pulse_type
        pulse_type = PulseType.LOW \
            if all(pulse_type == PulseType.HIGH for pulse_type in self.most_recent_pulse_received.values()) \
            else PulseType.HIGH
        return [Pulse(pulse_type, self.name, destination) for destination in self.destinations]


class Network:
    modules: dict[str, Module]
    nb_low_pulses: int = 0
    nb_high_pulses: int = 0

    def __init__(self,
                 lines: list[str]):
        self.modules = {}
        for line in lines:
            prefix_and_name, destinations_str = line.split(" -> ")
            destinations: list[str] = destinations_str.split(", ")
            if prefix_and_name == "broadcaster":
                self.modules[prefix_and_name] = Broadcaster(prefix_and_name, destinations)
                continue
            name: str = prefix_and_name[1:]
            if prefix_and_name[0] == "%":
                self.modules[name] = Flipflop(name, destinations)
            else:
                self.modules[name] = Conjunction(name, destinations)
        for module in self.modules.values():
            for destination in module.destinations:
                if destination not in self.modules:
                    continue
                destination_module = self.modules[destination]
                if isinstance(destination_module, Conjunction):
                    destination_module.add_sender(module.name)

    def get_1000_button_pushes_pulses_product(self) -> int:
        self.nb_low_pulses = 0
        self.nb_high_pulses = 0
        for _nb_button_pushes in range(1000):
            self.push_button()
        return self.nb_low_pulses * self.nb_high_pulses

    def push_button(self):
        pulses_queue = deque([Pulse(PulseType.LOW, "button", "broadcaster")])
        while pulses_queue:
            pulse = pulses_queue.popleft()
            if pulse.pulse_type == PulseType.LOW:
                self.nb_low_pulses += 1
            else:
                self.nb_high_pulses += 1
            if pulse.destination not in self.modules:
                continue
            resulting_pulses = self.modules[pulse.destination].handle_pulse(pulse)
            pulses_queue.extend(resulting_pulses)


def compute_pulses_number_product(lines: list[str]) -> int:
    network = Network(lines)
    return network.get_1000_button_pushes_pulses_product()
