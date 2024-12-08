void setup() {
  Serial.begin(115200); // Start serial communication at 9600 baud rate
}

void loop() {
  // Read digital pins
  int digitalPin2 = digitalRead(2);
  int digitalPin3 = digitalRead(3);
  
  // Read analog pins
  int analogPin0 = analogRead(A0);
  int analogPin1 = analogRead(A1);
  
  // Send the pin status to the serial port
  Serial.print("D2:"); Serial.print(digitalPin2);
  Serial.print(" D3:"); Serial.print(digitalPin3);
  Serial.print(" A0:"); Serial.print(analogPin0);
  Serial.print(" A1:"); Serial.println(analogPin1);
  
  delay(1000); // Wait for 1 second before sending the next data
}