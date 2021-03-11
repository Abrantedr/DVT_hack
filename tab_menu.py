import time                 # time.sleep
import threading            # threading.Thread, threading.Event
import tkinter as tk        # tk.BOTH
from tkinter import ttk     # ttk.Notebook

# Tab imports
from tab import MainTab, TreeTab, IOTab, PDOTab


class TabMenu(ttk.Notebook):    # self -> ttk.Notebook
    def __init__(self, root, controller, **kwargs):
        super().__init__(root, **kwargs)
        self.controller = controller

        # Create tabs
        self.tab_main = MainTab(self, controller)   # Sends controller to main tab
        self.tab_tree = TreeTab(self)
        self.tab_io = IOTab(self)
        self.tab_pdo = PDOTab(self)

        # Add tabs to notebook
        self.add(self.tab_main, text="Main")
        self.add(self.tab_tree, text="Tree")
        self.add(self.tab_io, text="Input / Output")
        self.add(self.tab_pdo, text="TPDO / RPDO")

        # Place the tab menu
        self.pack(fill=tk.BOTH, expand=True)

        # Selecting a tab triggers events
        self.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        # Set thread conditions
        self.thread_stop = threading.Event()

        # Set on tab selection conditions
        self.__tab_state = (True, False, False, False)

        # Start SDO request thread
        self.main_tab_sdo_thread = threading.Thread(target=self.sdo_request, name="SDO Requests")
        self.main_tab_sdo_thread.start()

    def sdo_request(self):
        while True:
            # Keep sending these specific SDOs while we are in Main tab
            if self.__tab_state[0]:
                self.controller.write(0x40, 0x5110, 0x00)
                # Another SDO
                # Another SDO
            if self.__tab_state[1]:
                pass
                # Another SDO
                # Another SDO
            if self.__tab_state[2]:
                pass
                # Another SDO
                # Another SDO
            if self.__tab_state[3]:
                pass
                # Another SDO
                # Another SDO

            # Check if we can close the thread
            if self.thread_stop.is_set():
                break

            time.sleep(0.5)

    def on_tab_changed(self, event):
        tab = event.widget.tab('current')['text']
        if tab == "Main":
            self.__tab_state = (True, False, False, False)
        elif tab == "Tree":
            self.__tab_state = (False, True, False, False)
        elif tab == "Input / Output":
            self.__tab_state = (False, False, True, False)
        elif tab == "TPDO / RPDO":
            self.__tab_state = (False, False, False, True)
