import sys
import os
import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtGui, QtWidgets


def run_app(app, ui, intro_d):
    ui.showNormal()

    # Show the instructions and ask for an output file name. Do some error
    # checking if the file isn't valid.
    fileNoGood = True
    while fileNoGood:
        # Try to open the output file for writing
        try:
            intro_d.show()
            intro_d.textbox_file.setFocus()
            intro_d.exec_()

            # Grab the filename from the textbox
            filename = intro_d.textbox_file.text()

            # Check if the file exists already, make sure they want to overwrite?
            if os.path.isfile(filename):
                qm = QtWidgets.QMessageBox
                retval = qm.question(intro_d, "", "This file already exists. "
                                                  "Are you sure you want it to be overwritten?",
                                     qm.Yes | qm.No, parent=ui)

                if retval == qm.No:
                    continue

            # Check if we can open the file. If so, set the output file on the main app
            # and we are ready to go!
            with open(filename, 'w') as f:
                fileNoGood = False
                ui.output_filename = intro_d.textbox_file.text()

        except Exception as ex:
            msg = QtWidgets.QMessageBox(parent=ui)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Output file could not be opened. Check the path.")
            msg.setDetailedText(f"{ex}")
            msg.setWindowTitle("Output File Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

    # Start a spike recorder recording for this session
    if ui.spike_record:
        # Generate the recording filename from the output filename
        record_filename = os.path.splitext(filename)[0] + ".wav"
        ui.record_client.start_record(record_filename)
        logger.info(f"Generating recording: {record_filename}")

    # Run the main app
    ret = app.exec_()

    if ui.spike_record:
        ui.record_client.shutdown()

    sys.exit(ret)