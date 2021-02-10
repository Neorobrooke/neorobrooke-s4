#define pinEncodeur1 22 
#define pinEncodeur2 23

bool encodeur1 = 0;
bool encodeur2 = 0;
int state = 0;
int lastState = 0;
int distance = 0;

void setup() {
  // put your setup code here, to run once:
pinMode(pinEncodeur1,INPUT);
pinMode(pinEncodeur2,INPUT);
Serial.begin(9600);

}

void loop() {
    // put your main code here, to run repeatedly:
  encodeur1 = digitalRead(pinEncodeur1);
  encodeur2 = digitalRead(pinEncodeur2);
  state = encodeur1+encodeur2*10;
   
  
  if (state!=lastState){
    Serial.println(distance);
    switch(state){
      case 0:
        if (lastState == 10){
          distance ++;
        }else if(lastState == 1){
          distance --;
        }
        //Serial.println("1000");
        break;
      case 1:
        if (lastState == 0){
          distance ++;
        }else if (lastState == 11){
          distance --;
        }
        //Serial.println("0100");
        break;
      case 11:
        if (lastState == 1){
          distance ++;
        }else if(lastState == 10){
          distance --;
        }
        //Serial.println("0010");
        break;
      case 10:
        if (lastState == 11){
          distance ++;
        }else{
          distance --;
        }
        //Serial.println("0001"); 
        break;   
    }
    
  }
  lastState = state;
  
}
