import logging
import datetime
import sys

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.DataStepper import DataStepper

_LOGGER = logging.getLogger(__name__)

class LogFormatter:
	def __init__(self):
		self.timestampFormat = "%Y-%m-%d %H:%M:%S.%f"

		# Whether to enable colors in logs.
		self.enableColors = True
		if sys.platform == "win32":
			self.enableColors = False

		# Whether the next log line should get a prefix.
		self._printPrefix = True

	def getPrefix(self, timestamp, fileName, lineNr, logLevel):
		return f"LOG: [{timestamp.strftime(self.timestampFormat)}] [{fileName[-30:]}:{lineNr:4n}] {self.getLogLevelStr(logLevel)}{self.getLogLevelColor(logLevel)} "

	def getLogLevelStr(self, logLevel):
		if logLevel == 8: return "V"
		if logLevel == 7: return "D"
		if logLevel == 6: return "I"
		if logLevel == 5: return "W"
		if logLevel == 4: return "E"
		if logLevel == 3: return "F"
		return " "

	def getLogLevelColor(self, logLevel):
		if self.enableColors:
			if logLevel == 8: return "\033[37;1m" # White
			if logLevel == 7: return "\033[37;1m" # White
			if logLevel == 6: return "\033[34;1m" # Blue
			if logLevel == 5: return "\033[33;1m" # Yellow
			if logLevel == 4: return "\033[35;1m" # Purple
			if logLevel == 3: return "\033[31;1m" # Red
		return ""

	def getEndColor(self):
		if self.enableColors:
			return "\033[0m"
		return ""

	def printLog(self,
	           logFormat: str,
	           fileName: str,
	           lineNr: int,
	           logLevel: int, # TODO: make enum
	           newLine: bool,
	           argBufs: list):
		timestamp = datetime.datetime.now()

		_LOGGER.debug(f"Log {fileName}:{lineNr} {logFormat} {argBufs}")

		if logFormat is not None:
			formattedString = ""
			i = 0
			argNum = 0
			while i < len(logFormat):
				if logFormat[i] == '%':
					# Check the arg format.
					i += 1
				else:
					# Just append the character
					formattedString += logFormat[i]
					i += 1
					continue

				if logFormat[i] == '%':
					# Actually not an arg, but an escaped '%'
					formattedString += logFormat[i]
					i += 1
					continue

				# Check arg type and let python do the formatting.
				argVal = 0     # Value of this arg
				argFmt = "%"   # Format of this arg
				while True:
					c = logFormat[i]
					argBuf = None
					argLen = 0
					if argNum < len(argBufs):
						argBuf = argBufs[argNum]
						argLen = len(argBuf)

					if c == 'd' or c == 'i':
						# Signed integer
						argVal = 0
						if argLen == 1:
							argVal = Conversion.uint8_to_int8(argBuf[0])
						elif argLen == 2:
							argVal = Conversion.uint8_array_to_int16(argBuf)
						elif argLen == 4:
							argVal = Conversion.uint8_array_to_int32(argBuf)
						elif argLen == 8:
							argVal = Conversion.uint8_array_to_int64(argBuf)

						argFmt += c
						break

					elif c == 'u' or c == 'x' or c == 'X' or c == 'o' or c == 'p':
						# Unsigned integer
						argVal = 0
						if argLen == 1:
							argVal = argBuf[0]
						elif argLen == 2:
							argVal = Conversion.uint8_array_to_uint16(argBuf)
						elif argLen == 4:
							argVal = Conversion.uint8_array_to_uint32(argBuf)
						elif argLen == 8:
							argVal = Conversion.uint8_array_to_uint64(argBuf)

						if c == 'p':
							# Python doesn't do %p
							argFmt += 'x'
						else:
							argFmt += c
						break

					elif c == 'f' or c == 'F' or c == 'e' or c == 'E' or c == 'g' or c == 'G':
						# Floating point
						argVal = 0.0
						if argLen == 4:
							argVal = Conversion.uint8_array_to_float(argBuf)

						argFmt += c
						break

					elif c == 'a':
						# Character
						argVal = ' '
						if argLen == 1:
							argVal = argBuf[0]

						argFmt += c
						break

					elif c == 's':
						# String
						argVal = ""
						if argBuf is not None:
							argVal = Conversion.uint8_array_to_string(argBuf)

						argFmt += c
						break

					else:
						i += 1
						argFmt += c
						continue

				# Let python do the formatting
				argStr = argFmt % argVal
				formattedString += argStr
				argNum += 1
				i += 1

			logStr = formattedString
			if self._printPrefix:
				logStr = self.getPrefix(timestamp, fileName, lineNr, logLevel) + logStr

			sys.stdout.write(logStr)
			if newLine:
				# Next line should be prefixed.
				self._printPrefix = True
				sys.stdout.write(self.getEndColor())
				sys.stdout.write('\n')
			else:
				self._printPrefix = False

	def printLogArray(self,
	                logFormat: str,
	                fileName: str,
	                lineNr: int,
	                logLevel: int, # TODO: make enum
	                newLine: bool,
	                elementType: int, # TODO: make enum
	                elementSize: int,
	                elementData: list):
		timestamp = datetime.datetime.now()

		dataStepper = DataStepper(elementData)
		dataSize = len(elementData)
		if dataSize % elementSize != 0:
			_LOGGER.warning(f"Remaining data with element size of {elementSize} and element data of size {dataSize}")
			return

		logStr = "["
		numElements = int(dataSize / elementSize)
		_LOGGER.debug(f"dataSize={dataSize} elementSize={elementSize} numElements={numElements}")
		for i in range(0, numElements):
			if elementType == 0:
				# Signed integer
				elemVal = 0
				if elementSize == 1:
					elemVal = dataStepper.getInt8()
					logStr += "%3i, " % elemVal
				elif elementSize == 2:
					elemVal = dataStepper.getInt16()
					logStr += "%5i, " % elemVal
				elif elementSize == 4:
					elemVal = dataStepper.getInt32()
					logStr += "%10i, " % elemVal
				elif elementSize == 8:
					elemVal = dataStepper.getInt64()
					logStr += "%20i, " % elemVal

			elif elementType == 1:
				# Unsigned integer
				elemVal = 0
				if elementSize == 1:
					elemVal = dataStepper.getUInt8()
					logStr += "%3u, " % elemVal
				elif elementSize == 2:
					elemVal = dataStepper.getUInt16()
					logStr += "%5u, " % elemVal
				elif elementSize == 4:
					elemVal = dataStepper.getUInt32()
					logStr += "%10u, " % elemVal
				elif elementSize == 8:
					elemVal = dataStepper.getUInt64()
					logStr += "%20u, " % elemVal

			elif elementType == 2:
				# Floating point
				elemVal = 0.0
				if elementSize == 4:
					argVal = dataStepper.getFloat()
				logStr += "%f, " % elemVal

		# Remove last ", " and add closing bracket.
		logStr = logStr[0:-2] + "]"

		if self._printPrefix:
			logStr = self.getPrefix(timestamp, fileName, lineNr, logLevel) + logStr

		sys.stdout.write(logStr)
		if newLine:
			# Next line should be prefixed.
			self._printPrefix = True
			sys.stdout.write(self.getEndColor())
			sys.stdout.write('\n')
		else:
			self._printPrefix = False
