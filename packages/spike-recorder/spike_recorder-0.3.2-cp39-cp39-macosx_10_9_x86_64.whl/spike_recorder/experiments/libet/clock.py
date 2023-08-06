#!/usr/bin/env python3
"""
An implementation of the Libet clock as a QtWidget. This is a heavily
modified version of the Qt5 example forked from:

# forked from https://github.com/baoboa/pyqt5/blob/master/examples/widgets/analogclock.py

The original license is copied below

"""

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import math
import sys
import typing
import numpy as np

from PyQt5.QtCore import QPoint, Qt, QDateTime, QTime, QTimer, QSettings, QRect, QRectF, pyqtSignal
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class LibetClock(QWidget):
    """
    A Widget that displays a rotating clock dial. The API provides for stopping, starting, and resetting the clock.
    It also provides the ability to select a time by clicking on the surface of the clock dial
    """

    # A polygon for the clock hand, just a line really.
    minuteHand = QPolygon([
        QPoint(0, 0),
        QPoint(0, 0),
        QPoint(0, -80),
        QPoint(0, -80)
    ])

    # Some colors we might need.
    handColor = QColor(0, 0, 0)
    minuteColor = QColor(57, 57, 57)
    whiteShadowColor = QColor(128, 128, 128)
    darkShadowColor = QColor(20, 20, 20)
    highlightColor = QColor(255, 0, 0)
    selectColor = QColor(49, 20, 255)
    smokeBackgroundColor = QColor(255, 255, 255)
    rubyColor = QColor(255, 255, 255)
    textColor = QColor(0, 0, 0)
    textPanelColor = QColor(255, 255, 255)

    # A signal that notifies when the time selection has changed.
    selectChange = pyqtSignal()

    def check_update(self):
        """
        Check if we need to update and do it if needed.

        Returns:
            None
        """
        self.update()

    def rotated_point(self, x, y, degr) -> typing.Tuple[int]:
        """
        Rotate a point with an angle.

        Args:
            x: The x coordinate
            y: The y coordinat
            degr: The angle to rotate by in degrees.

        Returns:
            A integer 2-tuple containing the rotated point coordinates.
        """
        theta = degr * math.pi / 180
        s = math.sin(theta)
        c = math.cos(theta)
        return int(x * c - y * s), int(x * s + y * c)

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        self.settings.sync()
        super(LibetClock, self).closeEvent(event)

    def __init__(self, parent=None, showFrame=False, windowSize=None):
        super(LibetClock, self).__init__(parent)

        self._rotations_per_minute = 5.0

        self._clock_cursor_pos = None
        self._clock_selection = None
        self._selected_time = None
        self._select_enabled = False

        self._start_time = None
        self._stop_time = None

        self._clock_stopped = True

        self.setMouseTracking(True)

        # Setup a time to invoke the render function
        timer = QTimer(self)
        timer.timeout.connect(self.check_update)
        timer.start(5)

        appIcon = QIcon.fromTheme("applications-accessories")
        self.setWindowIcon(appIcon)

        self.settings = QSettings('ToshihiroKamiya', 'Analog Clock')
        if windowSize is None:
            geometry = self.settings.value('geometry', None)
            if geometry is not None:
                self.restoreGeometry(geometry)
            else:
                windowSize = 100
                self.resize(windowSize, windowSize)
        else:
            if windowSize < 100:
                windowSize = 100
            self.resize(windowSize, windowSize)

        font = QFont()
        font.setPointSize(12)
        self.font = font

        font = QFont(font)
        font.setPointSize(13)
        self.rubyFont = font

        font = QFont(font)
        font.setPointSize(6)
        self.selFont = font


    @property
    def clock_stopped(self) -> bool:
        """
        Is the clock in a stopped state or not.

        Returns:
            True for stopped, False for running.
        """
        return self._clock_stopped

    @property
    def selected_time(self) -> int:
        """
        The currently selected time on the clock dial, None is no time is selected.

        Returns:
            The currently selected time on the clock dial, None is no time is selected. The time returned is
            always in milliseconds.
        """

        return self._selected_time

    @property
    def rotations_per_minute(self) -> float:
        """
        The number of rotations the clock should make per minute.

        Returns:
            The rotations per minute.
        """
        return self._rotations_per_minute

    @rotations_per_minute.setter
    def rotations_per_minute(self, value: float):
        """
        Set the number of rotations the clock should make per minute.

        Args:
            value: The number of rotations the clock should make per minute.

        Returns:
            None
        """
        self._rotations_per_minute = float(value)

    @property
    def select_enabled(self) -> bool:
        """
        Is time selection with mouse enabled?

        Returns:
            True for yes, False for No.
        """
        return self._select_enabled

    @select_enabled.setter
    def select_enabled(self, value: bool):
        """
        Is time selection with the mouse enabled?

        Args:
            value: True for yes, False for No.
        """

        if type(value) is not bool:
            return ValueError("Can't set select_enable to non-bool type.")

        self._select_enabled = value

        if not self._select_enabled:
            self._selected_time = None
            self._clock_selection = None

    def reset_clock(self):
        """
        Reset the clock. This moves the hand to the 12 position and stops the clock.

        Returns:
            None
        """
        self._start_time = None
        self._stop_time = None
        self._clock_stopped = True
        self._clock_selection = None
        self._selected_time = None
        self.selectChange.emit()

    def start_clock(self):
        """
        Start running the clock. This starts movement of the hand.

        Returns:
            None
        """
        self._clock_stopped = False

    def stop_clock(self):
        """
        Stop the clock in its current position.

        Returns:
            None
        """
        self._clock_stopped = True
        self._stop_time = QDateTime.currentDateTime().time()

    def msecs_elapsed(self) -> int:
        """
        Get the amount of time elapsed since the clock was first started. If the clock has been stopped
        calculate the time between start and stop time.

        Returns:
            The elapsed number of milliseconds. Returns 0 when the clock has not been started.
        """
        if self._start_time is None:
            return 0
        elif self._stop_time is None:
            return self._start_time.msecsTo(QDateTime.currentDateTime().time())
        else:
            return self._start_time.msecsTo(self._stop_time)

    def paintEvent(self, event):
        """
        Render the clock. Invoked periodicaly by a QTimer setup in the constructor.

        Args:
            event: The event signal.

        Returns:
            None
        """

        side = min(self.width(), self.height())

        if self._start_time is None and not self._clock_stopped:
            self._start_time = QDateTime.currentDateTime().time()

        # Compute the hand rotation based on the elapsed milliseconds
        rotation = math.fmod(self._rotations_per_minute * 360.0 * (self.msecs_elapsed() / 60000.0), 360.0)

        # Start all the drawing.
        handColor = self.handColor
        whiteShadowPen = QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        hlPen = QPen(self.highlightColor)
        hlPen.setJoinStyle(Qt.MiterJoin)
        hlPen.setWidthF(0.9)

        selPen = QPen(self.selectColor)
        selPen.setJoinStyle(Qt.MiterJoin)
        selPen.setWidthF(1.5)

        darkShadowPen = QPen(self.darkShadowColor)
        darkShadowPen.setJoinStyle(Qt.MiterJoin)
        darkShadowPen.setWidthF(0.9)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QPoint(0, 0), 99, 99)

        # Draw the 5 minute tick marks
        painter.setPen(whiteShadowPen)
        painter.setFont(self.rubyFont)
        painter.setBrush(QBrush(handColor))
        for i in range(0, 12):
            angle = i * 360/12
            x, y = self.rotated_point(0, -92, angle)
            painter.drawEllipse(x - 3, y - 3, 6, 6)

        # Draw the 1 minute tick marks
        painter.setPen(self.rubyColor)
        painter.setBrush(QBrush(self.minuteColor))
        for j in range(0, 60):
            if j % 5 != 0:
                angle = j * 360/60
                x, y = self.rotated_point(0, -92, angle)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # Draw hour numbers
        painter.setPen(darkShadowPen)
        hour_nums = [12] + list(range(1, 12))
        for i in range(0, 12):
            x, y = self.rotated_point(0, -76, i * 360 / 12)
            painter.drawText(QRect(x - 10, y - 10, 20, 20), Qt.AlignCenter, "%d" % (hour_nums[i]))

        # Draw the mouse cursor highlight
        if self._clock_cursor_pos is not None and self._select_enabled:
            painter.setPen(hlPen)
            painter.drawEllipse(int(self._clock_cursor_pos[0] - 1), int(self._clock_cursor_pos[1] - 1), 2, 2)

        if self._clock_selection is not None and self._select_enabled:
            selPen.setWidthF(1.5)
            painter.setPen(selPen)
            painter.drawEllipse(int(self._clock_selection[0] - 1), int(self._clock_selection[1] - 1), 2, 2)
            selPen.setWidthF(.2)
            painter.setPen(selPen)
            painter.setFont(self.selFont)
            painter.drawText(QRect(50, -100, 40, 20), Qt.AlignCenter,
                             "%d ms" % (self._selected_time))


        # draw hand
        painter.setPen(darkShadowPen)
        painter.setBrush(QBrush(self.minuteColor))
        painter.save()
        painter.rotate(rotation)
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        painter.end()

    def get_mouse_clock_pos(self, x, y) -> typing.Union[None, np.array]:
        """
        Get the current position on the surface of the clock dial based on x,y mouse
        coordinates. This function accepts pure screen coordinates. That is, inside the render
        function there is a coordinate transformation (scale, and translate to center origin).
        This function takes coordinates without this transformation and takes it into account.

        Args:
            x: The x coordinate of the mouse. This is in pure screen coordinates.
            y: The y coordinate of the mouse. This is in pure screen coordinates,

        Returns:
            A 2 element 1D numpy array containing the coordinates on the clock dial. The coordinates
            are in the transformed space. None is returned if the mouse is too far from the surface.
        """

        if self._select_enabled:
            side = min(self.width(), self.height())
            scale = (200.0 / side)

            # Unscale the radius of the clock. The painter coordinate system is scaled
            # and translated in paintEvent
            radius = (1 / scale) * 92

            # Find the closest point on the clock dial surface from the mouse location
            p = np.array([x, y])
            c = np.array([self.width() / 2, self.height() / 2])
            v = p - c

            # Get the nearest point on the clock surface
            clock_cursor_pos = (c + radius * (v / np.linalg.norm(v)))

            # We need to scale and transform the clock cursor position because of how the painter
            # coordinate system is setup in paintEvent. Maybe this should be done in paint event
            # I guess.
            clock_cursor_pos = (clock_cursor_pos - c) * scale

            # If the mouse isn't close enough to the surface, don't display it.
            if np.linalg.norm(clock_cursor_pos - (v * scale)) > 8.0:
                return None
            else:
                return clock_cursor_pos

    def mouseMoveEvent(self, event):
        """
        In select mode, track the users mouse movement on the dial
        """
        self._clock_cursor_pos = self.get_mouse_clock_pos(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        """
        In select mode, allow the user to select the currrent time.
        """

        if self._select_enabled:
            self._clock_selection = self.get_mouse_clock_pos(event.x(), event.y())

            if self._clock_selection is not None:
                # Figure out what time has been selected
                angle = math.degrees(math.atan2(self._clock_selection[1], self._clock_selection[0])) + 90.0

                if angle < 0:
                    angle = 360 + angle

                self._selected_time = int((60000.0 * angle) / (self._rotations_per_minute * 360.0))

                # If the clock has been running for more than 1 revolution, add the N revolutions to the selected
                # time.
                rotation = self._rotations_per_minute * 360.0 * (self.msecs_elapsed() / 60000.0)
                num_revolutions = math.floor(rotation / 360.0)
                self._selected_time = int(self._selected_time + (60000.0 / self._rotations_per_minute) * num_revolutions)

            else:
                self._selected_time = None

            self.selectChange.emit()


if __name__ == "__main__":
    import sys

    __doc__ = """Show wall clock.

Usage: {argv0} [Options]

Options:
  -f        Show window frame.
  -s SIZE   Set window size.
""".format(argv0=sys.argv[0])

    optionShowFrame = True
    optionWindowSize = None
    argv = sys.argv[1:]
    while argv:
        if argv[0] == '-f':
            optionShowFrame = True
        elif argv[0].startswith('-s'):
            if len(argv[0]) > 2:
                s = int(argv[0][2:])
            else:
                s = int(argv[1])
                del argv[0]
            optionWindowSize = s
        elif argv[0] == '-h':
            print(__doc__)
            sys.exit(0)
        else:
            sys.exit("error: too many arguments / unknown option: %s" % argv[0])
        del argv[0]

    argv.insert(0, sys.argv[0])
    app = QApplication(argv)
    clock = LibetClock(showFrame=optionShowFrame, windowSize=optionWindowSize)
    clock.show()
    sys.exit(app.exec_())

