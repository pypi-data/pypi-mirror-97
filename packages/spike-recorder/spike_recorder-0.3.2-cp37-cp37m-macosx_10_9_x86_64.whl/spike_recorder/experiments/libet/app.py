# -*- coding: utf-8 -*-

import os
import argparse
import sys

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtWidgets, QtCore

from spike_recorder.experiments.app_runner import run_app
from spike_recorder.experiments.libet.libet_ui import Ui_Libet
from spike_recorder.experiments.libet.instructions_ui import Ui_dialog_instructions
from spike_recorder.experiments.libet.data import LibetData
from spike_recorder.client import SpikeRecorder


# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class IntroDialog(QtWidgets.QDialog, Ui_dialog_instructions):
    """
    The intro instructions dialog box. Allows selecting the output file.
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.button_browse.clicked.connect(self.get_directory)

        # Lets prepopulate the output file name with something
        index = 1
        filename = f"libet_output{index}.csv"
        while os.path.isfile(filename):
            index = index + 1
            filename = f"libet_output{index}.csv"

        self.textbox_file.setText(filename)

    def reject(self):
        """
        If the user clicks cancel, we can't proceed, exit the app.

        Returns:
            None
        """
        self.parent().close()

    def get_directory(self):
        dialog = QtWidgets.QFileDialog()
        foo_dir = dialog.getExistingDirectory(self, 'Select an output directory')

        # Add a slash at the end
        foo_dir = foo_dir + '/'

        self.textbox_file.setText(foo_dir)


class LibetMainWindow(QtWidgets.QMainWindow, Ui_Libet):
    """
    The main application class for the Libet experiment.
    """

    def __init__(self, spike_record: bool = False, clock_hz: float = 1.0,
                 num_trials_phase1: int = 20, num_trials_phase2: int = 20):

        self.spike_record = spike_record
        self.clock_hz = clock_hz
        self.num_trials_phase1 = num_trials_phase1
        self.num_trials_phase2 = num_trials_phase2

        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        # adding action to a buttons
        self.button_next.clicked.connect(self.next_trial_click)
        self.button_retry.clicked.connect(self.retry_trial_click)

        # Don't let the buttons get focus so they can't be pressed with the space bar. This allows
        # us to press then on keyPress events rather than release events.
        self.button_next.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.button_retry.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.data = LibetData()

        self.output_filename = None

        # The first sent of NUM_PRACTICE_TRIALS do not ask the urge time.
        self.urge_mode = False

        self.clock_widget.selectChange.connect(self.on_clock_select_change)

        # Set the clock speed.
        self.clock_widget.rotations_per_minute = self.clock_hz * 60.0

        # Launch the spike recorder if needed
        if self.spike_record:
            self.record_client = SpikeRecorder()
            self.record_client.launch()
            self.record_client.connect()

        # Move the window over a bit to make room for the SpikeRecorder app
        self.move(10, 10)

    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        trial_txt = f"Trial: {self.data.num_trials+1}"

        if self.clock_widget.select_enabled:
            self.label_status.setText(f"{trial_txt} - Click the time you felt the urge.")
        else:
            self.label_status.setText(trial_txt)

    def restart_trial(self):
        """
        Restart the current trial.

        Returns:
            None
        """
        self.clock_widget.reset_clock()
        self.clock_widget.start_clock()
        self.button_next.setText("Stop")
        self.button_next.setStyleSheet("background-color : red;")
        self.button_retry.setEnabled(False)
        self.button_next.setEnabled(True)
        self.clock_widget.select_enabled = False

        self.update_status()

    def stop_trial(self):
        """
        Stop the trial.

        Returns:

        """
        self.clock_widget.stop_clock()
        self.button_next.setText("Next Trial")
        self.button_next.setStyleSheet("")
        self.button_retry.setEnabled(True)

        # If this is urge mode, make sure they can't go to the next trial without selecting
        # and urge time.
        if self.urge_mode:
            self.button_next.setEnabled(False)
            self.clock_widget.select_enabled = True
            self.update_status()

        # Check if we have finished our first set of trials, if so, now we need to enter
        # the secondary mode where we ask for the urge time
        if (self.data.num_trials+1) == self.num_trials_phase1:
            self.urge_mode = True
            self.clock_widget.select_enabled = True

            QtWidgets.QMessageBox.about(self, "Instructions - Part 2",
                                        f"For the next {self.num_trials_phase2} trials, stop the clock whenever you "
                                        f"like. After each trial, click the time on the clock when you first felt the "
                                        f"urge to stop the clock. ")

    def next_trial_click(self):
        """
        When the next trial button is clicked. This can also be the stop clock button when the trial is running.

        Returns:
            None
        """

        if not self.clock_widget.clock_stopped:
            self.record_event_marker(f"Trial {self.data.num_trials}: Stop")
            self.stop_trial()
        else:

            # Store the trial's data, unless the clock hasn't been started.
            if self.clock_widget.msecs_elapsed() > 0:
                self.data.add_trial(stop_time_msecs=self.clock_widget.msecs_elapsed(),
                                    urge_time_msecs=self.clock_widget.selected_time)

                self.record_event_marker(f"Trial {self.data.num_trials}: Next")

                # Dump the data back out to file. We will just dump everything back out over and over again
                # so that if the user stops half way through, they have part of their data.
                if self.output_filename is not None:
                    self.data.to_csv(self.output_filename)
                else:
                    logging.warning("Output filename is not defined, results are not being saved.")
            else:
                self.record_event_marker(f"Trial {self.data.num_trials}: Next")

            # If we have enough data then we are done!
            if self.data.num_trials == (self.num_trials_phase1 + self.num_trials_phase2):

                if self.spike_record:
                    self.record_client.stop_record()

                msg = QtWidgets.QMessageBox(parent=self)
                msg.setText("Experiment Complete!")
                msg.setWindowTitle("Done")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()

                self.close()

            self.restart_trial()

    def retry_trial_click(self):
        """
        Retry the trial, don't save the last trials results.

        Returns:
            None
        """
        self.record_event_marker(f"Trial {self.data.num_trials}: Retry")
        self.restart_trial()

    def on_clock_select_change(self):
        """
        Triggered anytime the user selects a time on the clock.
        """

        selected_time = self.clock_widget.selected_time

        # If we are in urge mode, and the user has not selected a urge time, do not allow next trial
        # until they have done so.
        if self.urge_mode:
            if selected_time is not None:
                self.button_next.setEnabled(True)
            else:
                # Don't turn of the next\stop button unless the clock is stopped!
                self.button_next.setEnabled(False)

    def closeEvent(self, event):
        if self.spike_record:
            self.record_client.shutdown()

        sys.exit(0)

    def record_event_marker(self, marker: str):
        """
        A little helper function to push event markers to the Spike Recorder app if it is
        running.

        Args:
            marker: The text for the marker.

        Returns:
            None
        """
        if self.spike_record:
            self.record_client.push_event_marker(marker)

    def keyPressEvent(self, event):
        """
        Stop and start the clock on press of space bar.

        Args:
            event: The keyboard press event.

        Returns:
            None
        """

        # If the space bar has been pressed and this isn't an auto repeat, to avoid multiple presses if held down.
        if event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat() and self.button_next.isEnabled():
            self.next_trial_click()

        # If the space bar has been pressed and this isn't an auto repeat, to avoid multiple presses if held down.
        if event.key() == QtCore.Qt.Key_R and not event.isAutoRepeat() and self.button_retry.isEnabled():
            self.retry_trial_click()

        event.accept()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--spike-record', action='store_true',
                        default=False,
                        help='Launch Backyard Brains Spike Recorder in background. Default is do not run.')
    parser.add_argument("--num-trials-phase1", type=int, default=20,
                         help="The number of trials to conduct for phase one. Default is 20.")
    parser.add_argument("--num-trials-phase2", type=int, default=20,
    help="The number of trials to conduct for phase two, in which time of urge is asked. Default is 20.")
    parser.add_argument('--clock_hz', type=float, default=1.0,
                        help='The number of full rotations the clock makes per second. Default is 1 but can '
                             'be set lower than 1.')

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    ui = LibetMainWindow(**vars(args))
    intro_d = IntroDialog(parent=ui)
    run_app(app=app, ui=ui, intro_d=intro_d)


if __name__ == "__main__":
    main()

