/*
Program: survey.c
Author:  Isaac Preyser
Date:    9/18/2024
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int* getControlBits() {
    static int control_bits[4];
    char line[3000];
    char *token;
    int line_number = 0;

    while(fgets(line, 3000, stdin) != (NULL)){
        line_number++; //for debug purposes. 
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ",");
        int i = 0;
        while (token != NULL && i < 4) {
            control_bits[i] = atoi(token);
            token = strtok(NULL, ",");
            i++;
        }
        break; 
    }

    return control_bits;
}


int main() {

    int* control_bits = getControlBits();

    // Print control bits for debugging
    printf("Control Bits: \n");
    for(int i = 0; i < 4; i++) {
        printf("  Bit %d: %d\n", i, control_bits[i]);
    }

    return 0;
}
