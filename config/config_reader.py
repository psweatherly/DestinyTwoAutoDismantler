import json
import logging
import os

cur_dir = os.getcwd()

class ConfigData(object):
    """Class for getting configs for the D2 Dismantler
    """

    def __init__(self):
        logging.debug("Fetching configs")
        self.configs = {
            "keybinds": {}
        }

        with open('config\\user_configs.json', 'r') as conf:
            jdata = json.loads(conf.read())
            self.bind_one = jdata['keybinds']['bind1']
            self.bind_two = jdata['keybinds']['bind2']
            self.bind_three = jdata['keybinds']['bind3']
            self.colors = jdata['colors']

        self.VK_CODE = {
            '0': 0x30,              '1': 0x31,
            '2': 0x32,              '3': 0x33,
            '4': 0x34,              '5': 0x35,
            '6': 0x36,              '7': 0x37,
            '8': 0x38,              '9': 0x39,

            'a': 0x41,              'b': 0x42,
            'c': 0x43,              'd': 0x44,
            'e': 0x45,              'f': 0x46,
            'g': 0x47,              'h': 0x48,
            'i': 0x49,              'j': 0x4A,
            'k': 0x4B,              'l': 0x4C,
            'm': 0x4D,              'n': 0x4E,
            'o': 0x4F,              'p': 0x50,
            'q': 0x51,              'r': 0x52,
            's': 0x53,              't': 0x54,
            'u': 0x55,              'v': 0x56,
            'w': 0x57,              'x': 0x58,
            'y': 0x59,              'z': 0x5A,

            'numpad_0': 0x60,       'numpad_1': 0x61,
            'numpad_2': 0x62,       'numpad_3': 0x63,
            'numpad_4': 0x64,       'numpad_5': 0x65,
            'numpad_6': 0x66,       'numpad_7': 0x67,
            'numpad_8': 0x68,       'numpad_9': 0x69,

            'F1': 0x70,             'F2': 0x71,
            'F3': 0x72,             'F4': 0x73,
            'F5': 0x74,             'F6': 0x75,
            'F7': 0x76,             'F8': 0x77,
            'F9': 0x78,             'F10': 0x79,
            'F11': 0x7A,            'F12': 0x7B,

            'add_key': 0x6B,        'alt': 0x12,
            'backspace': 0x08,      'caps_lock': 0x14,
            'clear': 0x0C,          'ctrl': 0x11,
            'decimal_key': 0x6E,    'del': 0x2E,
            'divide_key': 0x6F,     'down_arrow': 0x28,
            'end': 0x23,            'enter': 0x0D,
            'esc': 0x1B,            'execute': 0x2B,
            'help': 0x2F,           'home': 0x24,
            'ins': 0x2D,            'left_arrow': 0x25,
            'multiply_key': 0x6A,   'page_down': 0x22,
            'page_up': 0x21,        'pause': 0x13,
            'print': 0x2A,          'print_screen': 0x2C,
            'right_arrow': 0x27,    'select': 0x29,
            'separator_key': 0x6C,  'shift': 0x10,
            'spacebar': 0x20,       'subtract_key': 0x6D,
            'tab': 0x09,            'up_arrow': 0x26,

            'num_lock': 0x90,       'scroll_lock': 0x91,
            'left_shift': 0xA0,     'right_shift ': 0xA1,
            'left_control': 0xA2,   'right_control': 0xA3,
            'left_menu': 0xA4,      'right_menu': 0xA5,

            '+': 0xBB,              ',': 0xBC,
            '-': 0xBD,              '.': 0xBE,
            '/': 0xBF,              '`': 0xC0,
            ';': 0xBA,              '[': 0xDB,
            '\\': 0xDC,             ']': 0xDD,
            "'": 0xDE,              '`': 0xC0
        }

        self.VK_KEYS = [
            'backspace',            'tab',
            'clear',                'enter',
            'shift',                'ctrl',
            'alt',                  'pause',
            'caps_lock',            'esc',
            'spacebar',             'page_up',
            'page_down',            'end',
            'home',                 'left_arrow',
            'up_arrow',             'right_arrow',
            'down_arrow',           'select',
            'print',                'execute',
            'print_screen',         'ins',
            'del',                  'help',
            '0',                    '1',
            '2',                    '3',
            '4',                    '5',
            '6',                    '7',
            '8',                    '9',
            'a',                    'b',
            'c',                    'd',
            'e',                    'f',
            'g',                    'h',
            'i',                    'j',
            'k',                    'l',
            'm',                    'n',
            'o',                    'p',
            'q',                    'r',
            's',                    't',
            'u',                    'v',
            'w',                    'x',
            'y',                    'z',
            'numpad_0',             'numpad_1',
            'numpad_2',             'numpad_3',
            'numpad_4',             'numpad_5',
            'numpad_6',             'numpad_7',
            'numpad_8',             'numpad_9',
            'multiply_key',         'add_key',
            'separator_key',        'subtract_key',
            'decimal_key',          'divide_key',
            'F1',                   'F2',
            'F3',                   'F4',
            'F5',                   'F6',
            'F7',                   'F8',
            'F9',                   'F10',
            'F11',                  'F12',
            'num_lock',             'scroll_lock',
            'left_shift',           'right_shift ',
            'left_control',         'right_control',
            'left_menu',            'right_menu',
            '+',                    ',',
            '-',                    '.',
            '/',                    '`',
            ';',                    '[',
            '\\',                   ']',
            "'",                    '`'
        ]

        self.VK_VALUES = []
        for key in self.VK_CODE:
            self.VK_VALUES.append(self.VK_CODE[key])

        self.bind_one['keycode'] = self.VK_CODE[self.bind_one['keybind']]
        self.bind_two['keycode'] = self.VK_CODE[self.bind_two['keybind']]
        self.bind_three['keycode'] = self.VK_CODE[self.bind_three['keybind']]

        logging.debug("Configs fetched successfully")

    def save_config_data(self, settings):
        logging.debug("Saving config settings")
        beatified_data = json.dumps(settings, sort_keys=True, indent=4, separators=(',', ':'))
        with open('config\\user_configs.json', 'w') as conf:
            conf.write(beatified_data)

