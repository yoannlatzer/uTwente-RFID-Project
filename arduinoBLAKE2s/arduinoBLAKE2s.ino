/*
 * Arduino RFID reader - Yoann Latzer 2016 
 * Code based on "Dump Info" example from https://github.com/miguelbalboa/rfid
 * UID print code from stack overflow https://goo.gl/sD9org
 * SHA3 class is from Arduino Cryptographic Library: https://rweather.github.io/arduinolibs/index.html
*/

#include <SPI.h>
#include <MFRC522.h>
#include <Crypto.h>
#include <BLAKE2s.h>

#define HASH_LEN 16

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance.

/**
 * mfrc522.PICC_IsNewCardPresent() should be checked before 
 * @return the card UID
 */
unsigned long getID(){
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
    return -1;
  }
  unsigned long hex_num;
  hex_num =  mfrc522.uid.uidByte[3] << 24;
  hex_num += mfrc522.uid.uidByte[2] << 16;
  hex_num += mfrc522.uid.uidByte[1] << 8;
  hex_num += mfrc522.uid.uidByte[0];
  mfrc522.PICC_HaltA(); // Stop reading
  return hex_num; 
  
}

BLAKE2s bKey;
char key[] = "testkey";
uint8_t hashOfJSON[HASH_LEN];

void setup() {
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card
  Serial.println("Scan PICC to see UID and type...");
}

void loop() {
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  } else {
    unsigned long uid = getID();
    if(uid != -1){
      Serial.print("Card detected, UID: "); Serial.println(uid);
    }
    unsigned long hash;
    bKey.resetHMAC(key, sizeof(key));
    bKey.update(uid, sizeof(uid));
    bKey.finalizeHMAC(key, sizeof(key), hashOfJSON, HASH_LEN);
    String hashStr;
    for(int i=0;i<HASH_LEN; i++){
    hashStr += String(+hashOfJSON[i], HEX);
    }
    Serial.println(hashStr);
    Serial.println("");
  }
 
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
}
