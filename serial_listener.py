# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
# list ports python -m serial.tools.list_ports
from authenticate import authenticateHash
import serial
import init as scan

uidString = ""
ser = serial.Serial()
ser.baudrate = 9600 # Set boudrate
ser.port = 'COM3' # Set port
ser.timeout = 0 # Set timeout 0s

def pause(ctx):
    ser.close()

def listen(ctx):
    try:
        ser.open() # Open serial port
        print('Wating for RFID hash...')
        if ser.is_open == True:
            while True:
                # Wait until a tag is read
                hash = ser.read()
                if hash == b'\r':
                    print(uidString)
                    scan.realscan(ctx, uidString)
                    # Flush the bus
                    ser.flushInput()
                    uidString = ""
                    return
                if len(hash) != 0 :
                    uidString += hash.decode("utf-8")
        ser.close() # Close serial port
    except serial.SerialException:
        pass

def sendFakeHash(hash):
    return authenticateHash(hash)