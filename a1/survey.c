#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 3000
#define MAX_QUESTION_AMOUNT 200
#define MAX_RESPONSE_AMOUNT 50
#define MAX_LIKERT_AMOUNT 6 // 6 likert options. 

//I'm going to attempt this project using dynamic memory allocation.
typedef struct {
    char* question_content; 
    char question_type; // C, I, G, U, or P
    int question_number; 
    int is_reverse; // 0 or 1 (boolean)
} Question;

typedef struct {
    char* answer_content; 
    Question* corresponding_question;
    int score;  
} Answer;

typedef struct {
    char* major;
    int yes_no; // 0 or 1 (boolean)
    int dob[2]; // [0] = year, [1] = month, [2] = day.
    Answer* answers[MAX_QUESTION_AMOUNT]; 
} Response; 

//plan: 
//NOTE: everything comes piped in from stdin and all output is piped to stdout.
//1. Read test bits, and store them in int test_bits[3]. (found on line 0)
//2. Read the questions, and create a bank of questions. line 1 contains the questsions, and line 2 will have the question properties (direct or reverse). 
//3. read the likert terms, and store them in a string array. 
//4. read responses (one per line), and store them in an array of responses. 
//5. process data and present results.

int* getControlBits() {
    static int control_bits[3] = {0};  // initialize to zero
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

// functions to get specific options
void getQuestions(char* arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getQuestionOptions(char* arr[]) {
    getOptions(arr, MAX_QUESTION_AMOUNT, ";\n");
}

void getLikertOptions(char* arr[]) {
    getOptions(arr, MAX_LIKERT_AMOUNT, ",\n");
}

//constructors
Question* constructQuestion(char* question, char* answer_option) {
    Question* q = malloc(sizeof(Question));
    if (q == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    q->question_type = question[0];
    q->question_number = atoi(&question[1]); // Extract number after the type
    int len = strlen(question);

    // Check that the question is longer than 4 characters.
    if (len < 4) {
        printf("Error: Question is too short. Exiting.\n");
        exit(1);
    }

    int content_len = len - 4; // keeping only question content. e.g. skip 'C1: '
    q->question_content = malloc(content_len + 1); // +1 for null terminator
    if (q->question_content == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    strncpy(q->question_content, &question[4], content_len); // Skip 'C1: '
    q->question_content[content_len] = '\0'; // null terminate the string

    q->is_reverse = (answer_option[0] == 'R') ? 1 : 0;

    return q;
}

Answer* constructAnswer(char* answer, Question* corresponding_question) {
    Answer* a = malloc(sizeof(Answer));
    if (a == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    a->answer_content = malloc(strlen(answer) + 1);
    if (a->answer_content == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    strcpy(a->answer_content, answer);

    a->corresponding_question = corresponding_question;
    a->score = -1; // initialize to -1

    return a;
}

// parsing functions
void parseMajor(char* token, Response* r) {
    if (token) {
        size_t len = strlen(token);
        r->major = malloc(len + 1);
        if (r->major == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
        strncpy(r->major, token, len);
        r->major[len] = '\0';  // null-terminate the string
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
        sscanf(token, "%d-%d-%d", &r->dob[0], &r->dob[1], &r->dob[2]);
    } else {
        r->dob[0] = r->dob[1] = r->dob[2] = 0;
    }
}

void parseAnswers(Response* r, Question* question_bank[]) {
    int i = 0;
    char* token = strtok(NULL, ",\n");
    char* answers[MAX_QUESTION_AMOUNT];
    while (token != NULL && i < MAX_QUESTION_AMOUNT) {
        answers[i] = token;
        r->answers[i] = constructAnswer(answers[i], question_bank[i]);
        token = strtok(NULL, ",\n");
        i++;
    }
    // Nullify the rest of the answers
    for (int j = i; j < MAX_QUESTION_AMOUNT; j++) {
        r->answers[j] = NULL;
    }
}

Response getNextResponse(Question* question_bank[]) {
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
    parseAnswers(&r, question_bank);

    return r;
}

//calculation and output functions

//maybe use a helper function to calculate the scores for each response.
//RECALL: "fully disagree" = likert[0], "fully agree" = likert[5].
//FROM THE SPEC: The score for a question is the index of the answer in the likert scale, plus 1. 

//direct
int directScore(char* answer, char* likert_options[]) {
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (strcmp(answer, likert_options[i]) == 0) {
            return i + 1;
        }
    }
    return -1; // error case
}

//reverse
int reverseScore(char* answer, char* likert_options[]) {
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        if (strcmp(answer, likert_options[i]) == 0) {
            return MAX_LIKERT_AMOUNT - i;
        }
    }
    return -1; // error case
}



void calculateScores(Response* responses, int response_count, char* likert_options[]) {
    for (int i = 0; i < response_count; i++) {
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++) {
            if (responses[i].answers[j] == NULL) {
                break;
            }
            if (responses[i].answers[j]->corresponding_question->is_reverse) {
                //use reverse scoring. 
                responses[i].answers[j]->score = reverseScore(responses[i].answers[j]->answer_content, likert_options);
                
            } else {
                //use direct scoring.
                responses[i].answers[j]->score = directScore(responses[i].answers[j]->answer_content, likert_options);
            }
        }
    }
}


//cleanup functions
void freeStringArray(char** arr, int max_size) {
    if (arr == NULL) return; // Check if array is NULL
    for (int i = 0; i < max_size; i++) {
        if (arr[i] != NULL) {
            free(arr[i]);
            arr[i] = NULL; // Set to NULL to prevent double freeing
        }
    }
}

void freeQuestionBank(Question** question_bank, int max_size) {
    if (question_bank == NULL) return; // Check if question_bank is NULL
    for (int i = 0; i < max_size; i++) {
        if (question_bank[i] != NULL) {
            free(question_bank[i]->question_content);
            free(question_bank[i]);
            question_bank[i] = NULL; // Set to NULL to prevent double freeing
        }
    }
}

void freeResponse(Response* r) {
    if (r == NULL) return; // Check if response is NULL
    free(r->major);
    r->major = NULL; // Set to NULL to prevent double freeing
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (r->answers[i] != NULL) {
            free(r->answers[i]->answer_content);
            free(r->answers[i]);
            r->answers[i] = NULL; // Set to NULL to prevent double freeing
        }
    }
}

int main(){
    int* control_bits = getControlBits();
    char* questions[MAX_QUESTION_AMOUNT];
    char* question_opts[MAX_QUESTION_AMOUNT]; 
    char* likert_options[MAX_LIKERT_AMOUNT];
    
    getQuestions(questions);
    getQuestionOptions(question_opts);
    getLikertOptions(likert_options);

    // //print out likert options for debug.
    // for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
    //     printf("Likert Option %d: %s\n", i, likert_options[i]);
    // }

    //now we can make + populate the questions array. 
    Question* question_bank[MAX_QUESTION_AMOUNT];
    int question_count = 0;
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (questions[i] == NULL) {
            question_count = i;
            break;
        }
        question_bank[i] = constructQuestion(questions[i], question_opts[i]);
    }

    //print out the question bank for debug. 
    // for (int i = 0; i < question_count; i++) {
    //     printf("Question %c%d: %s\n", question_bank[i]->question_type, question_bank[i]->question_number, question_bank[i]->question_content);
    //     if (question_bank[i]->is_reverse) {
    //         printf("\tReverse\n");
    //     } else {
    //         printf("\tDirect\n");
    //     }
    // }

    //now we can get the responses.
    Response responses[MAX_RESPONSE_AMOUNT];
    int response_count = 0;
    for (int i = 0; i < MAX_RESPONSE_AMOUNT; i++) {
        responses[i] = getNextResponse(question_bank);
        if (responses[i].major == NULL) {
            response_count = i;
            break;
        }
    }
    calculateScores(responses, response_count, likert_options);
    // print out the responses for debug.
    // for (int i = 0; i < response_count; i++) {
    //     printf("Response %d:\n", i + 1);
    //     printf("\tMajor: %s\n", responses[i].major);
    //     printf("\tYes/No: %s\n", responses[i].yes_no ? "yes" : "no");
    //     printf("\tDate of Birth: %d-%d-%d\n", responses[i].dob[0], responses[i].dob[1], responses[i].dob[2]);
    //     for (int j = 0; j < question_count; j++) {
    //         printf("\tAnswer for %c%d: %s \n\t\tScore: %d", responses[i].answers[j]->corresponding_question->question_type, responses[i].answers[j]->corresponding_question->question_number, responses[i].answers[j]->answer_content, responses[i].answers[j]->score);
    //         if (responses[i].answers[j]->corresponding_question->is_reverse) {
    //             printf("\t(Reverse)\n");
    //         } else {
    //             printf("\t(Direct)\n");
    //         }
    //     }
    // }


    //next we can process the data and present the results.


    


    // Free allocated memory
    freeStringArray(questions, MAX_QUESTION_AMOUNT);
    freeStringArray(question_opts, MAX_QUESTION_AMOUNT);
    freeStringArray(likert_options, MAX_LIKERT_AMOUNT);
    freeQuestionBank(question_bank, question_count);
    for (int i = 0; i < response_count; i++) {
        freeResponse(&responses[i]); // &responses[i] is valid as long as responses[i] is not NULL
    }
    return 0; 
}