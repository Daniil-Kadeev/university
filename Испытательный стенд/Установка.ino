// количество датчиков для удобства
#define DS_SENSOR_AMOUNT 6
#define red 7
#define green 8
#define zummer 9
#define button 10
#define mosfet 11
#define test 12


// адреса датиков
uint8_t addr[][8] = {
  {0x28, 0xCA, 0x35, 0x7F, 0x1, 0x0, 0x0, 0x81},
  {0x28, 0x61, 0x52, 0x7F, 0x1, 0x0, 0x0, 0x65},
  {0x28, 0xF8, 0x64, 0x7F, 0x1, 0x0, 0x0, 0x5A},
  {0x28, 0xD9, 0x62, 0x7F, 0x1, 0x0, 0x0, 0x47},
  {0x28, 0xDE, 0x6D, 0x7F, 0x1, 0x0, 0x0, 0xAD},
  {0x28, 0x30, 0x7E, 0x7F, 0x1, 0x0, 0x0, 0xA5}
};
float dat = 0;
bool Flag = 0;



#include <microDS18B20.h>
// указываем DS_ADDR_MODE для подключения блока адресации
// и создаём массив датчиков на пине D2
MicroDS18B20<2, DS_ADDR_MODE> sensor[DS_SENSOR_AMOUNT];

void setup() {
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(zummer, OUTPUT);
  pinMode(button, INPUT);
  pinMode(mosfet, OUTPUT);
  pinMode(test, OUTPUT);
  digitalWrite(test, 1);
  digitalWrite(green, 1);
  digitalWrite(red, 0);
  //digitalWrite(zummer, 0);
  digitalWrite(mosfet, 1);
  Serial.begin(9600);
  Serial.println("CLEARDATA"); // очистка листа excel
  Serial.println("LABEL, Time, Tem1, Tem2, Tem3, Tem4, Tem5, Tem6, Mode");
  for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
    sensor[i].setAddress(addr[i]);
  }
}

void loop() {
  
  // конструкция программного таймера на 1c
  static uint32_t tmr;
  if (millis() - tmr >= 1000) {
    tmr = millis();

    Serial.print("DATA,TIME,"); // запись в excel текущей даты и времени
    // выводим показания в порт
    for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
      dat = sensor[i].getTemp();
      if (dat > 27){
        Flag = 1;
      }
      Serial.print(dat);
      Serial.print(',');
    }

    if (Flag){
      digitalWrite(green, 0);
      digitalWrite(red, 1);
      tone(zummer, 1000, 800);
      digitalWrite(mosfet, 0);
      Serial.print("ACCIDENT");
    }
    //
    if (digitalRead(button)){
      Flag = 0;
      digitalWrite(green, 1);
      digitalWrite(red, 0);
      noTone(zummer);
      digitalWrite(mosfet, 1);
      Serial.print("BUTTON PRESSED");
    }
    Serial.println();

    // запрашиваем новые
    for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
      sensor[i].requestTemp();
    }
  }
}