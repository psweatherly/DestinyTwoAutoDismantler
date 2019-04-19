__author__ = "Parker Weatherly"

import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import threading
import os
import logging
import logging.config
import logging.handlers
import json
import datetime
import sys
import traceback

from config import ConfigData
import dismantle_thread

cur_dir = os.getcwd()


class MainWindow(wx.Frame):
    """Primary Window"""

    def __init__(self, *args, **kwargs):
        """Default Constructor for wx.Frame"""
        super(MainWindow, self).__init__(*args, **kwargs)
        icon = PyEmbeddedImage(
            "iVBORw0KGgoAAAANSUhEUgAAAE4AAABECAYAAAAvMQN7AAAD+klEQVR42u1cP08yMRg//6CA"
            "KEhCSBwY3VwcNOED8AHcTEx4+QysjHwBJjYSRhIkzk6EWROjm4sTMXyKvj6XKynH9dq7a3tt"
            "735JAxJp6a/Pvz7PA46TI4dWGI/H6O8BHR4euo/k86OjI/yaMXh5eXE/P94Dfl4oFNDBwUHy"
            "/by+vroTEZPt/E0+J0jVFsvlcmcvpCCQ+yH/J/Ii7XYblcvlnYlpAxY6Pj72v64NVqsVKpVK"
            "rnZgsnzkBO4J3nN6eop+fn649+MSwZo8bBCqkCpqtZpLGGFSYo3RaIS49D/JIn4C05DAAJVL"
            "NDziw6VNJHF4A7Dw1dUVc/Fer4cqlcqOhID0wxgOh8z3Y5UU9fnJfVA16Pr6Wugp+QfMT9vw"
            "5+en+8HC1sd2h3XwsgZ8vu/v7/31wR2LlDZe4sDbRT39NIgjnIu6RRkSF5k48HaqiSOih/SJ"
            "u7y8RHENOcXmIdnqqgVxxWIx9umDE8kscQKckdI9BNpXlleTZOPEbiINicuJY68HkYcuXtUo"
            "Vb27u0PK4yAbiAu9soi+59lAHNed++TkRMp9z1TiwK7RbNseLi4uhEueicTFze7gq03WVTU6"
            "np+ft8wnlT4TiMOCwpN/4wJMmJQ83YmDvYGJ6nQ64hOv1Wo1NoG6Ewd7k5qWDijMGE0ceMyz"
            "szM16X2ogEUNWXQlzsvQqAPEe1HshwrieDPYcOhESks9vBoAVzwUlLWNQj5PpiJK6h8cQWp1"
            "y/V6PQL7wHIWtFYJATWOWPk9WgpcOVjkEbeQQFWNYi8x2e/v7zvzPT4+8pClD2l+taMRGHJ9"
            "ESJtYLNYB8B951QNLxYKHb+/v//ikkerNdzf3zOLydpJmh9w6mFqG1JU9rda7ama1wi0g263"
            "y1RtTxv0Rr/fZ54+raj89va2tXnYLhKemxpThhHHUf3XB6yyHxAiIvBkpb4gBJpMJkY1PnKH"
            "Gk9PT5E31mq1EJlwpZEn/f4pAx8fH1xNfNhwh7Q1bNFsNgO7KYPmFJYaSkvqeLofiY26Kkwm"
            "EnCzixdKcOfVGo2GucQJuh2IqrkaB9WEoZubG/OJ22w2TdUS59gCVepK2EZroEzaZrOZVcQ5"
            "CiXOLpyfn0vthrLOvmGEXeBFedSgJIDxeHh4UCFx1iIPeuPm6mQRV6/X7SVOZjxnRLIyLqCo"
            "E7cTIJOhiApVtdo5JP0ebGadQ05cAucgS11vb2/tjuNkEbdYLOwlbjAYSPlOrA7f/zfu9kB0"
            "POXERR3T6TQTxDle66iwGoOTJXjNM7EHNAYaWXBOiq+vLyRA8jIN7hCF/DEpJ4fjQPBKSl9Q"
            "JR97z/l8npPmB/wGCbRAkE3ZkHL3ekZy5Mgw/gMoRoA7F6WE6gAAAABJRU5ErkJggg==")
        self.SetIcon(icon.GetIcon())

        self.sx = 0
        self.sy = 0 - 20
        self.mainpan = wx.Panel(self)
        self.configs = ConfigData()
        self.online_status = False
        self.goodcolor = self.configs.colors['online']
        self.warningcolor = self.configs.colors['offline']
        self.on_off_flag = threading.Event()
        self.running_flag = threading.Event()
        self.configs.VK_CODE

        self.__init_ui()
        self._start_watcher_thread()

    def _start_watcher_thread(self):
        logging.debug("Creating Key Watcher thread")
        # Start the Key_Watch thread
        self.key_watcher = dismantle_thread.DismantleThread(
            self._gather_settings_data(),
            self.configs,
            self.running_flag,
            self.on_off_flag
        )

        self.key_watcher.daemon = True
        self.key_watcher.start()
        self.running_flag.set()

    def __init_ui(self):
        self.sizers = {}
        self.gui_items = {
            "action_but": {
                "start": wx.Button(
                    self.mainpan,
                    wx.ID_ANY,
                    "Start",
                    name="Start",
                    pos=(self.sx + 113, self.sy + 129),
                    size=(203, 50)
                ),
                "stop": wx.Button(
                    self.mainpan,
                    wx.ID_ANY,
                    "Stop",
                    name="Stop",
                    pos=(self.sx + 113, self.sy + 129),
                    size=(203, 50)
                )
            },
            "online_box": wx.TextCtrl(
                self.mainpan,
                wx.ID_ANY,
                "",
                name="Offline",
                pos=(self.sx + 10, self.sy + 130),
                size=(100, 50),
                style=wx.TE_READONLY
            ),
            "keybinds": {
                "labels": {
                    "amount": wx.StaticText(
                        self.mainpan,
                        wx.ID_ANY,
                        "Amount",
                        pos=(self.sx + 10, self.sy + 25)
                    ),
                    "keybind": wx.StaticText(
                        self.mainpan,
                        wx.ID_ANY,
                        "Keybind",
                        pos=(self.sx + 113, self.sy + 25)
                    )
                },
                "ten": {
                    "amount_txt": wx.TextCtrl(
                        self.mainpan,
                        wx.ID_ANY,
                        self.configs.bind_one['amount'],
                        name="Amount to Dismantle",
                        pos=(self.sx + 10, self.sy + 45),
                        size=(100, 25)
                    ),
                    "txt": wx.ComboBox(
                        self.mainpan,
                        size=(203, 25),
                        choices=self.configs.VK_KEYS,
                        value=self.configs.bind_one['keybind'],
                        style=wx.CB_DROPDOWN | wx.TE_READONLY,
                        name='Keybind 1',
                        pos=(self.sx + 113, self.sy + 45),
                    )
                },
                "twenty_five": {
                    "amount_txt": wx.TextCtrl(
                        self.mainpan,
                        wx.ID_ANY,
                        self.configs.bind_two['amount'],
                        name="Amount to Dismantle",
                        pos=(self.sx + 10, self.sy + 73),
                        size=(100, 25)
                    ),
                    "txt": wx.ComboBox(
                        self.mainpan,
                        size=(203, 25),
                        choices=self.configs.VK_KEYS,
                        value=self.configs.bind_two['keybind'],
                        style=wx.CB_DROPDOWN | wx.TE_READONLY,
                        name='Keybind 2',
                        pos=(self.sx + 113, self.sy + 73),
                    )
                },
                "fifty": {
                    "amount_txt": wx.TextCtrl(
                        self.mainpan,
                        wx.ID_ANY,
                        self.configs.bind_three['amount'],
                        name="Amount to Dismantle",
                        pos=(self.sx + 10, self.sy + 101),
                        size=(100, 25)
                    ),
                    "txt": wx.ComboBox(
                        self.mainpan,
                        size=(203, 25),
                        choices=self.configs.VK_KEYS,
                        value=self.configs.bind_three['keybind'],
                        style=wx.CB_DROPDOWN | wx.TE_READONLY,
                        name='Keybind 3',
                        pos=(self.sx + 113, self.sy + 101),
                    )
                }
            }
        }

        self.gui_items['online_box'].SetBackgroundColour(self.warningcolor)
        self.gui_items['action_but']['stop'].Hide()

        # Binds
        self.Bind(wx.EVT_BUTTON, self.on_start_stop, self.gui_items['action_but']['start'])
        self.Bind(wx.EVT_BUTTON, self.on_start_stop, self.gui_items['action_but']['stop'])

        self.Bind(wx.EVT_COMBOBOX, self._on_bind_one_sel, self.gui_items['keybinds']['ten']['txt'])
        self.Bind(wx.EVT_TEXT, self._on_bind_one_amt, self.gui_items['keybinds']['ten']['amount_txt'])

        self.Bind(wx.EVT_COMBOBOX, self._on_bind_one_sel, self.gui_items['keybinds']['twenty_five']['txt'])
        self.Bind(wx.EVT_TEXT, self._on_bind_one_amt, self.gui_items['keybinds']['twenty_five']['amount_txt'])

        self.Bind(wx.EVT_COMBOBOX, self._on_bind_one_sel, self.gui_items['keybinds']['fifty']['txt'])
        self.Bind(wx.EVT_TEXT, self._on_bind_one_amt, self.gui_items['keybinds']['fifty']['amount_txt'])

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.SetMinSize((200, 115))
        self.SetMaxSize((340, 205))
        dw, dh = wx.DisplaySize()
        w, h = self.GetSize()
        x = (dw / 2) - w
        y = (dh / 2) - h
        self.SetPosition((x - 10 + 1400, y - 45))

        self.Show()

    def on_start_stop(self, e):
        if self.online_status:
            # Switch to Offline
            self.gui_items['online_box'].SetBackgroundColour(self.warningcolor)
            self.gui_items['action_but']['stop'].Hide()
            self.gui_items['action_but']['start'].Show()
            self.SetTitle('Destiny 2 Auto-Dismantler - Offline')
            self.online_status = False

            # Stop the Key_Watch thread
            self.on_off_flag.clear()
        else:
            # Switch to Online
            self.gui_items['online_box'].SetBackgroundColour(self.goodcolor)
            self.gui_items['action_but']['start'].Hide()
            self.gui_items['action_but']['stop'].Show()
            self.SetTitle('Destiny 2 Auto-Dismantler - Online')
            self.online_status = True
            self.on_off_flag.set()

        self.Refresh()

    def _gather_settings_data(self):
        k_one = self.gui_items['keybinds']['ten']['txt'].GetValue()
        k_two = self.gui_items['keybinds']['twenty_five']['txt'].GetValue()
        k_three = self.gui_items['keybinds']['fifty']['txt'].GetValue()

        setting_data = {
            "ten": {
                "amount": int(self.gui_items['keybinds']['ten']['amount_txt'].GetValue()),
                "keybind": {
                    "key": k_one,
                    "key_code": self.configs.VK_CODE[k_one]
                }
            },
            "twenty_five": {
                "amount": int(self.gui_items['keybinds']['twenty_five']['amount_txt'].GetValue()),
                "keybind": {
                    "key": k_two,
                    "key_code": self.configs.VK_CODE[k_two]
                }
            },
            "fifty": {
                "amount": int(self.gui_items['keybinds']['fifty']['amount_txt'].GetValue()),
                "keybind": {
                    "key": k_three,
                    "key_code": self.configs.VK_CODE[k_three]
                }
            }
        }

        return setting_data

    def _on_bind_one_sel(self, e):
        logging.debug("Bind one changed to |{}|".format(self.gui_items['keybinds']['ten']['txt'].GetValue()))
        self.key_watcher.settings['ten']['keybind']['key'] = self.gui_items['keybinds']['ten']['txt'].GetValue()

    def _on_bind_one_amt(self, e):
        if self.gui_items['keybinds']['ten']['amount_txt'].GetValue():
            self.key_watcher.settings['ten']['amount'] = int(self.gui_items['keybinds']['ten']['amount_txt'].GetValue())
        else:
            self.key_watcher.settings['ten']['amount'] = 10

    def _on_bind_two_sel(self, e):
        logging.debug("Bind two changed to |{}|".format(self.gui_items['keybinds']['twenty_five']['txt'].GetValue()))
        self.key_watcher.settings['twenty_five']['keybind']['key'] = self.gui_items['keybinds']['twenty_five']['txt'].GetValue()

    def _on_bind_two_amt(self, e):
        if self.gui_items['keybinds']['twenty_five']['amount_txt'].GetValue():
            self.key_watcher.settings['twenty_five']['amount'] = int(self.gui_items['keybinds']['twenty_five']['amount_txt'].GetValue())
        else:
            self.key_watcher.settings['twenty_five']['amount'] = 25

    def _on_bind_three_sel(self, e):
        logging.debug("Bind three changed to |{}|".format(self.gui_items['keybinds']['fifty']['txt'].GetValue()))
        self.key_watcher.settings['fifty']['keybind']['key'] = self.gui_items['keybinds']['fifty']['txt'].GetValue()

    def _on_bind_three_amt(self, e):
        if self.gui_items['keybinds']['fifty']['amount_txt'].GetValue():
            self.key_watcher.settings['fifty']['amount'] = int(self.gui_items['keybinds']['fifty']['amount_txt'].GetValue())
        else:
            self.key_watcher.settings['fifty']['amount'] = 50

    def _save_settings(self):
        save_settings = {
            "keybinds": {
                "bind1": {
                    "amount": str(self.gui_items['keybinds']['ten']['amount_txt'].GetValue()),
                    "keybind": self.gui_items['keybinds']['ten']['txt'].GetValue()
                },
                "bind2": {
                    "amount": str(self.gui_items['keybinds']['twenty_five']['amount_txt'].GetValue()),
                    "keybind": self.gui_items['keybinds']['twenty_five']['txt'].GetValue()
                },
                "bind3": {
                    "amount": str(self.gui_items['keybinds']['fifty']['amount_txt'].GetValue()),
                    "keybind": self.gui_items['keybinds']['fifty']['txt'].GetValue()
                }
            },
            "colors": {
                "online": [13, 255, 19],
                "offline": [255, 128, 0]
            }
        }

        self.configs.save_config_data(save_settings)

    def on_close(self, e):
        self._save_settings()
        if self.online_status:
            self.on_start_stop(None)

        logging.debug("Closing application...")
        self.Destroy()

