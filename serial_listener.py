# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
# list ports python -m serial.tools.list_ports
from authenticate import authenticateHash
import serial

def listen():
    HASH_BYTES = 2
    ser = serial.Serial()
    ser.baudrate = 9600 # Set boudrate
    ser.port = 'COM3' # Set port
    ser.timeout = 0 # Set timeout 0s

    ser.open() # Open serial port
    print('Wating for RFID hash...')
    if ser.is_open == True:
        while True:
            # Wait until a tag is read
            hash = ser.read(HASH_BYTES)
            #print(hash)
            if len(hash) == HASH_BYTES:
                print(hash)
                # TODO: Do something with hash
                authenticateHash(hash)
                # Flush the bus
                ser.flushInput()
    ser.close() # Close serial port

def sendFakeHash(hash):
    return authenticateHash(hash)