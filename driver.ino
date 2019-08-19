#include <MFRC522.h>                            // Library for Mifare RC522 Devices (thingy that reads the card)
#include <SPI.h>                                // RC522 Module uses SPI protocol

const byte motor_pin_1 = 5;
const byte motor_pin_2 = 6;
int open_duration = 4000;
int close_duration = 300;

const byte red_LED_pin = 3;
const byte green_LED_pin = 2;

//Reader
const byte SS_pin = 10;
const byte RST_pin = 9;
MFRC522 rfid(SS_pin, RST_pin);                // Create MFRC522 (rfid reader) instance
byte readCard[4];

//void open();

void setup(){
	pinMode(motor_pin_1, OUTPUT);
	pinMode(motor_pin_2, OUTPUT);
	pinMode(red_LED_pin, OUTPUT);
	pinMode(green_LED_pin, OUTPUT);

	// init serial
	Serial.begin(9600);

	// init reader stuff 
	SPI.begin();                                     // MFRC522 Hardware uses SPI protocol
	rfid.PCD_Init();                              // Initialize MFRC522 Hardware
	rfid.PCD_SetAntennaGain(rfid.RxGain_max);  // MORE POWER
}


void loop(){
    if ( Serial.available() ) {
    	if ( Serial.read() == 'o' ){
        	greenLedFlash();
        	open();
      	}else{
        	redLedFlash();
      	}
    }
    getID();
    delay(50);
}

void getID() {
  	// Getting ready for Reading PICCs
	if ( ! rfid.PICC_IsNewCardPresent()) { //If a new PICC placed to RFID reader continue
    	return;
  	}
  	if ( ! rfid.PICC_ReadCardSerial()) {   //Since a PICC placed get Serial and continue
    	return;
  	}
  	
  	for (int i = 0; i < 4; i++) {  //op
    	readCard[i] = rfid.uid.uidByte[i];
    	Serial.print(readCard[i], HEX);
  	}
  	Serial.println("");
  	rfid.PICC_HaltA(); // Stop reading
}



void open(){
    //unlock
    analogWrite(motor_pin_1, 255);
    analogWrite(motor_pin_2, 0);
    delay(open_duration);

    //lock
    analogWrite(motor_pin_1, 0);
    analogWrite(motor_pin_2, 255);
    delay(close_duration);

    //stop motor
    analogWrite(motor_pin_2, 0);
}

// will flash and turn off
void greenLedFlash(){
	digitalWrite(green_LED_pin, HIGH);
    delay(50);
    digitalWrite(green_LED_pin, LOW);
    delay(50);
    digitalWrite(green_LED_pin, HIGH);
    delay(50);
    digitalWrite(green_LED_pin, LOW);
}

// will flash and turn off
void redLedFlash(){
    digitalWrite(red_LED_pin, HIGH);
    delay(50);
    digitalWrite(red_LED_pin, LOW);
    delay(50);
    digitalWrite(red_LED_pin, HIGH);
    delay(50);
    digitalWrite(red_LED_pin, LOW);
}
