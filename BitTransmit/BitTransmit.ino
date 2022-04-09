// INPUT MESSAGE
const char bits[120] = {1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
                         0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0};

// Constants
const int ledPin =  LED_BUILTIN; // the number of the LED pin

// User variables
const float lowFreq = 60;     // [hertz]
const int pulseWidth = 500;   // [microseconds]
const int numBitBins = 15;
const int bitsPerBin = 8;
const int tTime = 30;         // [seconds]

// System variables
float freqs[bitsPerBin] = {};

// Initialization
void setup() {
  // set the digital pin as output:
  pinMode(ledPin, OUTPUT);
  for (int i=0; i<bitsPerBin; i++) {
    freqs[i] = lowFreq*(1 + (i+0.5)/bitsPerBin);
  }
}

// Blink at multiple frequencies
void loop() {
  for (int i=1; i<=numBitBins; i++) {
    unsigned long currTime = millis();
    while (currTime <= i*tTime/numBitBins*1000) {
      BlinkHelper(i);
      currTime = millis();
    }
  }
}

void BlinkHelper(int i) {
  bool onB4 = false;
  unsigned long currMillis = millis();
  for (int j = 0; j<bitsPerBin; j++) {
    if (onB4 == false) {
      unsigned long period = round(1000/freqs[j]);
      if ((currMillis % period == 0) && (bits[i*bitsPerBin+j] == 1)) {
        digitalWrite(ledPin, HIGH);
        delayMicroseconds(pulseWidth);
        digitalWrite(ledPin, LOW);
        onB4 = true;
      }
    }
  }
}
