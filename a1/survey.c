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
#define MAX_LIKERT_AMOUNT 6 // 6 likert options. This leaves one extra space. Code is set up to reflect this. 

typedef struct {
    char* question;
    char question_type; // C, I, G, U, or P
    int question_number;
    int is_reverse; // boolean - is the question reverse scored?
} Question;

typedef struct {
    char* major;
    int yes_no;
    int dob_year;
    int dob_month;
    int dob_day;
    char* answer[MAX_QUESTION_AMOUNT];
    int c_scores[MAX_QUESTION_AMOUNT];
    int c_index;
    int i_scores[MAX_QUESTION_AMOUNT];
    int i_index;
    int g_scores[MAX_QUESTION_AMOUNT];
    int g_index;
    int u_scores[MAX_QUESTION_AMOUNT];
    int u_index;
    int p_scores[MAX_QUESTION_AMOUNT];
    int p_index;
} Response;

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
            size_t token_len = strlen(token);
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
            arr[j] = NULL;
        }

        break;  // we only want the first non-comment line
    }
}

// Functions to get specific options
void getQuestions(char* arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getAnswerOptions(char* arr[]) {
    getOptions(arr, MAX_ANSWER_AMOUNT, ";\n");
}

void getLikertOptions(char* arr[]) {
    getOptions(arr, MAX_LIKERT_AMOUNT, ",\n");
}

Question constructQuestion(char* question, char* answer_option) {
    Question q;
    q.question_type = question[0];
    q.question_number = atoi(&question[1]); // Extract number after the type
    int len = strlen(question);

    // Check that the question is longer than 4 characters.
    if (len < 4) {
        printf("Error: Question is too short. Exiting.\n");
        exit(1);
    }

    int content_len = len - 4; // keeping only question content. e.g. skip 'C1: '
    q.question = malloc(content_len + 1); // +1 for null terminator
    if (q.question == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    strncpy(q.question, &question[4], content_len); // Skip 'C1: '
    q.question[content_len] = '\0'; // null terminate the string

    q.is_reverse = (answer_option[0] == 'R') ? 1 : 0;
    return q;
}

// Parsing functions
void parseMajor(char* token, Response* r) {
    if (token) {
        r->major = malloc(strlen(token) + 1);
        if (r->major == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
        strcpy(r->major, token);
    } else {
        r->major = NULL;
    }
}

void parseYesNo(char* token, Response* r) {
    if (token) {
        r->yes_no = (strcmp(token, "yes") == 0) ? 1 : 0;
    } else {
        r->yes_no = 0; // default value
    }
}

void parseDateOfBirth(char* token, Response* r) {
    if (token) {
        sscanf(token, "%d-%d-%d", &r->dob_year, &r->dob_month, &r->dob_day);
    } else {
        r->dob_year = r->dob_month = r->dob_day = 0;
    }
}

void parseAnswers(Response* r) {
    int i = 0;
    char* token = strtok(NULL, ",\n");
    while (token != NULL && i < MAX_QUESTION_AMOUNT) {
        r->answer[i] = malloc(strlen(token) + 1);
        if (r->answer[i] == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
        strcpy(r->answer[i], token);
        token = strtok(NULL, ",\n");
        i++;
    }
    // Nullify the rest of the answers
    for (int j = i; j < MAX_QUESTION_AMOUNT; j++) {
        r->answer[j] = NULL;
    }
}

Response getNextResponse() {
    Response r = {0};  // zero-initialize all fields
    char line[MAX_LINE_LENGTH];
    char* token;

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        if (line[0] == '#' || line[0] == '\n') continue;  // skip comments and empty lines
        break;
    }

    if (line[0] == '\0' || feof(stdin)) {
        return r;  // return the "empty" response if no more input
    }

    // major
    token = strtok(line, ",\n");
    parseMajor(token, &r);

    // yes/no
    token = strtok(NULL, ",\n");
    parseYesNo(token, &r);

    // date of birth
    token = strtok(NULL, ",\n");
    parseDateOfBirth(token, &r);

    // answers
    parseAnswers(&r);

    return r;
}

// Helper function for reverse scoring
int reverseScore(const char* answer, char* likert_options[]) {
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (strcmp(answer, likert_options[i]) == 0) {
            return MAX_LIKERT_AMOUNT - 1 - i; // return 5 - index of the likert option, e.g. 5 for "fully disagree", as it appears first. shifted by 1 to account for 0 indexing. (this should change since we have 6 options and therefore max_likert_amount **should** be 5)
        }
    }
    printf("Error: Invalid answer. Expected a valid Likert option, but received \"%s\"\n", answer);
    return -1;  // Error state
}

// Helper function for forward scoring
int forwardScore(const char* answer, char* likert_options[]) {
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (strcmp(answer, likert_options[i]) == 0) {
            return i; // return the index of the likert option, e.g. 0 for "fully disagree", as it appears first. 
        }
    }
    printf("Error: Invalid answer. Expected a valid Likert option, but received \"%s\"\n", answer);
    return -1;  // Error state
}

// Function to score based on the question type and reverse flag
void scoreByType(int* scores, int* index, const char* answer, Question q, char* likert_options[]) {
    int score;
    if (q.is_reverse) {
        score = reverseScore(answer, likert_options);
    } else {
        score = forwardScore(answer, likert_options);
    }

    // Check that score is valid
    if (score >= 0) {
        scores[(*index)++] = score;
    } else {
        // Error case, do not increment index or add score
        printf("Error scoring question '%c%d': Invalid score for answer '%s'\n", q.question_type, q.question_number, answer);
    }
}

void scoreResponses(Response* r, Question q[], char* likert_options[]) {
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (r->answer[i] == NULL) {
            break;
        }

        switch (q[i].question_type) {
            case 'C':
                scoreByType(r->c_scores, &r->c_index, r->answer[i], q[i], likert_options);
                break;
            case 'I':
                scoreByType(r->i_scores, &r->i_index, r->answer[i], q[i], likert_options);
                break;
            case 'G':
                scoreByType(r->g_scores, &r->g_index, r->answer[i], q[i], likert_options);
                break;
            case 'U':
                scoreByType(r->u_scores, &r->u_index, r->answer[i], q[i], likert_options);
                break;
            case 'P':
                scoreByType(r->p_scores, &r->p_index, r->answer[i], q[i], likert_options);
                break;
            default:
                printf("Error: Invalid question type '%c' for question number %d. Exiting.\n", q[i].question_type, q[i].question_number);
                exit(1);
        }
    }
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

float* calcPercents(Response responses[], Question q, int response_count, char* likert_options[]) {
    float* percentages = malloc(MAX_LIKERT_AMOUNT * sizeof(float));
    int likert_counts[MAX_LIKERT_AMOUNT] = {0}; //stores the amount of times a given likert option was selected. In this case, 0 will always be fully disagree, and 4 will always be fully agree.
    if (percentages == NULL) {
        fprintf(stderr, "Memory allocation failed (calcPercents)\n");
        exit(1);
    } 

    // Initialize all percentages to 0
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        percentages[i] = 0;
    }
    // reverse lookup for each respondents' answer to question q. 
    for (int i = 0; i < response_count; i++){
        if(responses[i].major == NULL){
            break; // no more responses. 
        }
        if (q.is_reverse){
            //if we have reverse scoring, 5 corresponds with fully disagree, 0 corresponds with fully agree.
            switch(q.question_type){
            case 'C':
                likert_counts[5 - responses[i].c_scores[q.question_number - 1]]++;
                break;
            case 'I':
                likert_counts[5 - responses[i].i_scores[q.question_number - 1]]++;
                break;
            case 'G':
                likert_counts[5 - responses[i].g_scores[q.question_number - 1]]++;
                break;
            case 'U':
                likert_counts[5 - responses[i].u_scores[q.question_number - 1]]++;
                break;
            case 'P':
                likert_counts[5 - responses[i].p_scores[q.question_number - 1]]++;
                break;
            default:
                printf("Error: Invalid question type '%c' for question number %d. Exiting.\n", q.question_type, q.question_number);
                exit(1);
            }
        } else{
            switch(q.question_type){
            case 'C':
                likert_counts[responses[i].c_scores[q.question_number - 1]]++;
                break; 
            case 'I':
                likert_counts[responses[i].i_scores[q.question_number - 1]]++;
                break;
            case 'G':
                likert_counts[responses[i].g_scores[q.question_number - 1]]++;
                break;
            case 'U':
                likert_counts[responses[i].u_scores[q.question_number - 1]]++;
                break;
            case 'P':
                likert_counts[responses[i].p_scores[q.question_number - 1]]++;
                break;
            default:
                printf("Error: Invalid question type '%c' for question number %d. Exiting.\n", q.question_type, q.question_number);
                exit(1);
            
        }
        }
    }
    //now we should have a count of how many times each likert option was selected. 
    int total_responses = 0; 
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++){
        total_responses += likert_counts[i];
    }

    //now we can calculate the percentages.
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++){
        percentages[i] = (float)likert_counts[i] / total_responses * 100;
    }

    //remember to free percentages after using it.
    

    return percentages;
}

