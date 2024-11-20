import math
from abc import ABC, abstractmethod
from pyautogui import *


class ClickEvent(ABC):
    @abstractmethod
    def exec(self) -> None:
        pass


class SingleClick(ClickEvent):
    def exec(self) -> None:
        click()


class ClickOverTime(ClickEvent):
    dur: float
    interval: float

    def __init__(self, dur: float, interval: float) -> None:
        self.dur = dur
        self.interval = interval

    def exec(self) -> None:
        loops = self.dur / self.interval
        for i in range(math.ceil(loops)):
            sleep(self.interval)
            print(f"CLICK_OVER_TIME: {i}/{loops:2f}")
            click()


class ClickOverTimePatient(ClickOverTime):
    def exec(self) -> None:
        loops = self.dur / self.interval
        for i in range(math.ceil(loops)):
            sleep(self.interval)
            print(f"CLICK_OVER_TIME: {i}/{loops:2f}")
            mouseDown()
            sleep(0.05)
            mouseUp()



class Wait(ClickEvent):
    dur: float

    def __init__(self, dur: float) -> None:
        self.dur = dur

    def exec(self) -> None:
        print(f"WAITING: {self.dur}")

        sleep(self.dur)


class Hold(ClickEvent):
    dur: float

    def __init__(self, dur: float) -> None:
        self.dur = dur

    def exec(self) -> None:
        mouseDown()
        print(f"HOLD: HOLDING FOR {self.dur}")
        sleep(self.dur)
        print("HOLD: RELEASING")
        mouseUp()


class NonLockingHold(Hold):
    def exec(self) -> None:
        print(f"NON LOCKING HOLD: HOLDING FOR {self.dur}")
        for i in range(math.ceil(self.dur)):
            mouseDown()
            sleep(1)
            mouseUp()
            sleep(0.1)


class ClickRunner:
    sequence: list[ClickEvent]
    gap: float

    def __init__(self, sequence: list[ClickEvent], gap: float) -> None:
        self.sequence = sequence
        self.gap = gap

    def run_once(self) -> None:
        """Run the sequence."""
        for seq in self.sequence:
            seq.exec()
            sleep(self.gap)

    def run_loop(self) -> None:
        """Run the sequence, looping infinitely."""
        while True:
            self.run_once()


if __name__ == '__main__':
    click_sequence: list[ClickEvent] = [Hold(4), Wait(55), Hold(17), Wait(4), ClickOverTimePatient(2, 0.5), Wait(5)]
    sleep(3)
    runner = ClickRunner(click_sequence, gap=0.5)
    runner.run_loop()
