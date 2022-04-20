//For recording eeg data
//To be used with record_eeg.py
unsigned long start, t;


void setup() {
  Serial.begin(9600);
  start = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  t = millis() - start;
  if(t%10==0){
    Serial.print(t);
    Serial.print(',');
    Serial.print(analogRead(0));
    Serial.print('\n');
    delay(1);
  }
}
