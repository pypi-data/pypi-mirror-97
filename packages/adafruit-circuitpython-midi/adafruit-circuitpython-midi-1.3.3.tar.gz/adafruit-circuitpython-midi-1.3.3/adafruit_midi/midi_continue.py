# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.continue`
================================================================================

Continue MIDI message.


* Author(s): Mark Komus

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class Continue(MIDIMessage):
    """Continue MIDI message."""

    _STATUS = 0xFB
    _STATUSMASK = 0xFF
    LENGTH = 1


Continue.register_message_type()