# ######################################## #
#        Default Creator Functions         #
# ######################################## #

def logging_setup():
    """Returns the logging setup
    """
    log_config = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple"
            },
            "D2AutoDismantler": {
                "class": "logging.FileHandler",
                "filename": "logs\\D2AutoDismantler.log",
                "level": "DEBUG",
                "formatter": "simple"
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "D2AutoDismantler"],
                "level": "DEBUG"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "D2AutoDismantler"]
        }
    }

    return log_config

def default_config():
    return {
        "keybinds": {
            "bind1": {
                "amount": "10",
                "keybind": "numpad_1"
            },
            "bind2": {
                "amount": "25",
                "keybind": "numpad_2"
            },
            "bind3": {
                "amount": "50",
                "keybind": "numpad_3"
            }
        },
        "colors": {
            "online": [13, 255, 19],
            "offline": [255, 128, 0]
        }
    }

def main():
    log_loc = os.path.join(cur_dir, "logs")
    if not os.path.exists(log_loc):
        os.makedirs(log_loc)

    config_dir_loc = os.path.join(cur_dir, "config")
    if not os.path.exists(config_dir_loc):
        logging.debug("Config folder doesn't exist! Creating folder...")
        os.makedirs(config_dir_loc)

    try:
        with open(os.path.join(cur_dir, 'config/logging_config.json'), 'r') as f:
            logging_config = json.load(f)
    except:
        logging_config = logging_setup()
        with open(os.path.join(cur_dir, 'config/logging_config.json'), 'w') as f:
            config_data = json.dumps(logging_config, sort_keys=True, indent=4, separators=(',', ':'))
            f.write(config_data)

    app_log = logging.getLogger('app')
    logging.config.dictConfig(logging_config)

    time = datetime.datetime.now()
    logging.info("\n"
                 "*********************************\n"
                 "*** Destiny 2 Auto Dismantler ***\n"
                 "*** {} **\n"
                 "*********************************\n".format(time)
                 )

    try:
        with open(os.path.join(cur_dir, 'config/user_configs.json'), 'r') as f:
            test_read = json.load(f)
    except:
        with open(os.path.join(cur_dir, 'config/user_configs.json'), 'w') as f:
            config_data = json.dumps(default_config(), sort_keys=True, indent=4, separators=(',', ':'))
            f.write(config_data)

    app = wx.App(False)
    frame = MainWindow(None, title='Destiny 2 Auto-Dismantler - Offline')
    app.MainLoop()

def uncaught_exception_handler(ex_cls, ex, tb):
    """When QT crashes, it just calls abort() without outlogging what the
    exception was. This catches and displays these exceptions in the logs.
    """
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))

if __name__ == '__main__':
    sys.excepthook = uncaught_exception_handler
    main()

