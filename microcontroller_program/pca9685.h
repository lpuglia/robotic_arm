/*
 * pca9685.h
 *
 *  Created on: 05/gen/2017
 *      Author: Ciccio
 */

#ifndef PCA9685_H_
#define PCA9685_H_

/*
 * Internal clock frequency - 25Mhz
 */
#define PCA9685_CLOCK 25000000
#define PCA9685_ADDRESS 0x40
/*
 * Default PWM frequency.
 */
#define PCA9685_FREQ 60
static const I2CConfig PCA9685_I2C_CONFIG = {
    OPMODE_I2C,
    400000,
    FAST_DUTY_CYCLE_2,
};
/** @brief I2C1 driver identifier.*/
/* See 7.3 Register definitions */
#define PCA9685_MODE1 0x00
#define PCA9685_MODE2 0x01
#define PCA9685_ALLCALLADR 0x05
#define PCA9685_PRESCALE 0xFE
/* See 7.3.1 Mode register 1, MODE1 */
#define PCA9685_MODE1_RESTART 0x80
#define PCA9685_MODE1_EXTCLK 0x40
#define PCA9685_MODE1_AI 0x20
#define PCA9685_MODE1_SLEEP 0x10
#define PCA9685_MODE1_SUB1 0x08
#define PCA9685_MODE1_SUB2 0x04
#define PCA9685_MODE1_SUB3 0x02
#define PCA9685_MODE1_ALLCALL 0x01
/* 7.3.2 Mode register 2, MODE2 */
#define PCA9685_MODE2_INVRT 0x10
#define PCA9685_MODE2_OCH 0x08
#define PCA9685_MODE2_OUTDRV 0x04
#define PCA9685_MODE2_OUTNE 0x03 //Actually a mask of bits. Paragraph 7.3.2 Mode register 2, MODE2
#define LED0_ON_L 0x6
#define LED0_ON_H 0x7
#define LED0_OFF_L 0x8
#define LED0_OFF_H 0x9
#define PCA9685_DEFI2C_PORT GPIOB
#define PCA9685_DEFI2C_SCL_PAD 10
#define PCA9685_DEFI2C_SDA_PAD 11
#define PCA9685_DEFI2C_MODE PAL_STM32_OTYPE_OPENDRAIN | PAL_STM32_OSPEED_MID2 | PAL_MODE_ALTERNATE(4)
#define PCA9685_DEFI2C_SPEED 400000
#define PCA9685_DEFI2C_DRIVER I2CD1

typedef struct PCA9685 {
    uint8_t i2caddress;
    I2CDriver *driver;
    const I2CConfig *config;
    bool acquire;
    uint8_t rxbuf[32];
    uint8_t txbuf[32];
    msg_t status;
    systime_t tmo;
    uint32_t pwm_frequency;
    uint8_t pwm_channel;
} PCA9685;
uint8_t readreg(PCA9685 *pca9685, uint8_t reg)
{
  if(reg < 70 || reg > 249)
  {
     pca9685->tmo = MS2ST(4);
     if(pca9685->acquire)
       i2cAcquireBus(pca9685->driver);
     pca9685->status = i2cMasterTransmitTimeout(pca9685->driver,pca9685->i2caddress, &reg, 1, pca9685->rxbuf, 1, pca9685->tmo);
     if(pca9685->acquire)
          i2cReleaseBus(pca9685->driver);
  }
  return pca9685->rxbuf[0];
}
void writereg(PCA9685 *pca9685, uint8_t reg, uint8_t data)
{
     pca9685->txbuf[0] = reg;//register address
     pca9685->txbuf[1] = data;
     pca9685->tmo = MS2ST(4);
     if(pca9685->acquire)
       i2cAcquireBus(pca9685->driver);
     pca9685->status = i2cMasterTransmitTimeout(pca9685->driver,pca9685->i2caddress, pca9685->txbuf, 2, pca9685->rxbuf, 0, pca9685->tmo);
     if(pca9685->acquire)
          i2cReleaseBus(pca9685->driver);
}
void reset(PCA9685 *pca9685)
{
  writereg(pca9685, PCA9685_MODE1, 0x00);
  chThdSleepMilliseconds(1);
}
void setFreq(PCA9685 *pca9685, uint32_t freq)
{
      uint8_t prescale = (uint8_t)(int) (PCA9685_CLOCK / (4096 * freq)) - 1;
      if (prescale < 3)
          prescale = 3;
      uint8_t oldmode = readreg(pca9685, PCA9685_MODE1); //Preserve old mode
      uint8_t newmode = (oldmode & !PCA9685_MODE1_RESTART) | PCA9685_MODE1_SLEEP; // Don't change any MODE1 bit except set SLEEP bit 1 and RESTART bit goes 0
      writereg(pca9685, PCA9685_MODE1, newmode); // go to sleep, shutting the oscillator off
      writereg(pca9685, PCA9685_PRESCALE, prescale); // set the prescaler
      writereg(pca9685, PCA9685_MODE1, oldmode);
      chThdSleepMicroseconds(500);//Wait 0.5ms for oscillator stabilisation
      writereg(pca9685, PCA9685_MODE1, oldmode | PCA9685_MODE1_ALLCALL | PCA9685_MODE1_AI | PCA9685_MODE1_RESTART);
      pca9685->pwm_frequency = freq;
}
void setPWM(PCA9685 *pca9685, uint8_t channel, uint16_t on, uint16_t off)
{
     pca9685->pwm_channel = channel;
     pca9685->txbuf[0] = LED0_ON_L + 4 * channel;
     pca9685->txbuf[1] = on & 0x00FF;
     pca9685->txbuf[2] = on >> 8;
     pca9685->txbuf[3] = off & 0x00FF;
     pca9685->txbuf[4] = off >> 8;
     pca9685->tmo = MS2ST(4);
     if(pca9685->acquire)
            i2cAcquireBus(pca9685->driver);
          pca9685->status = i2cMasterTransmitTimeout(pca9685->driver,pca9685->i2caddress, pca9685->txbuf, 5, pca9685->rxbuf, 0, pca9685->tmo);
          if(pca9685->acquire)
               i2cReleaseBus(pca9685->driver);
}
uint32_t  getPWM(PCA9685 *pca9685,uint8_t channel) {
    uint32_t pwm = 0;
    uint16_t pwm1 =0;

    pwm = (readreg(pca9685,(LED0_ON_L+4*channel) + 2) & 0x0F) << 8;
    pwm |= readreg(pca9685,(LED0_ON_L+4*channel) + 3);
    pwm = pwm << 16; //Shift all by 16 bits, first half contains on period counter
    pwm |= (readreg(pca9685,(LED0_ON_L+4*channel) + 1) & 0x0F) << 8;
    pwm |= readreg(pca9685,LED0_ON_L+4*channel); //The other half will contain off period counter

    return pwm;
//    pwm1=pwm>>16;
//    pwm1=(pwm1*400)/4096;
//    return pwm1;
}

int  trasformToPWM(int grado) {
   if(grado==-1)
     return grado;
   if(grado==0)
     return 150;
   if(grado==180)
     return 750;
   if(grado==-2)
        return 0;

   return (900*grado)/180;
}
#endif /* OS_RT_INCLUDE_PCA9685_H_ */
