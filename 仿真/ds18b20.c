#include "reg51.h"
#include "intrins.h"     //_nop_();��ʱ������
#define  Disdata    P0   //���������
#define  discan     P2   //ɨ���
#define uchar unsigned char
#define uint unsigned int
sbit  DQ=P3^0;        //�¶������
sbit  DIN=P0^7;       //LEDС�������
sbit jia=P1^0;
sbit jian=P1^1;

uint   h;
uint temperature;

uchar code ditab[16]={0x00,0x01,0x01,0x02,0x03,0x03,0x04,0x04,0x05,0x06,0x06,0x07,0x08,0x08,0x09,0x09};

uchar code dis_7[12]={0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0xff,0xbf};
               
uchar code  scan_con[]={0x7f,0xbf,0xdf,0xef};//0xf7,0xfb,0xfd,0xfe};   // ��ɨ�������
uchar data  temp_data[2]={0x00,0x00};               // �����¶��ݷ�
uchar data  display[5]={0x00,0x00,0x00,0x00,0x00};//��ʾ��Ԫ����,��4������,һ�������ݴ���

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
presence=DQ; // presence=0������һ��
   }
delay(45);    //��ʱ500us
presence = ~DQ;
}
DQ=1;
} 
 
/**********18B20д�����*********/
//�� 1-WIRE ������дһ���ֽ�
void write_byte(uchar val)
{
uchar i;
for (i=8; i>0; i--) //
{
//DQ=0;delay(1); 
DQ=1;nop_();nop_();
DQ=0;nop_();nop_();nop_();nop_();
DQ = val&0x01;      //���λ�Ƴ�
delay(6);           //66us
val=val/2;
DQ=1;          //����һλ
}
DQ = 1;
delay(1);  
}
//
/*********18B20��1���ֽں���********/
//�������϶�ȡһ���ֽ�
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
ow_reset();       //���߸�λ
write_byte(0xCC); // ��Skip ROM����
write_byte(0xBE); //  ��������
temp_data[0]=read_byte();  //�¶ȵ�8λ
temp_data[1]=read_byte();  //�¶ȸ�8λ
ow_reset();
write_byte(0xCC); // Skip ROM
write_byte(0x44); // ��ת������
}

work_temp()//���ݴ���
{
uchar n=0;       //
temperature=((temp_data[1]<<8)|temp_data[0])*0.0625; //�¶ȵ�ʵ��ʮ������ֵ
if(temp_data[1]>127)
 {
 temperature=((temp_data[1]<<8)|temp_data[0]);
  temperature=((~temperature)+1);
  temp_data[1]=temperature/256;
  temp_data[0]=temperature%6;
   n=1;
  }//���¶�����


display[4]=temp_data[0]&0x0f;
display[0]=ditab[display[4]];

display[4]=((temp_data[0]&0xf0)>>4)|((temp_data[1]&0x0f)<<4);

display[3]=display[4]/100;     //display[1]=display[4]%100/10;
display[2]=display[4]%100/10;  //display[1]=display[1]%10;
display[1]=display[4]%100%10;
display[0]=(temp_data[0]%16)*10/16;//С�����һλ

if(display[3]==0){display[3]=0x0a;if(display[2]==0){display[2]=0x0a;}}//���λΪ0ʱ������ʾ

if(n==1){display[3]=0x0b;}  //���¶�ʱ���λ��ʾ"-"
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
Disdata=0xff;    //��ʼ���˿�
discan=0xff;
for(h=0;h<4;h++){display[h]=8;}//������ʾ8888
ow_reset();       // ������ת��һ��
write_byte(0xCC); // Skip ROM
write_byte(0x44); // ��ת������
for(h=0;h<250;h++)
   {scan();}          //������ʾ"8888"1��
while(1)
 {
  read_temp();         //����18B20�¶�����
  work_temp();         //�����¶�����
  for(h=0;h<250;h++){scan();}          //��ʾ�¶�ֵ1��
	if(keyscan())
		flag=
	
  }
}