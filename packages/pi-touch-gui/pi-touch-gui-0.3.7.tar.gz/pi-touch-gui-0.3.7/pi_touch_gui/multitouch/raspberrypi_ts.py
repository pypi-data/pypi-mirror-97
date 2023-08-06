# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Touchscreen for the official Raspberry PI 4's 7" touchscreen hardware.

    Based VERY CLOSELY on the Pimoroni hp4ts.py (see the Pimoroni folder)
"""
import errno
import glob
import io
import queue
import select
import struct
import threading
from collections import namedtuple
from pathlib import Path

import pygame

TOUCH_X = 0
TOUCH_Y = 1

TouchEvent = namedtuple('TouchEvent', ('timestamp', 'type', 'code', 'value'))

EV_SYN = 0
EV_ABS = 3

ABS_X = 0
ABS_Y = 1

ABS_MT_SLOT = 0x2f  # 47 MT slot being modified
ABS_MT_POSITION_X = 0x35  # 53 Center X of multi touch position
ABS_MT_POSITION_Y = 0x36  # 54 Center Y of multi touch position
ABS_MT_TRACKING_ID = 0x39  # 57 Unique ID of initiated contact

# Touch events
TS_PRESS = 1
TS_RELEASE = 0
TS_MOVE = 2


class Touch(object):
    def __init__(self, slot, x, y):
        self.slot = slot

        self._x = x
        self._y = y
        self.last_x = -1
        self.last_y = -1

        self._id = -1
        self.events = []
        self._on_move = None
        self._on_press = None
        self._on_release = None
        self._page = None

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page):
        self._page = page

    @property
    def position(self):
        return self.x, self.y

    @property
    def last_position(self):
        return self.last_x, self.last_y

    @property
    def valid(self):
        return self.id > -1

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value != self._id:
            if value == -1 and TS_RELEASE not in self.events:
                self.events.append(TS_RELEASE)
            elif TS_PRESS not in self.events:
                self.events.append(TS_PRESS)

        self._id = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value != self._x and TS_MOVE not in self.events:
            self.events.append(TS_MOVE)
        self.last_x = self._x
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value != self._y and TS_MOVE not in self.events:
            self.events.append(TS_MOVE)
        self.last_y = self._y
        self._y = value

    def handle_events(self):
        """Run outstanding press/release/move events"""
        for event in self.events:
            if event == TS_MOVE and callable(self._on_move):
                self._on_move(event, self)
            if event == TS_PRESS and callable(self._on_press):
                self._on_press(event, self)
            if event == TS_RELEASE and callable(self._on_release):
                self._on_release(event, self)

        self.events = []


class Touches(list):
    @property
    def valid(self):
        return [touch for touch in self if touch.valid]


class Touchscreen(object):
    TOUCHSCREEN_EVDEV_NAME = 'raspberrypi-ts'
    EVENT_FORMAT = str('llHHi')
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

    def __init__(self, device=None, size=None):
        self._device = device or self.TOUCHSCREEN_EVDEV_NAME
        self.size = size or (800, 480)

        self._running = False
        self._thread = None
        self._f_poll = select.poll()
        self._f_device = io.open(self._touch_device(), 'rb', self.EVENT_SIZE)
        self._f_poll.register(self._f_device, select.POLLIN)
        self.position = Touch(0, 0, 0)
        self.touches = Touches([Touch(x, 0, 0) for x in range(10)])
        self._event_queue = queue.Queue()
        self._touch_slot = 0

        self.surface = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

    def _run(self):
        self._running = True
        while self._running:
            self.poll()

    def run(self):
        if self._thread is not None:
            return

        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        if self._thread is None:
            return

        self._running = False
        self._thread.join()
        self._thread = None

    @property
    def _current_touch(self):
        return self.touches[self._touch_slot]

    def close(self):
        self._f_device.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __iter__(self):
        pass

    def _lazy_read(self):
        while self._wait_for_events():
            event = self._f_device.read(self.EVENT_SIZE)
            if not event:
                break
            yield event

    def _get_pending_events(self):
        for event in self._lazy_read():
            (tv_sec, tv_usec, type, code, value) = struct.unpack(
                self.EVENT_FORMAT, event)
            self._event_queue.put(
                TouchEvent(tv_sec + (tv_usec / 1000000), type, code, value))

    def _wait_for_events(self, timeout=2):
        return self._f_poll.poll(timeout)

    def poll(self):

        self._get_pending_events()

        while not self._event_queue.empty():
            event = self._event_queue.get()
            self._event_queue.task_done()

            if event.type == EV_SYN:  # Sync
                for touch in self.touches:
                    touch.handle_events()
                return self.touches

            if event.type == EV_ABS:  # Absolute cursor position
                if event.code == ABS_MT_SLOT:
                    self._touch_slot = event.value

                if event.code == ABS_MT_TRACKING_ID:
                    self._current_touch.id = event.value

                if event.code == ABS_MT_POSITION_X:
                    self._current_touch.x = event.value

                if event.code == ABS_MT_POSITION_Y:
                    self._current_touch.y = event.value

                if event.code == ABS_X:
                    self.position.x = event.value

                if event.code == ABS_Y:
                    self.position.y = event.value

        return []

    def _touch_device(self):
        for evdev in glob.glob("/sys/class/input/event*"):
            try:
                with Path(evdev, 'device', 'name').open(mode='r') as f:
                    if f.read().strip() == self._device:
                        return str(Path('/dev', 'input', Path(evdev).name))
            except IOError as e:
                if e.errno != errno.ENOENT:
                    raise
        raise RuntimeError(
            'Unable to locate touchscreen device: {}'.format(self._device))

    def read(self):
        return next(iter(self))


if __name__ == "__main__":
    """ Test for Touchscreen.
    """
    import signal

    ts = Touchscreen()


    def handle_event(event, touch):
        print(["Release", "Press", "Move"][event],
              touch.slot,
              touch._x,
              touch._y)


    for touch in ts.touches:
        touch._on_press = handle_event
        touch._on_release = handle_event
        touch._on_move = handle_event

    ts.run()

    try:
        signal.pause()
    except KeyboardInterrupt:
        print("Stopping thread...")
        ts.stop()
        exit()
