# -*- coding: utf-8 -*-
import sys
import os
import time

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from spike_recorder.experiments.app_runner import run_app
from spike_recorder.experiments.iowa.instructions_ui import Ui_dialog_instructions
from spike_recorder.experiments.iowa.iowa_ui import Ui_main_window
from spike_recorder.experiments.iowa.win_message_ui import Ui_Dialog as Ui_win_message
from spike_recorder.experiments.iowa.deck import Deck
from spike_recorder.experiments.iowa.data import IowaData
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
        filename = f"iowa_output{index}.csv"
        while os.path.isfile(filename):
            index = index + 1
            filename = f"iowa_output{index}.csv"

        self.textbox_file.setText(filename)

    def reject(self):
        """
        If the user clicks cancel, we can't proceeed, exit the app.

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


class WinDialog(QtWidgets.QDialog, Ui_win_message):
    """
    A modal dialog that displays wins and losses from a deck pull and pauses the
    experiement for a bit.
    """

    def __init__(self, parent=None, deck_index=0, win_amount=0, loss_amount=0, delay_seconds=3):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.label.setText(f'<html><head/><body><p style="color:#0571b0">Win: ${win_amount}</p>'
                           f'<p style="color:#ca0020">Loss: ${loss_amount}</p></body></html>')

        self.lcdNumber.display(delay_seconds)

        # Setup a time to invoke the render function and see if its time to close
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.setWindowTitle(f"Deck {deck_index+1} Pull - Winnings and Losses")

    def update(self):
        """
        Update the countdown timer, close the dialog when it is done.

        Returns:
            None
        """
        self.lcdNumber.display(self.lcdNumber.intValue() - 1)

        if self.lcdNumber.intValue() == 0:
            self.done(0)


class IowaMainWindow(QtWidgets.QMainWindow, Ui_main_window):
    """
    The main window GUI for the Iowa Gambling task experiment.
    """

    # How long to pause between deck pulls
    DELAY_SECS = 3

    def __init__(self, total_deck_pulls: int = 100, spike_record: bool = False):

        self.spike_record = spike_record
        self.total_deck_pulls = total_deck_pulls

        # And estimate of the max winnings, this is probably wrong but I need
        # something for the maxes on the progress bars.
        self.max_winnings = self.total_deck_pulls * 350
        self.max_losses = self.total_deck_pulls * 350

        # The starting winnings
        self.initial_winnings = 2000

        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        # Setup the exerpiment status variables
        self.winnings = self.initial_winnings
        self.losses = 0
        self.last_win = 0
        self.last_loss = 0
        self.deck_pull_index = 0
        self.is_hunch = False
        self.is_sure = False

        self.progress_winnings.setMaximum(self.max_winnings)
        self.progress_losses.setMaximum(self.max_losses)

        # Define the deck behaviour
        deck1 = Deck.make_finite_deck(win_amounts=100,
                               loss_amounts=[0, 150, 200, 250, 300, 350],
                               loss_weights=[50, 10, 10, 10, 10, 10])
        deck2 = Deck.make_finite_deck(win_amounts=100,
                               loss_amounts=[0, 1250],
                               loss_weights=[90, 10])
        deck3 = Deck.make_finite_deck(win_amounts=50,
                               loss_amounts=[0, 25, 50, 75],
                               loss_weights=[40, 30, 20, 10])
        deck4 = Deck.make_finite_deck(win_amounts=50,
                               loss_amounts=[0, 250],
                               loss_weights=[90, 10])

        # Assign each deck to a button
        self.decks = {self.deck_button1: deck1,
                      self.deck_button2: deck2,
                      self.deck_button3: deck3,
                      self.deck_button4: deck4}

        # Send all the deck button presses to a single handler
        for button, deck in self.decks.items():
            button.clicked.connect(self.deck_button_pressed)

            # Don't let the buttons get focus so they can't be pressed with the space bar. This allows
            # us to press then on keyPress events rather than release events.
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.hunch_button.clicked.connect(self.update_hunch)
        self.hunch_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Key presses that map to buttons
        self.keymap = {
            **{key: self.deck_button1 for key in [Qt.Key_1, Qt.Key_A, Qt.Key_Left]},
            **{key: self.deck_button2 for key in [Qt.Key_2, Qt.Key_S, Qt.Key_Down]},
            **{key: self.deck_button3 for key in [Qt.Key_3, Qt.Key_D, Qt.Key_Right]},
            **{key: self.deck_button4 for key in [Qt.Key_4, Qt.Key_W, Qt.Key_Up]},
            **{key: self.hunch_button for key in [Qt.Key_Space, Qt.Key_Shift]},
        }

        # Update the status
        self.update_status()

        # Setup the data recording
        self.data = IowaData()

        # Launch the spike recorder if needed
        if self.spike_record:
            self.record_client = SpikeRecorder()
            self.record_client.launch()
            self.record_client.connect()

        # Move the window over a bit to make room for the SpikeRecorder app
        self.move(10, 10)

    def deck_button_pressed(self):
        """
        The user has drawn from a deck. Lets see what they win. This is the main event of the application.

        Returns:
            None
        """

        # Get the button that was clicked
        button = self.sender()

        # Get the deck for this button
        deck = self.decks[button]

        deck_index = list(self.decks.values()).index(deck)

        # Pull a card from this deck
        (win_amount, loss_amount) = deck.pull()

        self.winnings = self.winnings + win_amount
        self.losses = self.losses + loss_amount
        self.last_win = win_amount
        self.last_loss = loss_amount

        # Update the status display
        self.update_status()

        # Add the data and rewrite the experimental data to the file.
        self.data.add_trial(deck=deck_index, win_amount=win_amount, loss_amount=loss_amount,
                            hunch=self.is_hunch, sure=self.is_sure)

        if self.spike_record:
            self.record_client.push_event_marker(f"Deck Pull #{self.get_num_pulls()}: Deck #{deck_index}")

        # Dump the data back out to file. We will just dump everything back out over and over again
        # so that if the user stops half way through, they have part of their data.
        if self.output_filename is not None:
            self.data.to_csv(self.output_filename)
        else:
            logger.warning("Output filename is not definied, results are not being saved.")

        if self.DELAY_SECS and self.DELAY_SECS > 0:
            win_diag = WinDialog(parent=self, win_amount=win_amount, loss_amount=loss_amount,
                                 deck_index=deck_index,
                                 delay_seconds=self.DELAY_SECS)
            win_diag.exec_()

        if self.get_num_pulls() >= self.total_deck_pulls:

            if self.spike_record:
                self.record_client.stop_record()

            msg = QtWidgets.QMessageBox(parent=self)
            msg.setText("Experiment Complete!")
            msg.setWindowTitle("Done")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

            self.close()

    def update_hunch(self):
        """
        Allow the user to record when they get a hunch by pressing a button.

        Returns:
            None
        """
        if not self.is_hunch:
            self.is_hunch = True
            self.hunch_button.setText("I am pretty sure!")

            # Set event to spike recorder to mark in the recording when a hunch was recorded
            if self.spike_record:
                self.record_client.push_event_marker("Hunch!")
        else:
            if not self.is_sure:
                self.is_sure = True
                self.hunch_button.setEnabled(False)

                # Set and event in the spike recorder to mark in the recording when the user is sure.
                if self.spike_record:
                    self.record_client.push_event_marker("Sure!")

    def get_num_pulls(self):
        """
        Check how many pulls we have made on the decks.

        Returns:
            The number of pulls
        """
        return sum([deck.num_pulls for button, deck in self.decks.items()])

    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        self.label_last_win.setText(f'Winnings on last trial: <font color="#0571b0">${self.last_win}</font>')
        self.label_last_loss.setText(f'Losses on last trial: <font color="#ca0020">${self.last_loss}</font>')
        net = self.last_win - self.last_loss
        color = "#0571b0" if net >= 0 else "#ca0020"
        self.label_net_win.setText(f'Net Winnings: <font color="{color}">${net}</font>')
        self.label_pull_count.setText(f"Pull {self.get_num_pulls()}/{self.total_deck_pulls}")

        # Update the progress bars
        self.progress_winnings.setValue(self.winnings)
        self.progress_winnings.setFormat(f"${self.winnings}")
        self.progress_losses.setValue(self.losses)
        self.progress_losses.setFormat(f"${self.losses}")

    def closeEvent(self, event):
        if self.spike_record:
            self.record_client.shutdown()

        sys.exit(0)

    def keyPressEvent(self, event):
        """
        Decks can be controlled by pressing the [1,2,3,4], [a,s,d,w], or
        [left,down,right,up] arrow keys. The hunch button can pressed with
        the space or shift key.

        Args:
            event: The keyboard press event.

        Returns:
            None
        """

        if event.key() in self.keymap:
            button = self.keymap[event.key()]
            button.animateClick()

        event.accept()


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--spike-record', action='store_true',
                        default=False,
                        help='Launch Backyard Brains Spike Recorder in background. Default is do not run.')
    parser.add_argument('--total-deck-pulls', type=int, default=100,
                        help='The total number of deck pulls in the experiment. Default is 100.')

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    ui = IowaMainWindow(**vars(args))
    intro_d = IntroDialog(parent=ui)
    run_app(app, ui, intro_d)


if __name__ == "__main__":
    main()

