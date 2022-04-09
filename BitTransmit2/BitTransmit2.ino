// INPUT MESSAGE
const char bits[120] = {1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
                         0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0};

// Constants
const int ledPin =  LED_BUILTIN; // the number of the LED pin

// User variables
const float freq = 500;     // [hertz]
const int pulseWidth = 500;   // [microseconds]
const int numBitBins = 15;
const int bitsPerBin = 8;
const int tTime = 30;         // [seconds]
const int separation = 5;

// System variables
int freqs[(int) pow(2,bitsPerBin)] = {};
int prevMillis = 0;

// Initialization
void setup() {
  // set the digital pin as output:
  pinMode(ledPin, OUTPUT);
  for (int i=0; i<pow(2,bitsPerBin); i++) {
    freqs[i] = freq + i*separation;
  }
}

// Blink at frequency
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
  unsigned long currMillis = millis();
  unsigned long f = 0;
  for (int j = 0; j<bitsPerBin; j++) {
    if (bits[i*bitsPerBin+j] == 1) {
      f += 2^(i*bitsPerBin+j);
    }
  }
  unsigned long period = round(1000/freqs[f]);
  if (currMillis - prevMillis >= period) {
    digitalWrite(ledPin, HIGH);
    delayMicroseconds(pulseWidth);
    digitalWrite(ledPin, LOW);
    prevMillis = currMillis;
  }
}
