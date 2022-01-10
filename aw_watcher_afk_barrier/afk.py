import logging
import platform
from datetime import datetime, timedelta, timezone
from time import sleep
import os
import Xlib.display
import contextlib


from aw_core.models import Event
from aw_client import ActivityWatchClient

class X11Error(Exception):
    """An error that is thrown at the end of a code block managed by a
    :func:`display_manager` if an *X11* error occurred.
    """
    pass

@contextlib.contextmanager
def display_manager(display):
    """Traps *X* errors and raises an :class:``X11Error`` at the end if any
    error occurred.
    This handler also ensures that the :class:`Xlib.display.Display` being
    managed is sync'd.
    :param Xlib.display.Display display: The *X* display.
    :return: the display
    :rtype: Xlib.display.Display
    """
    errors = []

    def handler(*args):
        """The *Xlib* error handler.
        """
        errors.append(args)

    old_handler = display.set_error_handler(handler)
    try:
        yield display
        display.sync()
    finally:
        display.set_error_handler(old_handler)
    if errors:
        raise X11Error(errors)


from .config import watcher_config

system = platform.system()

if system == "Windows":
    from .windows import seconds_since_last_input
elif system == "Darwin":
    from .macos import seconds_since_last_input
elif system == "Linux":
    from .unix import seconds_since_last_input
else:
    raise Exception("Unsupported platform: {}".format(system))


logger = logging.getLogger(__name__)
td1ms = timedelta(milliseconds=1)




class Settings:
    def __init__(self, config_section):
        # Time without input before we're considering the user as AFK
        self.timeout = config_section["timeout"]
        # How often we should poll for input activity
        self.poll_time = config_section["poll_time"]

        assert self.timeout >= self.poll_time


class AFKWatcher:
    def __init__(self, display, testing=False):
        # Read settings from config
        configsection = "aw-watcher-afk" if not testing else "aw-watcher-afk-testing"
        self.settings = Settings(watcher_config[configsection])

        self.client = ActivityWatchClient("aw-watcher-afk", testing=testing)
        self.bucketname = "{}_{}".format(
            self.client.client_name, self.client.client_hostname
        )
        self.display = display

    def ping(self, afk: bool, timestamp: datetime, duration: float = 0):
        data = {"status": "afk" if afk else "not-afk"}
        e = Event(timestamp=timestamp, duration=duration, data=data)
        pulsetime = self.settings.timeout + self.settings.poll_time
        self.client.heartbeat(self.bucketname, e, pulsetime=pulsetime, queued=True)

    def run(self):
        logger.info("aw-watcher-afk started")

        # Initialization
        sleep(1)

        eventtype = "afkstatus"
        self.client.create_bucket(self.bucketname, eventtype, queued=True)

        # Start afk checking loop
        with self.client:
            self.heartbeat_loop()

    def is_barrier_host_active(self):
        with display_manager(self.display) as dm:
            qp = dm.screen().root.query_pointer()
            child = qp._data.get('child', None)
            if child is 0:
                return True
            # For some reason the child window when the cursor leaves the display using barrier gets this id or higher, no idea how or why, but it seems to work.
            if child.id < 27262976:  # hex for 01a00000
                return True
            return False

    def heartbeat_loop(self):
        afk = False
        while True:
            try:
                if system in ["Darwin", "Linux"] and os.getppid() == 1:
                    # TODO: This won't work with PyInstaller which starts a bootloader process which will become the parent.
                    #       There is a solution however.
                    #       See: https://github.com/ActivityWatch/aw-qt/issues/19#issuecomment-316741125
                    logger.info("afkwatcher stopped because parent process died")
                    break

                now = datetime.now(timezone.utc)
                seconds_since_input = seconds_since_last_input()
                last_input = now - timedelta(seconds=seconds_since_input)
                logger.debug("Seconds since last input: {}".format(seconds_since_input))

                # If no longer AFK
                if afk and seconds_since_input < self.settings.timeout and self.is_barrier_host_active():
                    logger.info("No longer AFK")
                    self.ping(afk, timestamp=last_input)
                    afk = False
                    # ping with timestamp+1ms with the next event (to ensure the latest event gets retreived by get_event)
                    self.ping(afk, timestamp=last_input + td1ms)
                # If becomes AFK
                elif not afk and seconds_since_input >= self.settings.timeout:
                    logger.info("Became AFK")
                    self.ping(afk, timestamp=last_input)
                    afk = True
                    # ping with timestamp+1ms with the next event (to ensure the latest event gets retreived by get_event)
                    self.ping(
                        afk, timestamp=last_input + td1ms, duration=seconds_since_input
                    )
                # Send a heartbeat if no state change was made
                else:
                    if afk:
                        self.ping(
                            afk, timestamp=last_input, duration=seconds_since_input
                        )
                    else:
                        self.ping(afk, timestamp=last_input)

                sleep(self.settings.poll_time)

            except KeyboardInterrupt:
                logger.info("aw-watcher-afk stopped by keyboard interrupt")
                break
