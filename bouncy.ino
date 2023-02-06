#include <Wire.h>
#include <U8g2lib.h>
#define PI 3.1415926535897932384626433832795

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

float screen_width =128;
float screen_height=64;
float ball_x=screen_width/2;
float ball_y=screen_height/2;
float ball_radius = 4;
float ball_angle  = 0;
float ball_speed = 10.0;

void setup() 
{
  Serial.begin(9600);  
  Wire.begin();
  u8g2.begin();
  u8g2_prepare();
  randomSeed(analogRead(0));
  ball_angle = random(1, 360);  
  
  ball_radius = random(1, 10);
  ball_speed = random(1, 15);  

  ball_x = random(10, 118);
  ball_y = random(10, 54);
}

void u8g2_prepare(void) 
{
  u8g2.enableUTF8Print();
  u8g2.setFont(u8g2_font_9x18B_tf);
  u8g2.setFontRefHeightExtendedText();
  u8g2.setDrawColor(1);
  u8g2.setFontPosTop();
  u8g2.setFontDirection(0);
}

void showball() 
{
    u8g2.drawStr( 0, 0, "Bouncy Ball");
    u8g2.clearBuffer(); // clear the internal memory
  //  u8g2.drawFrame(1,1,127,63);   
    u8g2.drawDisc(ball_x,ball_y,ball_radius);
    u8g2.sendBuffer();
}  

void loop() 
{
  ball_x += cos(ball_angle) * ball_speed;
  ball_y += sin(ball_angle) * ball_speed;
  
  if ( ball_x - ball_radius < 0 )
  {
     ball_x = ball_radius;
     ball_angle = PI - ball_angle;
  }
  else if ( ball_x + ball_radius > screen_width ) 
  {
     ball_x = screen_width - ball_radius;
     ball_angle = PI - ball_angle;
  }
  
  if ( ball_y < ball_radius ) 
  {
     ball_y = ball_radius;
     ball_angle = ( PI * 2 ) - ball_angle;
  }
  else if ( ball_y + ball_radius > screen_height )
  {
     ball_y = screen_height - ball_radius;
     ball_angle = ( PI * 2 ) - ball_angle;
  }
  
  showball();
  delay(1);
}
