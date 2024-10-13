#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "input_handling.h"
#include "dyn_survey.h"



//constructors
Question* constructQuestion(char* question, char* answer_option) {
    Question* q = (Question *)malloc(sizeof(Question));
    if (q == NULL) {
        fprintf(stderr, "Memory allocation failed (allocating space for a new Question q in Question* constructQuestion)\n");
        exit(1);
    }

    q->question_type = question[0];
    q->question_number = atoi(&question[1]); // extract number after the type
    int len = strlen(question);

    // check that the question is longer than 4 characters.
    // otherwise, the code below would break the string we are wokring on and do funky stuff (that I don't want)
    if (len < 4) {
        printf("Error: Question is too short. Exiting.\n");
        exit(1);
    }




    int content_len = len - 4; // keeping only question content. e.g. skip 'C1: '
    //if the question number is greater than 9, we need to adjust the content length.
    if (q->question_number > 9) {
        content_len--;
    }

    q->question_content = (char *)malloc(content_len + 1); // +1 for null terminator
    if (q->question_content == NULL) {
        fprintf(stderr, "Memory allocation failed (allocating space for question_content in Question* constructQuestion)\n");
        exit(1);
    }
    //if the question number is greater than 9, we need to skip an extra character.
    if (q->question_number > 9) {
        strncpy(q->question_content, &question[5], content_len); // skip 'C10: '
    } else {
        strncpy(q->question_content, &question[4], content_len); // skip 'C1: '
    }
    q->question_content[content_len] = '\0'; // null terminate the string

    q->is_reverse = (answer_option[0] == 'R') ? 1 : 0;

    return q;
}

Response* constructAnswer(char* answer, Question* corresponding_question) {
    Response* a = (Response *)malloc(sizeof(Response));
    if (a == NULL) {
        fprintf(stderr, "Memory allocation failed (Response* constructAnswer, allocating space for new Response a)\n");
        exit(1);
    }

    a->answer_content = (char *)malloc(strlen(answer) + 1);
    if (a->answer_content == NULL) {
        fprintf(stderr, "Memory allocation failed (Response* constructAnswer, allocating space for answer_content.)\n");
        exit(1);
    }
    strcpy(a->answer_content, answer);

    a->corresponding_question = corresponding_question;
    a->score = -1; // initialize to -1

    return a;
}

//filtering functions
Filter* constructFilter(char* line) {
    Filter* f = (Filter *)malloc(sizeof(Filter));
    if (f == NULL) {
        fprintf(stderr, "Memory allocation failed (Filter* constructFilter, allocating space for new Filter f)\n");
        exit(1);
    }

    char* token = strtok(line, ",\n");
    //first token is the type of filter.
    f->type = atoi(token);

    switch(f->type){
        case 0:
            //major filter
            token = strtok(NULL, ",\n");
            f->major = (char *)malloc(strlen(token) + 1);
            if (f->major == NULL) {
                fprintf(stderr, "Memory allocation failed (Filter* constructFilter, allocating space for f->major)\n");
                exit(1);
            }
            strcpy(f->major, token);
            break;
        case 1:
            //yes_no filter
            token = strtok(NULL, ",\n");
            f->yes_no = (strcmp(token, "yes") == 0) ? 1 : 0;
            break;
        case 2:
            //age filter
            token = strtok(NULL, ",\n");
            f->age[0] = atoi(token);
            token = strtok(NULL, ",\n");
            f->age[1] = atoi(token);
            break;
        default:
            fprintf(stderr, "Invalid filter type. Exiting.\n");
            exit(1);
    }

    return f;
}

//parsing functions below: 

// Read control bits from stdin and return them as an array of 3 integers
int* getControlBits() {
    int* control_bits = (int*)malloc(3 * sizeof(int));  // allocate memory for control_bits array
    if (control_bits == NULL) {
        fprintf(stderr, "Memory allocation failed (allocating space for control_bits in getControlBits)\n");
        exit(1);
    }

    char line[MAX_LINE_LENGTH];

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        // skip comment lines
        if (line[0] == '#') {
            continue;
        }

        // try to parse 3 integers from the line
        int parsed = sscanf(line, "%d,%d,%d",
                            &control_bits[0], &control_bits[1],
                            &control_bits[2]);

        // if we parsed at least one integer, we're done
        if (parsed > 0) {
            break;
        }
        // if we couldn't parse any integers, continue to the next line
    }

    return control_bits;
}

