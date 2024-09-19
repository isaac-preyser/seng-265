/*
Program: survey.c
Author:  Isaac Preyser
Date:    9/18/2024
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const int MAX_LINE_LENGTH = 3000;
const int MAX_QUESTION_AMOUNT = 200;
const int MAX_ANSWER_AMOUNT = 50;
const int MAX_LIKERT_AMOUNT = 10;


int* getControlBits() {
    static int control_bits[4];
    char line[MAX_LINE_LENGTH];
    char *token;
    int line_number = 0;

    while(fgets(line, MAX_LINE_LENGTH, stdin) != (NULL)){
        line_number++; //for debug purposes. 
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ",\n");
        int i = 0;
        while (token != NULL && i < 4) {
            control_bits[i] = atoi(token);
            token = strtok(NULL, ",\n");
            i++;
        }
        break; 
    }

    return control_bits;
}


void getQuestions(char *arr[]) {
    char line[MAX_LINE_LENGTH];
    char *token;

    while(fgets(line, MAX_LINE_LENGTH, stdin) != (NULL)){
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ";\n");
        int i = 0;
        while (token != NULL) {
            //malloc space for the question (epic casts for the win)
            arr[i] = (char*)malloc(strlen(token) + 1);
            //copy the question into the array
            strncpy(arr[i], token, strlen(token));
            //get the next token
            token = strtok(NULL, ";\n");
            i++;
        } 
        //make the rest of the questions array NULL
        for (int j = i; j < MAX_QUESTION_AMOUNT; j++) {
            arr[j] = NULL;
        }

        break; //we only want the first line of questions.
    }
    return;

}

void getAnswerOptions(char* arr[]){
    char line[MAX_LINE_LENGTH];
    char *token;

    //get the answers. 
    while(fgets(line, MAX_LINE_LENGTH, stdin) != (NULL)){
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ";\n");
        int i = 0;
        while (token != NULL) {
            //malloc space for the question (epic casts for the win)
            arr[i] = (char*)malloc(strlen(token) + 1);
            //copy the question into the array
            strncpy(arr[i], token, strlen(token));
            //get the next token
            token = strtok(NULL, ";\n");
            i++;
        } 
        //make the rest of the questions array NULL
        for (int j = i; j < MAX_ANSWER_AMOUNT; j++) {
            arr[j] = NULL;
        }

        break; //we only want the first line of questions.
    }
}

void getLikertOptions(char* arr[]){
    char line[MAX_LINE_LENGTH];
    char *token;

    //get the answers. 
    while(fgets(line, MAX_LINE_LENGTH, stdin) != (NULL)){
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        token = strtok(line, ",\n");
        int i = 0;
        while (token != NULL) {
            //malloc space for the question (epic casts for the win)
            arr[i] = (char*)malloc(strlen(token) + 1);
            //copy the question into the array
            strncpy(arr[i], token, strlen(token));
            //get the next token
            token = strtok(NULL, ",\n");
            i++;
        } 
        //make the rest of the questions array NULL
        for (int j = i; j < MAX_LIKERT_AMOUNT; j++) {
            arr[j] = NULL;
        }

        break; //we only want the first line of questions.
    }
}


int main() {
    char* questions[MAX_QUESTION_AMOUNT];
    char* answer_options[MAX_ANSWER_AMOUNT];
    char* likert_options[MAX_LIKERT_AMOUNT];
    int* control_bits = getControlBits();

    getQuestions(questions); 
    getAnswerOptions(answer_options);
    getLikertOptions(likert_options);
    // Print control bits for debugging
    printf("Control Bits: \n");
    for(int i = 0; i < 4; i++) {
        printf("  Bit %d: %d\n", i, control_bits[i]);
    }
    // Print questions for debugging
   for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i] == NULL) {
            break;
        }
        printf("Question %d: %s\n", i, questions[i]);
    }
    // Print answer options for debugging
    for (int i = 0; i < MAX_ANSWER_AMOUNT; i++) {
        if (answer_options[i] == NULL) {
            break;
        }
        printf("Answer %d: %s\n", i, answer_options[i]);
    }
    // Print likert options for debugging
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (likert_options[i] == NULL) {
            break;
        }
        printf("Likert %d: %s\n", i, likert_options[i]);
    }
    return 0;
}
