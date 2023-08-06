import zmq
import attr
import cattr
import json
import multiprocessing

from typing import Dict
from enum import unique, Enum

import logging
logger = logging.getLogger(__name__)

import spike_recorder.server
import os


class SpikeRecorderUnavailable(Exception):
    """This exception is raised whenever we cannot reach the SpikeRecorder"""
    pass


@unique
class CommandType(Enum):
    """
    The type of command we want to execute on the server side.

        START_RECORD: Start a recording, this is equivalent to pressing the record button in GUI
        STOP_RECORDING: Stop a recording, this is equivalent to pressing the record button in GUI
        PUSH_EVENT_MARKER: Push an event to the recording.
        SHUTDOWN: Shutdown the server.
        REPLY_OK: Server sends this back if command is accepted.
        REPLY_ERROR: Server sends this back if command failed.

    """
    START_RECORD = "START_RECORD"
    STOP_RECORD = "STOP_RECORD"
    PUSH_EVENT_MARKER = "PUSH_EVENT_MARKER"
    SHUTDOWN = "SHUTDOWN"
    REPLY_OK = "REPLY_OK"
    REPLY_ERROR = "REPLY_ERROR"


@attr.s(auto_attribs=True)
class CommandMsg:
    """
    A structure to represent command passed to the SpikeRecorder application server side. These
    are serialized to JSON and sent over ZeroMQ.
    """
    type: CommandType
    args: Dict = attr.ib(default=attr.Factory(dict))

    def to_json(self) -> str:
        """
        Serialize this CommandMsg to JSON

        Returns:
            A string containing the JSON for this message.
        """
        return json.dumps(cattr.unstructure(self))

    @classmethod
    def from_json(cls, json_str) -> 'CommandMsg':
        """
        Convert a JSON string to CommandMsg

        Args:
            json_str: The JSON string to parse

        Returns:
            A CommandMsg instance for this JSON string.
        """
        return cattr.structure(json.loads(json_str), cls)


class SpikeRecorder:
    """
    The main API for launching and controlling the Backyard Brains SpikeRecorder GUI
    applications.
    """

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None

    @staticmethod
    def launch() -> multiprocessing.Process:
        """
        Launch the BackyardBrains SpikeRecorder app. This launches the application
        asynchronously.

        Note: the only way to safely shutdown the process from Python is to subsequently
            connect and shutdown
            >>> spike_client = SpikeRecorder()
            >>> spike_client.launch()
            >>> spike_client.connect()
            >>> spike_client.shutdown()

        Returns:
            The multiprocessing.Process running that the application is running inside.
        """
        return spike_recorder.server.launch(is_async=True)

    def connect(self):
        """
        Connect to an already running BackyardBrains SpikeRecorder GUI application.

        Returns:
            None
        """

        # Launch the SpikeRecorder process

        # Connect to the command server, wait until
        logger.info("Connecting to SpikeRecorder server ...")
        self.socket = self.context.socket(zmq.REQ)

        # Set the receive timeout to 500 milliseconds
        self.socket.setsockopt(zmq.RCVTIMEO, 500)

        self.socket.connect("tcp://localhost:5555")

    def shutdown(self, block: bool = False):
        """
        Close the SpikeRecorder GUI application completely.

        Args:
            block: Whether to block and wait for a reply from the server. True means wait, False means don't

        Returns:
            None
        """
        self._check_server()

        logger.info("Shutting down SpikeRecorder ...")

        # Send the shutdown command
        self._send(CommandMsg(type=CommandType.SHUTDOWN), block=block)

    def start_record(self, filename: str = None, block: bool = True):
        """
        Begin a recording session.

        Args:
            filename: Either a filename or directory. If a filename it must end .wav. If a directory,
                then the SpikeRecorder app will generate a unique filename in that directory and it will be
                 displayed in the app at the end of recording. If None, the default Spike Recording recording
                 path and filenames will be used.
            block: Whether to block and wait for a reply from the server. True means wait, False means don't

        Returns:
            None
        """

        if filename == "":
            filename = None

        # If we are dealing with a relative path, make it absolute.
        if filename is not None:
            filename = os.path.abspath(filename)

        self._check_server()
        if filename is None:
            self._send(CommandMsg(type=CommandType.START_RECORD), block=block)
        else:
            self._send(CommandMsg(type=CommandType.START_RECORD, args={'filename': filename}), block=block)

        logger.info("Recording Started")

    def stop_record(self, block: bool = True):
        """
        Stop a recording session. This results in the saving of two files, a WAV file with the
        recorded spike data and a txt file annotating event markers that were generated while
        recording. See Backyard Brains documention for more information:

        https://backyardbrains.com/products/files/SpikeRecorderDocumentation.2018.02.pdf

        Args:
            block: Whether to block and wait for a reply from the server. True means wait, False means don't

        Returns:
            None
        """
        self._check_server()
        self._send(CommandMsg(type=CommandType.STOP_RECORD), block=block)
        logger.info("Recording Stopped")

    def push_event_marker(self, marker: str, block: bool = True):
        """
        Immediately push an event marker into the recordring. The SpikeRecorder GUI application
        only supports adding markers name 0-9 by pressing the numeric keys on the keyboard. This
        function allows adding markes with arbitrary string literals.

        Args:
            marker: An arbitrary string label to identify this marker.
            block: Whether to block and wait for a reply from the server. True means wait, False means don't

        Returns:
            None
        """

        self._check_server()
        self._send(CommandMsg(type=CommandType.PUSH_EVENT_MARKER, args={'name': marker}), block=block)

    def _check_server(self):
        """
        Check if the socket has been setup with a connection to the server.

        Returns:

        """
        if not self.socket:
            raise ValueError("SpikeRecorder server connection not setup!")

    def _send(self, command: CommandMsg, block: bool = True) -> CommandMsg:
        """
        Send a command message to SpikeRecorder GUI application server. This is just a string message
        send to a ZeroMQ socket.

        Args:
            command: A command message to send to the server
            no_block: Fire the message and don't wait for a response

        Returns:
            The CommandMsg we received back as a reply
        """

        try:

            logger.info(f"Sending: {command}")
            self.socket.send(command.to_json().encode())

            if block:

                # Get the reply.
                reply_str = self.socket.recv()

                # Remove the null terminator
                reply_str = reply_str[0:len(reply_str)-1]

                reply = CommandMsg.from_json(reply_str)
                logger.info(f"Received: {reply}")

                if reply.type == CommandType.REPLY_ERROR:
                    raise Exception(f"Spike-Recorder Application Command Error: \n{reply}")

        except (zmq.error.Again, zmq.error.ZMQError) as ex:
            logger.error("Warning: Failed to communicate with Spike-Recorder application. No spike recording is occurring.")
            raise SpikeRecorderUnavailable() from ex
