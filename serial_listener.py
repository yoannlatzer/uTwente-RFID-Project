# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
# list ports python -m serial.tools.list_ports
from authenticate import authenticateHash
import serial
#import init as scan
import requests

def listen(ctx):
    try:
        uidString = ""
        ser = serial.Serial()
        ser.baudrate = 9600  # Set boudrate
        ser.port = '/dev/cu.usbmodem1421'  # Set port
        ser.timeout = 0  # Set timeout 0s
        ser.open() # Open serial port
        print('Wating for RFID hash...')
        if ser.is_open == True:
            while True:
                # Wait until a tag is read
                hash = ser.read()
                if hash == b'\r':
                    print(uidString)
                    r = requests.post('http://localhost:8080/fake/id', data={'id': uidString})
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