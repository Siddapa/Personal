//
//  How to access GPIO registers from C-code on the Raspberry-Pi
//  Example program
//  15-January-2012
//  Dom and Gert
//  Revised: 15-Feb-2013

// Access from ARM Running Linux

#define BCM2708_PERI_BASE 0x3F000000
#define GPIO_BASE (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE (4 * 1024)
#define BLOCK_SIZE (4 * 1024)

int mem_fd;
void *gpio_map;

// I/O access
volatile unsigned *gpio;

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio + ((g) / 10)) &= ~(7 << (((g) % 10) * 3))
#define OUT_GPIO(g) *(gpio + ((g) / 10)) |= (1 << (((g) % 10) * 3))
#define SET_GPIO_ALT(g, a) *(gpio + (((g) / 10))) |= (((a) <= 3 ? (a) + 4 : (a) == 4 ? 3  \
                                                                                     : 2) \
                                                      << (((g) % 10) * 3))

#define GPIO_SET *(gpio + 7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio + 10) // clears bits which are 1 ignores bits which are 0

#define GET_GPIO(g) (*(gpio + 13) & (1 << g)) // 0 if LOW, (1<<g) if HIGH

#define GPIO_PULL *(gpio + 37)     // Pull up/pull down
#define GPIO_PULLCLK0 *(gpio + 38) // Pull up/pull down clock

void setup_io();

void output(int start_bit, int end_bit, int start_pin, int end_pin);

void printButton(int g)
{
    if (GET_GPIO(g)) // !=0 <-> bit is 1 <- port is HIGH=3.3V
        printf("Button pressed!\n");
    else // port is LOW=0V
        printf("Button released!\n");
}

void main(int argc, char **argv)
{
    int g, rep;

    // Set up gpi pointer for direct register access
    setup_io();

    // Switch GPIO 7..11 to output mode

    /************************************************************************\
  * You are about to change the GPIO settings of your computer.          *
  * Mess this up and it will stop working!                               *
  * It might be a good idea to 'sync' before running this program        *
  * so at least you still have your code changes written to the SD-card! *
 \************************************************************************/
    
    for (i = 0; i <= 15, i++)
    {
        INP_GPIO(i);
        OUT_GPIO(i);
    }

    char red_filename[] = "red.txt";
    char green_filename[] = "green.txt";
    char blue_filename[] = "blue.txt";
    FILE* red_bin = fopen(red_filename, "r");
    FILE* green_bin = fopen(green_filename, "r");
    FILE* blue_bin = fopen(blue_filename, "r");
    int red_count = 0;
    int green_count = 0;
    int blue_count = 0;

    if (red_bin == NULL || green_bin == NULL || blue_bin == NULL){
        printf("File is not available \n");
    }
    else{
        for (c = getc(red_bin); c != EOF; c = getc(red_bin)){
            red_count = red_count + 1
        }
        for (c = getc(green_bin); c != EOF; c = getc(green_bin)){
            green_count = green_count + 1
        }
        for (c = getc(red_bin); c != EOF; c = getc(red_bin)){
            blue_count = blue_count + 1
        }
    }

    int red_bits[red_count];
    int green_bits[green_count];
    int blue_bits[blue_count];
    int index = 0;
    while ((ch = fgetc(red_bin)) != EOF){
        red_vals[index] = ch;
        index = index + 1;
    }
    index = 0;
    while ((ch = fgetc(green_bin)) != EOF){
        green_vals[index] = ch;
        index = index + 1;
    }
    index = 0;
    while ((ch = fgetc(blue_bin)) != EOF){
        blue_vals[index] = ch;
        index = index + 1;
    }

    for (int i = 0; i <= index/5; i++){
        output(red_bits[(i*5)..((i+1)*5)], 0, 4)
        output(green_bits[(i*6)..((i+1)*6)], 5, 10)
        output(blue_bits[(i*5)..((i+1)*5)], 11, 15)
    }

    fclose(red_bin);
    fclose(green_bin);
    fclose(blue_bin);
} // main

//
// Set up a memory regions to access GPIO
//
void setup_io()
{
    /* open /dev/mem */
    if ((mem_fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0)
    {
        printf("can't open /dev/mem \n");
        exit(-1);
    }

    /* mmap GPIO */
    gpio_map = mmap(
        NULL,                   //Any adddress in our space will do
        BLOCK_SIZE,             //Map length
        PROT_READ | PROT_WRITE, // Enable reading & writting to mapped memory
        MAP_SHARED,             //Shared with other processes
        mem_fd,                 //File to map
        GPIO_BASE               //Offset to GPIO peripheral
    );

    close(mem_fd); //No need to keep mem_fd open after mmap

    if (gpio_map == MAP_FAILED)
    {
        printf("mmap error %d\n", (int)gpio_map); //errno also set!
        exit(-1);
    }

    // Always use volatile pointer!
    gpio = (volatile unsigned *)gpio_map;

} // setup_io


void output(int bits[], int start_pin, int end_pin){
    for (int i = start_pin; i <= end_pin, i++){
        if (bits[i] == 1){
            GPIO_SET = 1<<i
            GPIO_CLR = 1<<i
        } else if (bits[i] == 0) {
            GPIO_CLR = 1<<i
        }
    }
}
