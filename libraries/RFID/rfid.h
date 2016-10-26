/*
  RFID.h - Library for reading the UID of an RFID tag.
*/

#ifndef RFID_h
#define RFID_h

#include <Arduino.h>
#include <..\MFRC522\MFRC522.h>
#include <SPI.h>

class RFID
{
  public:
    RFID();
	void begin();
    uint32_t readUID();
};

#endif