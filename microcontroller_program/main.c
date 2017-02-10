/*
    ChibiOS - Copyright (C) 2006..2015 Giovanni Di Sirio
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
#include "ch.h"
#include "hal.h"
#include "test.h"
#include "pca9685.h"
//#include "i2c_lld.c"
/*
 * LED blinker thread, times are in milliseconds.
 */

static SerialConfig uartCfg = {9600, // bit rate
    };

static THD_WORKING_AREA(waRead, 2048);
msg_t thReader(PCA9685 *arg) {
  char received[1024];
    int pos = 0;
    int count_ch=0;
    int ch0,ch1,ch2,ch3,ch4,ch5;
    uint32_t g= 0;
    uint8_t c;
  while(true){
    while ((char)c !='&'){
        /* This will wait for a character to be received */
        c = sdGet(&SD2);
        //sdPut(&SD2,c);
        received[pos] = (char)c;
        pos++;
      if((char)c==','){
        received[pos] = '\0';
        if(count_ch==0)
                  ch0=trasformToPWM(atoi(received));
        if(count_ch==1)
                  ch1=trasformToPWM(atoi(received));
        if(count_ch==2)
                  ch2=trasformToPWM(atoi(received));
        if(count_ch)
                  ch3=trasformToPWM(atoi(received));
        if(count_ch==4)
                  ch4=trasformToPWM(atoi(received));
        pos=0;
        count_ch++;
      }
    }
    received[pos] ='\0';
    ch5=trasformToPWM(atoi(received));
    chThdSleepMilliseconds(100);
    chprintf((BaseSequentialStream *)&SD2,"%d,%d,%d,%d,%d,%d\n",ch0,ch1,ch2,ch3,ch4,ch5);
    if(ch0!=-1){
      setPWM(arg, 0, 0, ch0);
      //chThdSleepMilliseconds(100);
    }
    if(ch0!=-1){
      setPWM(arg, 1, 0, ch1);
      //chThdSleepMilliseconds(100);
    }
    if(ch0!=-1){
      setPWM(arg, 2, 0, ch2);
      //chThdSleepMilliseconds(100);
    }
    if(ch0!=-1){
      setPWM(arg, 3, 0, ch3);
     // chThdSleepMilliseconds(100);
    }
    if(ch0!=-1){
      setPWM(arg, 4, 0, ch4);
    //  chThdSleepMilliseconds(100);
    }
    if(ch0!=-1){
      setPWM(arg, 5, 0, ch5);
    //  chThdSleepMilliseconds(100);
    }
    chThdSleepMilliseconds(100);
    pos=0;
    count_ch=0;
    c=0;

   // chprintf((BaseSequentialStream *)&SD2,"get: %lu",( unsigned long )getPWM(arg,ch0));
  }
}


/*
 * Application entry point.
 */
int main(void) {
  /*
   * System initializations.
   * - HAL initialization, this also initializes the configured device drivers
   *   and performs the board-specific initializations.
   * - Kernel initialization, the main() function becomes a thread and the
   *   RTOS is active.
   */
  halInit();
  chSysInit();
  /*
   * Activates the serial driver 2 using the driver default configuration.
   */
  sdStart(&SD2, &uartCfg);

   palSetPadMode(GPIOB, 8, PAL_MODE_ALTERNATE(4) | PAL_STM32_OTYPE_OPENDRAIN);
   palSetPadMode(GPIOB, 9, PAL_MODE_ALTERNATE(4) | PAL_STM32_OTYPE_OPENDRAIN);

   /**
      * Prepares the PCA9685
      */
   PCA9685 pca9685;
   pca9685.i2caddress = PCA9685_ADDRESS;
   pca9685.driver = &PCA9685_DEFI2C_DRIVER;
   pca9685.pwm_frequency = PCA9685_FREQ;
   pca9685.config = &PCA9685_I2C_CONFIG;
   pca9685.acquire = TRUE;
   /*
     * Starts I2C
     */
   i2cStart(pca9685.driver, pca9685.config);

   reset(&pca9685);

   setFreq(&pca9685, pca9685.pwm_frequency);

   chThdCreateStatic(waRead, sizeof(waRead), NORMALPRIO, thReader, &pca9685);

  /*
   * Normal main() thread activity, in this demo it does nothing except
   * sleeping in a loop and check the button state.
   */
  while (true) {
    if (!palReadPad(GPIOC, GPIOC_BUTTON))
      TestThread(&SD2);
    chThdSleepMilliseconds(500);
  }
}
