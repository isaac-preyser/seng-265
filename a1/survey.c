/*
Program: survey.c
Author:  Isaac Preyser
Date:    9/18/2024
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LINE_LENGTH 3000
#define MAX_QUESTION_AMOUNT 200
#define MAX_ANSWER_AMOUNT 50
#define MAX_LIKERT_AMOUNT 10

typedef struct {
    char* question; 
    char question_type; //is it type C, I, G, U or P? (corresponds to question category - subtokenizing the question content will be necessary)
    int question_number;
    int is_reverse; //boolean - is the question reverse scored?
}Question;

typedef struct{
    char* major;
    int yes_no; 
    int dob_year; 
    int dob_month;
    int dob_day; 
    char* answer[MAX_QUESTION_AMOUNT]; 
    int scores[MAX_QUESTION_AMOUNT];
}Response;

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

Question constructQuestion(char* question, char* answer_option){
    Question q;
    q.question_type = question[0];
    q.question_number = atoi(&question[1]); //this is a hack lmao
    //check that the question is longer than 4 characters. 
    if (strlen(question) < 4){
        printf("Error: Question is too short. Exiting.\n");
        exit(1);
    }
    q.question = malloc(strlen(question) - 3);
    strncpy(q.question, &question[4], strlen(question) - 4); //we just want the question content. 
    q.question[strlen(question) - 4] = '\0'; //null terminate the string.
    q.is_reverse = 0; //default to false.
    if (answer_option[0] == 'R'){
        q.is_reverse = 1;
    }
    return q;
}

Response getNextResponse(){
    Response r;
    char line[MAX_LINE_LENGTH];
    char *token;

    // Initialize the response with null values
    r.major = NULL;
    r.yes_no = -1;
    r.dob_year = -1;
    r.dob_month = -1;
    r.dob_day = -1;
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        r.answer[i] = NULL;
    }


    while(fgets(line, MAX_LINE_LENGTH, stdin) != (NULL)){
        //if the line starts with a #, skip it. 
        if (line[0] == '#'){
            continue; 
        }
        //otherwise, we are reading a response.
        break; 
    }
    //check if the line is empty. if it is, we are done reading responses.
     if (line[0] == '\0' || feof(stdin)) {
        return r; // Return the "empty" response
    }


    //we need to tokenize the line to grab the appropriate data.
    token = strtok(line, ",\n");
    r.major = malloc(strlen(token) + 1);
    strncpy(r.major, token, strlen(token));
    r.major[strlen(token)] = '\0'; //null terminate the string.
    token = strtok(NULL, ",\n");
    if (strcmp(token, "yes") == 0){
        r.yes_no = 1;
    } else {
        r.yes_no = 0;
    }
    token = strtok(NULL, ",\n");
    // Parse the date of birth using sscanf
    sscanf(token, "%d-%d-%d", &r.dob_year, &r.dob_month, &r.dob_day);
    printf("Debug: Read DOB: %d-%d-%d\n", r.dob_year, r.dob_month, r.dob_day);
    // Read the answers
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        token = strtok(NULL, ",\n");
        if (token == NULL){
            printf("Debug: No more answers, breaking at i=%d\n", i);
            break; 
        }
        r.answer[i] = malloc(strlen(token) + 1);
        strncpy(r.answer[i], token, strlen(token));
        r.answer[i][strlen(token)] = '\0'; //null terminate the string.
        printf("Debug: Read answer[%d]: %s\n", i, r.answer[i]);
    }

    return r;

}

int scoreResponse(){
    
    
    return 0;
}

int main() {
    char* questions[MAX_QUESTION_AMOUNT];
    char* answer_options[MAX_ANSWER_AMOUNT];
    char* likert_options[MAX_LIKERT_AMOUNT];
    int* control_bits = getControlBits();

    getQuestions(questions); 
    getAnswerOptions(answer_options);
    getLikertOptions(likert_options);

    // Commented out debugging code...

    // Construct the questions
    Question q[MAX_QUESTION_AMOUNT];
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i] == NULL) {
            break;
        }
        q[i] = constructQuestion(questions[i], answer_options[i]);
    }

    // Get responses (1 per line until EOF)
    Response responses[MAX_QUESTION_AMOUNT];
    int response_count = 0;
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        responses[i] = getNextResponse();
        if (responses[i].major == NULL) {
            // We've reached the end of the input
            response_count = i;
            break;
        }
    }
    //print out the responses for debugging purposes.
    for (int i = 0; i < response_count; i++){
        printf("Major: %s\n", responses[i].major);
        printf("Yes/No: %d\n", responses[i].yes_no);
        printf("DOB: %d-%d-%d\n", responses[i].dob_year, responses[i].dob_month, responses[i].dob_day);
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++){
            if (responses[i].answer[j] == NULL){
                break; 
            }
            printf("Answer %d: %s\n", j, responses[i].answer[j]);
        }
    }

    // Before we exit, we MUST free the memory
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i] == NULL) {
            break;
        }
        free(questions[i]);
    }
    for (int i = 0; i < MAX_ANSWER_AMOUNT; i++) {
        if (answer_options[i] == NULL) {
            break;
        }
        free(answer_options[i]);
    }
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (likert_options[i] == NULL) {
            break;
        }
        free(likert_options[i]);
    }
    for (int i = 0; i < response_count; i++) {
        if (responses[i].major != NULL) {
            free(responses[i].major);
        }
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++) {
            if (responses[i].answer[j] != NULL) {
                free(responses[i].answer[j]);
            }
        }
    }
    
    return 0;
}