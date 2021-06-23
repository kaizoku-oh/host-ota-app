import argparse
import serial
from functools import partial

OTA_FRAME_ACK_BYTE          = 0x01
OTA_FRAME_ERR_BYTE          = 0x02
OTA_FRAME_START_BYTE        = 0x03
OTA_FRAME_END_BYTE          = 0x04
OTA_FRAME_BEGIN_OTA_BYTE    = 0x05
OTA_FRAME_FINISHED_OTA_BYTE = 0x06

binary_file = ""
chunk_size  = 0
baud        = 0
port        = ""
serialPort  = {}

def setup_serial():
  global serialPort

  serialPort = serial.Serial(port = port, baudrate = baud)
  serialPort.write(b'hello')
  serialPort.close()

def main():
  global binary_file
  global chunk_size 
  global baud
  global port
  global serialPort

  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()

  ap.add_argument("-c", "--chunk", type=int, default=64, help="Chunk size")
  ap.add_argument("-b", "--baud", type=int, default=115200, help="Serial baudrate")
  ap.add_argument("-p", "--port", type=str, default="COM3", help="Serial COM port")
  ap.add_argument("-f", "--file", type=str, default="firmware.bin", help="Binary file path")

  args, unknown = ap.parse_known_args()
  args = vars(args)

  binary_file = args['file']
  chunk_size = args['chunk']
  baud = args['baud']
  port = args['port']

  print("file name: {}".format(binary_file))
  print("chunk size: {}".format(chunk_size))
  print("baudrate: {}".format(baud))
  print("port: {}".format(port))

  with open(binary_file, 'rb') as file:
    for chunk in iter(partial(file.read, chunk_size), b''):
      # Send chunk
      serialPort.write(chunk)
      # Wait for 1 byte
      c = serialPort.read(1)
      if c == OTA_FRAME_ACK_BYTE:
        pass
      elif c == OTA_FRAME_ERR_BYTE:
        pass
      else:
        pass

if __name__ == "__main__":
  main()
