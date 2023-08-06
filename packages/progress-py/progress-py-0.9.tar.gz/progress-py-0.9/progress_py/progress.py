import os
import threading
import time
from dataclasses import dataclass


@dataclass
class Cursor:
    move_up = "\033[F"
    move_down = "\n"
    move_left = "\r"


class Progress():

    def __init__(self, refresh_time: float) -> None:
        """
            Base class for ProgressBars and Spinners

            Parameters:

                refresh_time (float): The time interval after which progress will be updated
        """
        # The thread for printing in non-blocking fashion
        self.thread: threading.Thread
        # The time after which the progress will be updated
        self.refresh_time = refresh_time

        # Variable to stop the printing thread
        self._stopped = True

    @staticmethod
    def _clean() -> None:
        """ This method will erase everything printed till now """

        # Move the cursor to the start of line above
        print(Cursor.move_left + Cursor.move_up, end='')
        # Print ' ' in the whole line
        print(os.get_terminal_size()[0] * " ", end='')
        # Move the cursor to the left
        print(Cursor.move_left, end='')

    def _print(self) -> None:
        """ Override this method """
        return

    def start(self) -> None:
        """ Start the progress prinitng thread """
        if self._stopped:
            # Create a thread to print progress & start it
            self.thread = threading.Thread(target=self._print, daemon=True)
            self.thread.start()

            # Set __stop to False
            self._stopped = False
        else:
            raise RuntimeError("Cannot start progress if it is already running")

    def stop(self, clean=False) -> None:
        """
            Stop the progress prinitng thread, it will take 2 * refresh_time to stop

            Parameters:

                clean (bool): Whether to erase the progress printed or not
        """

        # Wait for some time to print any unprinted changes
        time.sleep(self.refresh_time)
        # Stop the printing thread
        self._stopped = True

        if clean:
            # Wait for some time before cleaning
            time.sleep(self.refresh_time)
            self._clean()


class ProgressBar(Progress):
    PHASES = [' ', '█']

    def __init__(self, msg: str = '', refresh_time: float = 0.2, size: int = 40) -> None:
        """
            Prints a progress bar to the cli

            Parameters:
                msg (str): The message to be printed, you can use '{progress}' to set the spinner's location

                refresh_time (float): The time interval after which progress will be updated

                size (int): The size of the progress bar (the number of max characters to print)
        """
        super().__init__(refresh_time)

        self.size = size
        self.percent_completed = 0

        self.set_msg(msg)

    def set_msg(self, msg) -> None:
        """
            Set the message to be printed with the progress bar

            Parameters:
                msg (str): The message to be printed, you can use '{progress}' to set the spinner's location
        """
        self.__msg = msg
        if "{progress}" not in self.__msg:
            self.__msg = "{progress} " + self.__msg

    def _print(self) -> None:
        """ Print the progress bar to cli """

        print(Cursor.move_down, end='')
        while not self._stopped:
            progress = "|" + (int(self.percent_completed * self.size/100) * ProgressBar.PHASES[1]).ljust(self.size, ProgressBar.PHASES[0]) + "|"
            self._clean()
            print(self.__msg.format(progress=progress))

            time.sleep(self.refresh_time)


class Spinner(Progress):
    PHASES = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']

    def __init__(self, msg: str = '', refresh_time: float = 0.2) -> None:
        """
            Prints infinite spinning spinner to the cli

            Parameters:
                msg (str): The message to be printed, you can use '{spinner}' to set the spinner's location

                refresh_time (float): The time interval after which progress will be updated
        """
        super().__init__(refresh_time)

        self.counter = 0
        self.set_msg(msg)

    def set_msg(self, msg: str) -> None:
        """
            Set the message to be printed with the spinner

            Parameters:
                msg (str): The message to be printed, you can use '{spinner}' to set the spinner's location
        """
        self.__msg = msg
        if "{spinner}" not in self.__msg:
            self.__msg = "{spinner} " + self.__msg

    def _print(self) -> None:
        """ Print the spinner to cli """

        print(Cursor.move_down, end='')
        while not self._stopped:
            self.counter = (self.counter + 1) % len(Spinner.PHASES)
            self._clean()
            print(self.__msg.format(spinner=Spinner.PHASES[self.counter]))

            time.sleep(self.refresh_time)
