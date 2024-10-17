// количество датчиков для удобства
#define DS_SENSOR_AMOUNT 6

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





#include <microDS18B20.h>
// указываем DS_ADDR_MODE для подключения блока адресации
// и создаём массив датчиков на пине D2
MicroDS18B20<4, DS_ADDR_MODE> sensor[DS_SENSOR_AMOUNT];

void setup() {

  Serial.begin(9600);

  Serial.println("CLEARDATA"); // очистка листа excel
  Serial.println("LABEL, Time, Tem1, Tem2, Tem3, Tem4, Tem5, Tem6");
  for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
    sensor[i].setAddress(addr[i]);
  }
}


void loop() {
  // конструкция программного таймера на 1c
  static uint32_t tmr;
  if (millis() - tmr >= 2000) {
    tmr = millis();
    Serial.print("DATA,TIME,"); // запись в excel текущей даты и времени	

    for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
      dat = sensor[i].getTemp();
      Serial.print(dat);
      Serial.print(',');
    }
    Serial.println();
    

    // запрашиваем новые
    for (int i = 0; i < DS_SENSOR_AMOUNT; i++) {
      sensor[i].requestTemp();
    }
  }
}
// отправляет состояние на лампы
