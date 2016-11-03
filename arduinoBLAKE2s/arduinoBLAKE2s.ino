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
// Define Hash length
#define HASH_LEN 32

#define SS_PIN 10
#define RST_PIN 9
// Create MFRC522 instance.
MFRC522 mfrc522(SS_PIN, RST_PIN);

/*
 * Create a BLAKE2s object, a char to store the key 
 * and a 8bit unsigned integer to store the hash  
 */
BLAKE2s B2s;
char key[] = "Les sanglots longs des violons de l'automne, blessent mon coeur d'une langueur monotone";
uint8_t hashOfJSON[HASH_LEN];

void setup() {
  pinMode(6, OUTPUT);
  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card
  // Serial.println("Scan PICC to see UID and type...");
  
}

unsigned long getID(){
  /*
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
    return -1;
  }
  */
  unsigned long hex_num;
  unsigned long hex_temp;
  hex_temp =  mfrc522.uid.uidByte[3];
  hex_num = hex_temp << 24;
  hex_temp = mfrc522.uid.uidByte[2];
  hex_num += hex_temp << 16;
  hex_temp = mfrc522.uid.uidByte[1];
  hex_num += hex_temp << 8;
  hex_num += mfrc522.uid.uidByte[0];
  mfrc522.PICC_HaltA(); // Stop reading
  return hex_num; 
  
}

void loop() {
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
 
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Hash the UID if getID() gave results
  unsigned long uid = getID();
    if(uid != -1){
      // Print the uid on serial port
      // Serial.print("Card detected, UID: "); Serial.println(uid);
      // BLAKE2s: reset the key, update the uid and finalize the hash
      B2s.resetHMAC(key, sizeof(key));
      B2s.update(uid, sizeof(uid));
      B2s.finalizeHMAC(key, sizeof(key), hashOfJSON, HASH_LEN);
      // put the hash stored in "hashOfJSON" in a string
      String hashStr;
      for(int i=0;i<HASH_LEN; i++){
      hashStr += String(+hashOfJSON[i], HEX);
      }
      // Print the hash string on serial port
      Serial.println(hashStr);
      // Turn the buzzer on and off when hash is transmitted
      //tone(6, 523);
      //delay(200);
      //tone(6, 698);
      //delay(200);
      //noTone(6);
    }
  
}
