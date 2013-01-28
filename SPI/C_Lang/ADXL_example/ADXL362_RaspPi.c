#include <bcm2835.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    
    if (!bcm2835_init())
        return 1;
    
    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // The default
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                   // The default
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_65536); // The default
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                      // The default
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);      // the default
    
    char buf[] = { 0x0B, 0x00, 0x00}; // Read DeviceID of ADXL362
    bcm2835_spi_transfern(buf, sizeof(buf));
    // buf will now be filled with the data that was read from the slave
    printf("Device ID: %02X \n", buf[2]);
    
    char buf1[] = {0x0A, 0x1F, 0x52}; // Soft Reset
    bcm2835_spi_transfern(buf1, sizeof(buf1));

    delay(1000);

    char buf2[] = {0x0A, 0x2D, 0x02}; // Setup for Measure
    bcm2835_spi_transfern(buf2, sizeof(buf2));

    delay(1000);

    char buf3[] = {0x0B, 0x0E, 0x00, 0x00}; // Read X
    bcm2835_spi_transfern(buf3, sizeof(buf3));
    printf("X Axis is: %02X %02X \n", buf3[3], buf3[2]);

    delay(1000);
    printf("Device ID: %02X \n", buf[2]);
    
    char buf4[] = {0x0A, 0x1F, 0x52}; // Soft Reset
    bcm2835_spi_transfern(buf1, sizeof(buf1));

    delay(1000);

    char buf5[] = {0x0A, 0x2D, 0x02}; // Setup for Measure
    bcm2835_spi_transfern(buf2, sizeof(buf2));

    delay(1000);

    char buf6[] = {0x0B, 0x0E, 0x00, 0x00}; // Read X
    bcm2835_spi_transfern(buf3, sizeof(buf3));
    printf("X Axis is: %02X %02X \n", buf3[3], buf3[2]);

    delay(1000);

    char buf7[] = {0x0B, 0x0E, 0x00, 0x00}; // Read X
    bcm2835_spi_transfern(buf4, sizeof(buf4));
    printf("X Axis is: %02X %02X \n", buf4[3], buf4[2]);

    bcm2835_spi_end();
    return 0;
}