from enum import Enum
from CoDrone.crc import CRC16
from time import process_time

from CoDrone.protocol import Header
from CoDrone.protocol import DataType


class StateLoading(Enum):
    Ready = 0x00
    Receiving = 0x01
    Loaded = 0x02
    Failure = 0x03


class Section(Enum):
    Start = 0x00
    Header = 0x01
    Data = 0x02
    End = 0x03


class Receiver:
    def __init__(self):

        self.state = StateLoading.Ready
        self.sectionOld = Section.End
        self.section = Section.Start
        self.index = 0

        self.header = Header()
        self.timeReceiveStart = 0
        self.timeReceiveComplete = 0

        self._buffer = bytearray()
        self.data = bytearray()

        self.crc16received = 0
        self.crc16calculated = 0

        self.message = None

    def call(self, data):

        now = process_time()*1000

        self.message = None

        # First Step
        if self.state == StateLoading.Failure:
            self.state = StateLoading.Ready

        # Second Step
        if self.state == StateLoading.Ready:
            self.section = Section.Start
            self.index = 0

        elif self.state == StateLoading.Receiving:
            if (self.timeReceiveStart + 600) < now:
                self.state = StateLoading.Failure
                self.message = "Error / Receiver / StateLoading.Receiving / Time over."
                return self.state

        elif self.state == StateLoading.Loaded:
            return self.state

        # Third Step
        if self.section != self.sectionOld:
            self.index = 0
            self.sectionOld = self.section

        # Fourth Step
        if self.section == Section.Start:
            if self.index == 0:
                if data == 0x0A:
                    self.state = StateLoading.Receiving

                else:
                    self.state = StateLoading.Failure
                    return self.state
                self.timeReceiveStart = now

            elif self.index == 1:
                if data != 0x55:
                    self.state = StateLoading.Failure
                    return self.state

                else:
                    self.section = Section.Header
            else:
                self.state = StateLoading.Failure
                self.message = "Error / Receiver / Section.Start / Index over."
                return self.state

        elif self.section == Section.Header:

            if self.index == 0:
                self.header = Header()

                try:
                    self.header.dataType = DataType(data)

                except:
                    self.state = StateLoading.Failure
                    self.message = "Error / Receiver / Section.Header / DataType Error. 0x{0:02X}".format(data)
                    return self.state

                self.crc16calculated = CRC16.calc(data, 0)

            elif self.index == 1:
                self.header.length = data
                self.crc16calculated = CRC16.calc(data, self.crc16calculated)

                if self.header.length > 128:
                    self.state = StateLoading.Failure
                    self.message = "Error / Receiver / Section.Header / Data length is longer than 128. [{0}]".format(
                        self.header.length)
                    return self.state

                elif self.header.length == 0:
                    self.section = Section.End

                else:
                    self.section = Section.Data
                    self._buffer.clear()

            else:
                self.state = StateLoading.Failure
                self.message = "Error / Receiver / Section.Header / Index over."
                return self.state

        elif self.section == Section.Data:
            self._buffer.append(data)
            self.crc16calculated = CRC16.calc(data, self.crc16calculated)

            if self.index == (self.header.length - 1):
                self.section = Section.End

        elif self.section == Section.End:
            if self.index == 0:
                self.crc16received = data

            elif self.index == 1:
                self.crc16received = (data << 8) | self.crc16received

                if self.crc16received == self.crc16calculated:
                    self.data = self._buffer.copy()
                    self.timeReceiveComplete = now
                    self.state = StateLoading.Loaded
                    self.message = "Success / Receiver / Section.End / Receive complete / {0} / [receive: 0x{1:04X}]".format(
                        self.header.dataType, self.crc16received)
                    return self.state

                else:
                    self.state = StateLoading.Failure
                    self.message = "Error / Receiver / Section.End / CRC Error / {0} / [receive: 0x{1:04X}, calculate: 0x{2:04X}]".format(
                        self.header.dataType, self.crc16received, self.crc16calculated)
                    return self.state

            else:
                self.state = StateLoading.Failure
                self.message = "Error / Receiver / Section.End / Index over."
                return self.state

        else:
            self.state = StateLoading.Failure
            self.message = "Error / Receiver / Section over."
            return self.state

        # Fifth Step
        if self.state == StateLoading.Receiving:
            self.index += 1

        return self.state

    def checked(self):
        self.state = StateLoading.Ready
