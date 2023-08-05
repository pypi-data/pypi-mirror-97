// ********************* Define I/O ***************************

// pins utilisées pour le SPI
#define PIN_SCLK      13
#define PIN_MISO      12
#define PIN_MOSI      11

// Pins utilisées pour chip select
#define PIN_CS_DAC  10

// Pins pour local/remote, mode, range
//#define PIN_RANGE_SET  3

// ********************** CONSTANTES **************************
const int DAC_ENABLE_PIN[8] = {9,8,7,6,5,4,3,2};
const int DAC_CHANNEL_MAP[8] = {1,2,0,3,7,4,6,5};

const long ADC_offset = 59; //zero offset in bits
const float ADC_gain = 0.00007762145; //5.087V divided by 2^16
const long DAC_offset[8] = { //zero offset in bits
  9,
  8,
  8,
  9,
  6,
  7,
  7,
  8
};
const float DAC_gain[8] = { //5.000V divided by 2^16
  0.000076194763,
  0.000076194191,
  0.000076188755,
  0.000076189613,
  0.000076207542,
  0.000076207733,
  0.000076212978,
  0.000076210213
};
//5V setpoint = 4.3825A based on 50mohm current sense resistor and 2.4K / 110 ohm divider
const float VOLTS_PER_AMP = -5.8142857; //DAC volts per amp at output
const float VOLTS_PER_AMP_ZERO[8] = { //DAC volts for zero current output
  4.195,
  4.178,
  4.1935,
  4.245,
  4.183,
  4.2275,
  4.287,
  4.202
};
const float AMPS_PER_VOLT = 0.00454545454; //4.54mA per Volt (220 ohm transimpedance)

// ****************** FONCTIONS ***************************
void serialEvent();
int HandleSource(struct SCPI_Command cmd);
int registerSlave(int slaveChan, int masterChan);
