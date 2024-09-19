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


void getQuestions(char *arr[]) {
    char line[3000];
    char *token;
    int line_number = 0;

    while(fgets(line, 3000, stdin) != (NULL)){
        line_number++; //for debug purposes. 
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ";");
        int i = 0;
        while (token != NULL) {
            //malloc space for the question
            arr[i] = (char*)malloc(strlen(token) + 1);
            //copy the question into the array
            strcpy(arr[i], token);
            //get the next token
            token = strtok(NULL, ";");
            i++;
        } 
        //make the rest of the questions array NULL
        for (int j = i; j < 200; j++) {
            arr[j] = NULL;
        }

        break; //we only want the first line of questions.
    }
    return;

}


int main() {
    const int MAX_QUESTION_LENGTH = 3000;
    char* questions[200];

    int* control_bits = getControlBits();
    
    getQuestions(questions); 
    // Print control bits for debugging
    printf("Control Bits: \n");
    for(int i = 0; i < 4; i++) {
        printf("  Bit %d: %d\n", i, control_bits[i]);
    }
    // Print questions for debugging
   for (int i = 0; i < 200; i++) {
        if (questions[i] == NULL) {
            break;
        }
        printf("Question %d: %s\n", i, questions[i]);
    }
    return 0;
}
