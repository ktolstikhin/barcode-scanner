import time
from io import StringIO
from threading import Thread, Event, Lock

from evdev import InputDevice, ecodes, categorize


CODE_CHAR_MAP = {
    'KEY_A': "A",
    'KEY_B': "B",
    'KEY_C': "C",
    'KEY_D': "D",
    'KEY_E': "E",
    'KEY_F': "F",
    'KEY_G': "G",
    'KEY_H': "H",
    'KEY_I': "I",
    'KEY_J': "J",
    'KEY_K': "K",
    'KEY_L': "L",
    'KEY_M': "M",
    'KEY_N': "N",
    'KEY_O': "O",
    'KEY_P': "P",
    'KEY_Q': "Q",
    'KEY_R': "R",
    'KEY_S': "S",
    'KEY_T': "T",
    'KEY_U': "U",
    'KEY_V': "V",
    'KEY_W': "W",
    'KEY_X': "X",
    'KEY_Y': "Y",
    'KEY_Z': "Z",
    'KEY_KP0': "0",
    'KEY_KP1': "1",
    'KEY_KP2': "2",
    'KEY_KP3': "3",
    'KEY_KP4': "4",
    'KEY_KP5': "5",
    'KEY_KP6': "6",
    'KEY_KP7': "7",
    'KEY_KP8': "8",
    'KEY_KP9': "9",
    'KEY_NUMERIC_0': "0",
    'KEY_NUMERIC_1': "1",
    'KEY_NUMERIC_2': "2",
    'KEY_NUMERIC_3': "3",
    'KEY_NUMERIC_4': "4",
    'KEY_NUMERIC_5': "5",
    'KEY_NUMERIC_6': "6",
    'KEY_NUMERIC_7': "7",
    'KEY_NUMERIC_8': "8",
    'KEY_NUMERIC_9': "9",
    'KEY_NUMERIC_STAR': "*",
    'KEY_0': "0",
    'KEY_1': "1",
    'KEY_2': "2",
    'KEY_3': "3",
    'KEY_4': "4",
    'KEY_5': "5",
    'KEY_6': "6",
    'KEY_7': "7",
    'KEY_8': "8",
    'KEY_9': "9",
    'KEY_APOSTROPHE': "'",
    'KEY_BACKSLASH': "\\",
    'KEY_COMMA': ",",
    'KEY_DOT': ".",
    'KEY_EQUAL': "=",
    'KEY_GRAVE': "`",
    'KEY_LEFTBRACE': "[",
    'KEY_MINUS': "-",
    'KEY_RIGHTBRACE': "]",
    'KEY_SEMICOLON': ";",
    'KEY_SLASH': "/",
    'KEY_SPACE': " ",
    'KEY_TAB': "\t",
}


class InputDeviceReader(Thread):

    READ_DELAY = 0.01

    def __init__(self, device):
        self.device = InputDevice(device)
        self.sio = StringIO()
        self.lock = Lock()
        self.stop_event = Event()
        super().__init__()

    def read(self):
        return self.raw_read().strip()

    def raw_read(self):

        with self.lock:
            data = self.sio.getvalue()
            self.sio = StringIO()

        return data

    def run(self):

        while not self.stop_event.is_set():
            event = self.device.read_one()

            if event is None:
                time.sleep(self.READ_DELAY)
                continue

            if event.type != ecodes.EV_KEY:
                continue

            e = categorize(event)

            if e.keystate != e.key_up:
                continue

            char = CODE_CHAR_MAP.get(e.keycode, '')

            with self.lock:
                self.sio.write(char)
                self.sio.flush()

    def join(self, timeout=None):
        self.stop_event.set()
        super().join(timeout)

