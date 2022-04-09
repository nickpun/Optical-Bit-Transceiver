// INPUT MESSAGE
const char bits[120] = {1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
                         0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0};

// Constants
const int ledPin =  LED_BUILTIN; // the number of the LED pin

// User variables
const float freq = 40;     // [hertz]
const int pulseWidth = 500;   // [microseconds]
const int numBitBins = 15;
const int tTime = 30;         // [seconds]

// System variables
unsigned long period = round(1000/freq);

// Initialization
void setup() {
  // set the digital pin as output:
  pinMode(ledPin, OUTPUT);
}

// Blink at multiple frequencies
void loop() {
  for (int i=1; i<numBitBins; i++) {
    if (bits[i] == 1) {
      unsigned long currTime = millis();
      unsigned long prevMillis = 0;
      while (currTime <= i*tTime/numBitBins*1000) {
        unsigned long currMillis = millis();
        if (currMillis - prevMillis >= period) {
        digitalWrite(ledPin, HIGH);
        delayMicroseconds(pulseWidth);
        digitalWrite(ledPin, LOW);
        prevMillis = currMillis;
        }
        currTime = millis();
      }
    }
  }
}
