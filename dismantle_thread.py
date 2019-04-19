import threading
import win32api as winapi
import win32con as wincon
import time
import logging


class DismantleThread(threading.Thread):
    """
    """
    def __init__(self, keybind_settings, configs, running_flag, on_off_flag):
        self.settings = keybind_settings
        self.configs = configs
        self.running_flag = running_flag
        self.on_off_flag = on_off_flag
        self._setup_logger()
        logging.debug("Key Watcher thread initialized")

        threading.Thread.__init__(self)

    def run(self):
        """
        """
        out_rotation = 0
        in_rotation = 0
        logging.debug("Key Watcher - Run was called")

        while self.running_flag.isSet():
            if out_rotation % 4 == 0:
                logging.debug("Key Watcher - in |Standby|")

            while self.on_off_flag.isSet():
                if in_rotation % 4 == 0:
                    logging.debug("Key Watcher - in |Watching|")
                time.sleep(.3)

                if winapi.GetAsyncKeyState(self.configs.VK_CODE[self.settings['ten']['keybind']['key']]):
                    for x in range(self.settings['ten']['amount']):
                        self._hold_f()

                if winapi.GetAsyncKeyState(self.configs.VK_CODE[self.settings['twenty_five']['keybind']['key']]):
                    for x in range(self.settings['twenty_five']['amount']):
                        self._hold_f()

                if winapi.GetAsyncKeyState(self.configs.VK_CODE[self.settings['fifty']['keybind']['key']]):
                    for x in range(self.settings['fifty']['amount']):
                        self._hold_f()

                in_rotation += 1

            time.sleep(.4)
            out_rotation += 1

    def _hold_f(self):
        """Holds the key 'F' down and then presses backspace and enter to get rid of the chat
        """
        logging.debug("Key Watcher - Holding 'F'")
        winapi.keybd_event(self.configs.VK_CODE['f'], 0, 0, 0)  # F Key
        time.sleep(1)
        winapi.keybd_event(self.configs.VK_CODE['f'], 0, wincon.KEYEVENTF_KEYUP, 0)  # F Key
        time.sleep(.1)
        self._press_key('backspace')
        time.sleep(.1)
        self._press_key('enter')
        time.sleep(.2)

    def _press_key(self, key):
        """Presses and releases a key based on an index given
        
        :param key_code: STRING - A string index relating to a key code
        """
        logging.debug("Key Watcher - Pressing key |{}|".format(key))
        winapi.keybd_event(self.configs.VK_CODE[key], 0, 0, 0)
        time.sleep(.1)
        winapi.keybd_event(self.configs.VK_CODE[key], 0, wincon.KEYEVENTF_KEYUP, 0)

    def _setup_logger(self):
        logging_config = self._logging_setup()
        app_log = logging.getLogger('app')
        logging.config.dictConfig(logging_config)

    def _logging_setup(self):
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
                    "filename": "logs\\D2AutoDismantlerThread.log",
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