void outputPercentiles(Question questions[], Response responses[], int response_count, char* likert_options[]) {
    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\n");
    printf("SURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %d\n\n", response_count);
    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n\n");

    // Loop through each question, and output the relative percentual frequencies for each level of agreement. 
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i].question == NULL) {
            break;
        }
        float* percents = calcPercents(responses, questions[i], response_count, likert_options);
        printf("%c%d: %s\n", questions[i].question_type, questions[i].question_number, questions[i].question);
        for (int j = 0; j < MAX_LIKERT_AMOUNT; j++) {
            printf("%.2f: %s\n", percents[j], likert_options[j] );
        }
        printf("\n");
        free(percents); // Free the allocated memory for percents (we don't need it anymore)
    }

    
 

}

void cleanup(char** questions, char** answer_options, char** likert_options, Response* responses, int response_count) {
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

    // Score responses
    for (int i = 0; i < response_count; i++) {
        if (responses[i].major == NULL) {
            break;
        }
        // Score the response
        scoreResponses(&responses[i], q, likert_options);
    }
    outputPercentiles(q, responses, response_count, likert_options);

    
    // Free allocated memory before exiting
    cleanup(questions, answer_options, likert_options, responses, response_count);
    //need to add percents to cleanup function. 
    return 0;
}
