#define pinEncodeur1 18
#define pinEncodeur2 19

int state = 0;
int lastState = 0;
int distance = 0;

long temps = 0;
volatile bool tic = false;
volatile bool up = true;
const double mmParTic = 0.75071069;

int changeDistance() {
  if (up && digitalRead(pinEncodeur2) || !up && !digitalRead(pinEncodeur2)) {
    distance ++;
  } 
  else {
    distance --;
  }
  up = !up;
}
void setup() {
  // put your setup code here, to run once:
  pinMode(pinEncodeur1, INPUT);
  pinMode(pinEncodeur2, INPUT);
  up = digitalRead(pinEncodeur1);
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(pinEncodeur1), changeDistance, CHANGE);
}

void loop() {
  delay(1000);
  Serial.println(distance * mmParTic);
}
