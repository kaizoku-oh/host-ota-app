import argparse
import serial
from functools import partial

binary_file = ""
chunk_size = 0
baud = 0
port = ""

def setup_serial():
  ser = serial.Serial(port)
  ser.write(b'hello')
  ser.close()
  pass

def send_serial(data):
  pass

def main():
  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()

  ap.add_argument("-c", "--chunk", type=int, default=64, help="Chunk size")
  ap.add_argument("-b", "--baud", type=int, default=115200, help="Serial baudrate")
  ap.add_argument("-p", "--port", type=str, default="COM3", help="Serial COM port")
  ap.add_argument("-f", "--file", type=str, default="firmware.bin", help="Binary file path")

  args, unknown = ap.parse_known_args()
  args = vars(args)

  global binary_file = args['file']
  global chunk_size = args['chunk']
  global baud = args['baud']
  global port = args['port']

  print("file name: {}".format(binary_file))
  print("chunk size: {}".format(chunk_size))
  print("baudrate: {}".format(baud))
  print("port: {}".format(port))

  with open(binary_file, 'rb') as file:
    for chunk in iter(partial(file.read, chunk_size), b''):
      send_serial(chunk)
      if receive_ack():
        pass
      elif receive_err():
        resend_serial()
      else:
        pass

if __name__ == "__main__":
  main()