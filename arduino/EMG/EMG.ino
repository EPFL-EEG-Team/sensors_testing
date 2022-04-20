//Unit testing EMG
//Lights up an LED when you make a movement
//Tested on Arduino Uno
float v;
float threshold_high = 400;
float threshold_low = 200;
int on;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  v = analogRead(0);  
  Serial.println(v);
  if(v > threshold_high && on == 0){
    on = 1;
  }else if(on == 1 && v < threshold_low){
    on = 0;
  }
  if(on){
    digitalWrite(LED_BUILTIN, HIGH);
  }else{
    digitalWrite(LED_BUILTIN, HIGH);
  }

}
