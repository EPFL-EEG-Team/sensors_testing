//For recording eeg data
//To be used with record_eeg.py
unsigned long now, prev;


void setup() {
  Serial.begin(115200);
  prev = micros();
}

void loop() {
  // put your main code here, to run repeatedly:
  now = micros();
  if(now - prev >= 2000){
    prev = now;
    Serial.print(now);
    Serial.print(',');
    Serial.print(analogRead(0));
    Serial.print('\n');
  }
}
