#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

# Default python packages
import logging
import os
import time

# pip installed python packages
from pynput.keyboard import Key, Controller


class WorkLogin:
    """Class that performs functions for login"""

    def __init__(self, conf_path=os.path.join(os.path.expanduser("~"),
                                              ".work_login.conf")):
        """Saves config file location"""

        print("I GOT INITIALIZED")
        self.conf_path = conf_path
        self.keyboard = Controller()

    def login(self):
        """Logs user in through terminal"""

        # Configures config file if not done so already
        self.configure()
        # Opens a terminal
        os.system("gnome-terminal")
        time.sleep(1)
        with open(self.conf_path, "r") as f:
            for cmd in f:
                self._run_cmd(cmd)

    def configure(self):
        """Configures file that will contain commands to run"""

        # I know I could be using proper logging
        # But this is supposed to be a quick package
        if not os.path.exists(self.conf_path):
            logging.info("Configuring work login")
            cmds = [input("Next command, or hit enter:\n")]
            # Ugh needs 3.6 compatibility, but with 3.8 could use walrus here
            while cmds[-1] != "":
                cmds.append(input("Next command, or hit enter:\n"))
            with open(self.conf_path, "w+") as f:
                f.write("\n".join(cmds))

    def _run_cmd(self, cmd):
        """Runs a command slowly so as not to error"""

        new_cmd = cmd.replace("\n", "")
        for c in new_cmd:
            self._type_key(c)
        self._type_key(Key.enter)
        time.sleep(.1)

    def _type_key(self, key):
        """Types a key with a delay"""

        self.keyboard.press(key)
        time.sleep(.005)
        self.keyboard.release(key)
        time.sleep(.005)
