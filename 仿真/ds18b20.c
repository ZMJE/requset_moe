#include "reg51.h"
#include "intrins.h"     //_nop_();延时函数用
#define  Disdata    P0   //段码输出口
#define  discan     P2   //扫描口
#define uchar unsigned char
#define uint unsigned int
sbit  DQ=P3^0;        //温度输入口
sbit  DIN=P0^7;       //LED小数点控制
sbit jia=P1^0;
sbit jian=P1^1;

uint   h;
uint temperature;

uchar code ditab[16]={0x00,0x01,0x01,0x02,0x03,0x03,0x04,0x04,0x05,0x06,0x06,0x07,0x08,0x08,0x09,0x09};

uchar code dis_7[12]={0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0xff,0xbf};
               
uchar code  scan_con[]={0x7f,0xbf,0xdf,0xef};//0xf7,0xfb,0xfd,0xfe};   // 列扫描控制字
uchar data  temp_data[2]={0x00,0x00};               // 读出温度暂放
uchar data  display[5]={0x00,0x00,0x00,0x00,0x00};//显示单元数据,共4个数据,一个运算暂存用

void delay(uint t)
{
for(;t>0;t--);
}
//
  void scan()
 {
   char k;  // Disdata=0;
   for(k=0;k<4;k++)
     {
      discan=scan_con[k]; //P2
      Disdata=dis_7[display[k]];//P1
      if(k==1) DIN=0;//DIN=1;
      delay(90);
     }
 }

ow_reset(void)
{
char presence=1;
while(presence)
{
while(presence)
  {
DQ=1;_nop_();_nop_();
DQ=0;    
delay(50); // 550us
DQ=1;   
delay(6);  // 66us
presence=DQ; // presence=0继续下一步
   }
delay(45);    //延时500us
presence = ~DQ;
}
DQ=1;
} 
 
/**********18B20写命令函数*********/
//向 1-WIRE 总线上写一个字节
void write_byte(uchar val)
{
uchar i;
for (i=8; i>0; i--) //
{
//DQ=0;delay(1); 
DQ=1;nop_();nop_();
DQ=0;nop_();nop_();nop_();nop_();
DQ = val&0x01;      //最低位移出
delay(6);           //66us
val=val/2;
DQ=1;          //右移一位
}
DQ = 1;
delay(1);  
}
//
/*********18B20读1个字节函数********/
//从总线上读取一个字节
uchar read_byte(void)
{
uchar i;
uchar value = 0;
for (i=8;i>0;i--)
{
DQ=1;_nop_();_nop_();
value>>=1;
DQ = 0;             //
_nop_();_nop_();_nop_();_nop_();   //4us
DQ = 1;
_nop_();_nop_();_nop_();_nop_();   //4us 
if(DQ)value|=0x80;
delay(3);           //30us
}
DQ=1;
return(value);
}


read_temp()
{
ow_reset();       //总线复位
write_byte(0xCC); // 发Skip ROM命令
write_byte(0xBE); //  发读命令
temp_data[0]=read_byte();  //温度低8位
temp_data[1]=read_byte();  //温度高8位
ow_reset();
write_byte(0xCC); // Skip ROM
write_byte(0x44); // 发转换命令
}

work_temp()//数据处理
{
uchar n=0;       //
temperature=((temp_data[1]<<8)|temp_data[0])*0.0625; //温度的实际十进制数值
if(temp_data[1]>127)
 {
 temperature=((temp_data[1]<<8)|temp_data[0]);
  temperature=((~temperature)+1);
  temp_data[1]=temperature/256;
  temp_data[0]=temperature%6;
   n=1;
  }//负温度求补码


display[4]=temp_data[0]&0x0f;
display[0]=ditab[display[4]];

display[4]=((temp_data[0]&0xf0)>>4)|((temp_data[1]&0x0f)<<4);

display[3]=display[4]/100;     //display[1]=display[4]%100/10;
display[2]=display[4]%100/10;  //display[1]=display[1]%10;
display[1]=display[4]%100%10;
display[0]=(temp_data[0]%16)*10/16;//小数点后一位

if(display[3]==0){display[3]=0x0a;if(display[2]==0){display[2]=0x0a;}}//最高位为0时都不显示

if(n==1){display[3]=0x0b;}  //负温度时最高位显示"-"
}

char keyscan()
{
	if(jia==0||jian==0)
	{
		delay(100);
		if(jia==0)
			return 1;
		else if(jian==0)
			return 2;
		else
			return 0;
			
	}
}

main()
{
	int flag=0;
Disdata=0xff;    //初始化端口
discan=0xff;
for(h=0;h<4;h++){display[h]=8;}//开机显示8888
ow_reset();       // 开机先转换一次
write_byte(0xCC); // Skip ROM
write_byte(0x44); // 发转换命令
for(h=0;h<250;h++)
   {scan();}          //开机显示"8888"1秒
while(1)
 {
  read_temp();         //读出18B20温度数据
  work_temp();         //处理温度数据
  for(h=0;h<250;h++){scan();}          //显示温度值1秒
	if(keyscan())
		flag=
	
  }
}