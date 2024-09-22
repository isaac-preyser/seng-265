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
    static int control_bits[4] = {0};  // initialize to zero
    char line[MAX_LINE_LENGTH];

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        // skip comment lines
        if (line[0] == '#') {
            continue;
        }

        // try to parse 4 integers from the line
        int parsed = sscanf(line, "%d,%d,%d,%d", 
                            &control_bits[0], &control_bits[1], 
                            &control_bits[2], &control_bits[3]);

        // if we parsed at least one integer, we're done
        if (parsed > 0) {
            break;
        }
        // if we couldn't parse any integers, continue to the next line
    }

    return control_bits;
}


void getOptions(char *arr[], int max_size, const char *delimiters) {
    char line[MAX_LINE_LENGTH];
    char *token;

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#') {
            continue;
        }
        
        int i = 0;
        token = strtok(line, delimiters);
        while (token != NULL && i < max_size) {
            size_t token_len = strlen(token); //slightly smaller than an int, and avoids recomputing the length of the token.
            arr[i] = malloc(token_len + 1);
            if (arr[i] == NULL) {
                fprintf(stderr, "Memory allocation failed\n");
                exit(1);
            }
            strncpy(arr[i], token, token_len);
            arr[i][token_len] = '\0';  // ensure null-termination
            token = strtok(NULL, delimiters);
            i++;
        }

        // null-terminate the rest of the array
        for (int j = i; j < max_size; j++) {
            arr[i] = NULL;
        }

        break;  // we only want the first non-comment line
    }
}

//these really don't need to be separate functions, but I'm doing it for the sake of readability.
void getQuestions(char *arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getAnswerOptions(char *arr[]) {
    getOptions(arr, MAX_ANSWER_AMOUNT, ";\n");
}

void getLikertOptions(char *arr[]) {
    getOptions(arr, MAX_LIKERT_AMOUNT, ",\n");
}

Question constructQuestion(char* question, char* answer_option){
    Question q;
    q.question_type = question[0];
    q.question_number = atoi(&question[1]); //this is a hack lmao
    int len = strlen(question);
    //check that the question is longer than 4 characters. 
    if (len < 4){
        printf("Error: Question is too short. Exiting.\n");
        exit(1);
    }
    q.question = malloc(len - 3);
    strncpy(q.question, &question[4], len - 4); //we just want the question content. 
    q.question[len - 4] = '\0'; //null terminate the string.
    q.is_reverse = 0; //default to false.
    if (answer_option[0] == 'R'){
        q.is_reverse = 1;
    }
    return q;
}

Response getNextResponse() {
    Response r = {0};  // zero-initialize all fields
    char line[MAX_LINE_LENGTH];
    char *token;

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#') continue;  // skip comment lines
        break;
    }

    if (line[0] == '\0' || feof(stdin)) {
        return r;  // return the "empty" response if no more input
    }

    // major
    token = strtok(line, ",\n");
    if (token) {
        r.major = malloc(strlen(token) + 1);
        strncpy(r.major, token, strlen(token));
        r.major[strlen(token)] = '\0';  // ensure null-termination
    }

    // yes/no
    token = strtok(NULL, ",\n");
    if (token) r.yes_no = (strcmp(token, "yes") == 0) ? 1 : 0;

    // date of birth
    token = strtok(NULL, ",\n");
    if (token) {
        sscanf(token, "%d-%d-%d", &r.dob_year, &r.dob_month, &r.dob_day);
    }

    // answers
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        token = strtok(NULL, ",\n");
        if (!token) break;
        r.answer[i] = malloc(strlen(token) + 1);
        strncpy(r.answer[i], token, strlen(token));
        r.answer[i][strlen(token)] = '\0';  // ensure null-termination
    }

    return r;
}

int scoreResponse(){
    
    
    return 0;
}

void freeStringArray(char** arr, int max_size) {
    for (int i = 0; i < max_size; i++) {
        if (arr[i] == NULL) {
            break;
        }
        free(arr[i]);
    }
}

void freeResponses(Response* responses, int response_count) {
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
}

void cleanup(char** questions, char** answer_options, char** likert_options, 
             Response* responses, int response_count) {
    freeStringArray(questions, MAX_QUESTION_AMOUNT);
    freeStringArray(answer_options, MAX_ANSWER_AMOUNT);
    freeStringArray(likert_options, MAX_LIKERT_AMOUNT);
    freeResponses(responses, response_count);
}

int main() {
    char* questions[MAX_QUESTION_AMOUNT];
    char* answer_options[MAX_ANSWER_AMOUNT];
    char* likert_options[MAX_LIKERT_AMOUNT];
    int* control_bits = getControlBits();

    getQuestions(questions); 
    getAnswerOptions(answer_options);
    getLikertOptions(likert_options);


    // Construct the questions
    Question q[MAX_QUESTION_AMOUNT];
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i] == NULL) {
            break;
        }
        q[i] = constructQuestion(questions[i], answer_options[i]);
    }

    // // print out the questions for debugging purposes.
    // for (int i = 0; i < MAX_QUESTION_AMOUNT; i++){
    //     if (q[i].question == NULL){
    //         break;
    //     }
    //     printf("Question %c%d: %s\n", q[i].question_type, q[i].question_number, q[i].question);
    //     printf("Reverse: %d\n", q[i].is_reverse);
    // }

    // Get responses (1 per line until EOF)
    Response responses[MAX_QUESTION_AMOUNT];
    int response_count = 0;
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        responses[i] = getNextResponse();
        if (responses[i].major == NULL) {
            // no more responses
            response_count = i;
            break;
        }
    }
    // // print out the responses for debugging purposes.
    // for (int i = 0; i < response_count; i++){
    //     printf("Major: %s\n", responses[i].major);
    //     printf("Yes/No: %d\n", responses[i].yes_no);
    //     printf("DOB: %d-%d-%d\n", responses[i].dob_year, responses[i].dob_month, responses[i].dob_day);
    //     for (int j = 0; j < MAX_QUESTION_AMOUNT; j++){
    //         if (responses[i].answer[j] == NULL){
    //             break; 
    //         }
    //         printf("Answer %d: %s\n", j, responses[i].answer[j]);
    //     }
    // }

    // before we exit, we MUST free the memory
    cleanup(questions, answer_options, likert_options, responses, response_count);
    
    return 0;
}