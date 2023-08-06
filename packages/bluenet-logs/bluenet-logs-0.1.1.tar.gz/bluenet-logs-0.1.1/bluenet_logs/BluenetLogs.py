from crownstone_uart import UartEventBus, UartTopics
from crownstone_uart.core.uart.uartPackets.UartLogArrayPacket import UartLogArrayPacket
from crownstone_uart.core.uart.uartPackets.UartLogPacket import UartLogPacket

from bluenet_logs.LogFormatter import LogFormatter
from bluenet_logs.LogLineRetriever import LogLineRetriever


class BluenetLogs:
	__version__ = "0.1.1"

	def __init__(self):
		self.logFormatter = LogFormatter()
		self.logLineRetriever = LogLineRetriever()

		UartEventBus.subscribe(UartTopics.log, self.onLog)
		UartEventBus.subscribe(UartTopics.logArray, self.onLogArray)

	def setSourceFilesDir(self, dir: str):
		self.logLineRetriever.setSourceFilesDir(dir)

	def onLog(self, data: UartLogPacket):
		fileName = self.logLineRetriever.getFileName(data.header.fileNameHash)
		if fileName is None:
			return
		logFormat = self.logLineRetriever.getLogFormat(fileName, data.header.lineNr)
		if logFormat is None:
			return
		self.logFormatter.printLog(logFormat, fileName, data.header.lineNr, data.header.logLevel, data.header.newLine, data.argBufs)

	def onLogArray(self, data: UartLogArrayPacket):
		fileName = self.logLineRetriever.getFileName(data.header.fileNameHash)
		if fileName is None:
			return
		# No log format is used yet.
		logFormat = ""
		self.logFormatter.printLogArray(logFormat, fileName, data.header.lineNr, data.header.logLevel, data.header.newLine, data.elementType, data.elementSize, data.elementData)