//general function to grab options from a string, seperated by specified delimiters. 
//accepts an array of max_size length and fills it with options until either no more options, or array is full. 
void getOptions(char* arr[], int max_size, const char* delimiters) {
    char line[MAX_LINE_LENGTH];
    char* token;

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#') {
            continue;
        }

        int i = 0;
        token = strtok(line, delimiters);
        while (token != NULL && i < max_size) {
            size_t token_len = strlen(token); //should I cast this to an int?
            arr[i] = (char *)malloc(token_len + 1);
            if (arr[i] == NULL) {
                fprintf(stderr, "Memory allocation failed (allocating space for arr[i] in void getOptions)\n");
                exit(1);
            }
            strncpy(arr[i], token, token_len);
            arr[i][token_len] = '\0';  // ensure null-termination
            token = strtok(NULL, delimiters);
            i++;
        }

        // null-terminate the rest of the array
        for (int j = i; j < max_size; j++) {
            arr[j] = NULL;
        }

        break;  // we only want the first non-comment line
    }
}


int getResponseCount(){
    char line[MAX_LINE_LENGTH];
    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#') {
            continue;
        }
        int response_count = atoi(line);
        return response_count;
    }
    return -1; //if we reach this point, something went wrong.
}

// function calls to getOptions to get specific options
void getQuestions(char* arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getQuestionOptions(char* arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getLikertOptions(char* arr[]) {
    getOptions(arr, MAX_LIKERT_AMOUNT, ",\n");
}

int getFilters(Filter** filters) {
    if (filters == NULL) {
        fprintf(stderr, "Memory allocation failed (Filter** getFilters, allocating space for filters)\n");
        exit(1);
    }

    char line[MAX_LINE_LENGTH];
    int i = 0;
    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#') {
            continue;
        }

        filters[i] = constructFilter(line);
        i++;
    }

    // null-terminate the rest of the array
    for (int j = i; j < MAX_FILTER_AMOUNT; j++) {
        filters[j] = NULL;
    }

    return i;
}


// parsing functions
void parseMajor(char* token, Respondent* r) {
    if (token) {
        size_t len = strlen(token);
        r->major = (char *)malloc(len + 1);
        if (r->major == NULL) {
            fprintf(stderr, "Memory allocation failed (void parseMajor)\n");
            exit(1);
        }
        strncpy(r->major, token, len);
        r->major[len] = '\0';  // null-terminate the string
    } else {
        r->major = NULL;
    }
}

void parseYesNo(char* token, Respondent* r) {
    if (token) {
        r->yes_no = (strcmp(token, "yes") == 0) ? 1 : 0;
    } else {
        r->yes_no = 0; // default value
    }
}

void parseDateOfBirth(char* token, Respondent* r) {
    if (token) {
        sscanf(token, "%d-%d-%d", &r->dob[0], &r->dob[1], &r->dob[2]);
    } else {
        r->dob[0] = r->dob[1] = r->dob[2] = 0;
    }
}

void parseAnswers(Respondent* r, Question* question_bank[]) {
    int i = 0;
    char* token = strtok(NULL, ",\n");
    char* answers[MAX_QUESTION_AMOUNT];
    while (token != NULL && i < MAX_QUESTION_AMOUNT) {
        answers[i] = token;
        r->answers[i] = constructAnswer(answers[i], question_bank[i]);
        token = strtok(NULL, ",\n");
        i++;
    }
    // nullify the rest of the answers
    for (int j = i; j < MAX_QUESTION_AMOUNT; j++) {
        r->answers[j] = NULL;
    }
}


Respondent* getNextResponse(Question* question_bank[]) {
    Respondent* r = NULL;  // zero-initialize all fields
    r = (Respondent *)malloc(sizeof(Respondent));
    char line[MAX_LINE_LENGTH];
    char* token;

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#' || line[0] == '\n') continue;  // skip comments and empty lines
        break;
    }

    if (line[0] == '\0' || feof(stdin)) {
        return r;  // return the "empty" response if no more input
    }

    token = strtok(line, ",\n");
    parseMajor(token, r);

    token = strtok(NULL, ",\n");
    parseYesNo(token, r);

    token = strtok(NULL, ",\n");
    parseDateOfBirth(token, r);

    parseAnswers(r, question_bank);

    return r;
}





