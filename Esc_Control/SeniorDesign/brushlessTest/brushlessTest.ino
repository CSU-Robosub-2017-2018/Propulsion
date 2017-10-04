#include<Servo.h>

Servo esc;
int val=1000;
void setup()
{
  esc.attach(10);
  Serial.begin(9600);
}


void loop()
{
  if(Serial.available()){
  val= Serial.parseInt(); }
  esc.writeMicroseconds(val);
  Serial.println(val);
  delay(1);
}

