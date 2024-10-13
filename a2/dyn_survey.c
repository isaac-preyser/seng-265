#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "input_handling.h"

#define MAX_LINE_LENGTH 3000
#define MAX_QUESTION_AMOUNT 200
#define MAX_RESPONSE_AMOUNT 50
#define MAX_LIKERT_AMOUNT 6 // 6 likert options. 
#define MAX_CATEGORY_AMOUNT 5 // 5 categories- C, I, G, U, P.
#define MAX_FILTER_AMOUNT 10 //max of 10 filters permitted. 

//a2 TODOS: 
// convert all static arrays to dynamic arrays using realloc(). - do this last, as it doesn't seem to be necessary to make all tests pass. 
// figure out some way to keep track of how many times we have expanded our array. 


// convert Responses[] array to a Response* [] array (to be more flexible with how memory is allocated.) - DONE
// write a function to parse filtering terms, and perform control logic in the output. 
//  



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
    //perhaps include a function pointer to a scoring function in here. (just to see what happens.. lol) 
} Answer;

typedef struct {
    char* major;
    int yes_no; // 0 or 1 (boolean)
    int dob[3]; // [0] = year, [1] = month, [2] = day.
    Answer* answers[MAX_QUESTION_AMOUNT]; 
} Response; 

typedef struct {
    char* major;
    int yes_no; // 0 or 1 (boolean)
    int age[2]; //age[0] = min age, age[1] = max age.
    int type; //0 = major, 1 = yes_no, 2 = age.
} Filter; 

//plan: 
//NOTE: everything comes piped in from stdin and all output is piped to stdout.
//1. Read control bits, and store them in int control_bits[3]. (found on line 0)
//2. Read the questions, and create a bank of questions. line 1 contains the questsions, and line 2 will have the question properties (direct or reverse). 
//3. read the likert terms, and store them in a string array. 
//4. read responses (one per line), and store them in an array of responses. 
//5. process data and present results.

int* getControlBits() {
    static int control_bits[2] = {0};  // initialize to zero. this also assumes that there will only ever be 4 control bits.
    char line[MAX_LINE_LENGTH];

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        // skip comment lines
        if (line[0] == '#') {
            continue;
        }

        // try to parse 4 integers from the line
        int parsed = sscanf(line, "%d,%d,%d",
                            &control_bits[0], &control_bits[1],
                            &control_bits[2]);

        // if we parsed at least one integer, we're done
        if (parsed > 0) {
            break;
        }
        // if we couldn't parse any integers, continue to the next line

	//the above should probably be more specific, but I guess it's ok. 
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

Answer* constructAnswer(char* answer, Question* corresponding_question) {
    Answer* a = (Answer *)malloc(sizeof(Answer));
    if (a == NULL) {
        fprintf(stderr, "Memory allocation failed (Answer* constructAnswer, allocating space for new Answer a)\n");
        exit(1);
    }

    a->answer_content = (char *)malloc(strlen(answer) + 1);
    if (a->answer_content == NULL) {
        fprintf(stderr, "Memory allocation failed (Answer* constructAnswer, allocating space for answer_content.)\n");
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

int getFilteredResponses(Response* responses[], int response_count, Response* filtered_responses[], Filter** filters, int filter_count) {
    //PLAN: 
    //for each response, check if it passes all filters.
    //if it does, add it to the filtered_responses array.
    //return the number of filtered responses.
    int filtered_count = 0;
    for (int i = 0; i < response_count; i++) {
        int passed_all_filters = 1;
        for (int j = 0; j < filter_count; j++) {
            switch(filters[j]->type){
                case 0:
                    //major filter
                    if (strcmp(responses[i]->major, filters[j]->major) != 0) {
                        passed_all_filters = 0;
                    }
                    break;
                case 1:
                    //yes_no filter
                    if (responses[i]->yes_no != filters[j]->yes_no) {
                        passed_all_filters = 0;
                    }
                    break;
                case 2:
                    //age filter
                    //first, calculate the respondent's age. 

                    // hard-coded current date (probably not the best way to do this, but it's fine for now)
                    int current_year = 2024;
                    int current_month = 10;
                    int current_day = 12;

                    int age = current_year - responses[i]->dob[0];

                    if (current_month < responses[i]->dob[1] || (current_month == responses[i]->dob[1] && current_day < responses[i]->dob[2])) {
                        age--;
                    }

                    //check if the age is within the filter's range.
                    if (age < filters[j]->age[0] || age > filters[j]->age[1]) {
                        passed_all_filters = 0;
                    }

                    break;
                default:
                    fprintf(stderr, "Invalid filter type. Exiting.\n");
                    exit(1);
            }
        }
        if (passed_all_filters) {
            filtered_responses[filtered_count] = responses[i];
            filtered_count++;
        }
    }
    return filtered_count;
}
    




// parsing functions
void parseMajor(char* token, Response* r) {
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
    // nullify the rest of the answers
    for (int j = i; j < MAX_QUESTION_AMOUNT; j++) {
        r->answers[j] = NULL;
    }
}


Response* getNextResponse(Question* question_bank[]) {
    Response* r = NULL;  // zero-initialize all fields
    r = (Response *)malloc(sizeof(Response));
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


//calculation and output functions

//maybe use a helper function to calculate the scores for each response.
//RECALL: "fully disagree" = likert[0], "fully agree" = likert[5].
//FROM THE ASSIGNMENT SHEET: The score for a question is the index of the answer in the likert scale, plus 1. 

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



void calculateScores(Response* responses[], int response_count, char* likert_options[]) {
    for (int i = 0; i < response_count; i++) {
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++) {
            if (responses[i]->answers[j] == NULL) {
                break;
            }
            if (responses[i]->answers[j]->corresponding_question->is_reverse) {
                //use reverse scoring. 
                responses[i]->answers[j]->score = reverseScore(responses[i]->answers[j]->answer_content, likert_options);
                
            } else {
                //use direct scoring.
                responses[i]->answers[j]->score = directScore(responses[i]->answers[j]->answer_content, likert_options);
            }
        }
    }
}

//this function returns an array of floats (as large as MAX_LIKERT_AMOUNT).
//this output array will contain a series of floats corresponding to the percentage of answers
//corresponding to eac question. 

//e.g., given a question q (and 6 potential responses), returns:[ 10.00, 0.00, 15.00, 25.00, 0.00
// , 50.00]

float* calcPercentage(Response* responses[], int response_count, Question q) {
    float* percentages = (float *)malloc(sizeof(float) * MAX_LIKERT_AMOUNT); 
    if (percentages == NULL) {
        fprintf(stderr, "allocating space for *percentages in float calcPercentage");
        exit(1); 
    }
    int counts[MAX_LIKERT_AMOUNT] = {0}; // initialize to zero
    //search for the question in each of the responses, and increment the count for the corresponding likert option.
    for (int i = 0; i < response_count; i++) {
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++) {
            if (responses[i]->answers[j] == NULL) {
                break;
            }
            //check if the answer corresponds with the target question number and type. 
            if (responses[i]->answers[j]->corresponding_question->question_number == q.question_number && responses[i]->answers[j]->corresponding_question->question_type == q.question_type) {
                //check for reverse scoring. 
                if (q.is_reverse) {
                    counts[MAX_LIKERT_AMOUNT - responses[i]->answers[j]->score]++;
                } else {
                    counts[responses[i]->answers[j]->score - 1]++;
                }
            }
        }
    } 
    //calculate the percentages.
    for (int i = 0; i < MAX_LIKERT_AMOUNT; i++) {
        percentages[i] = (float) counts[i] / response_count * 100;
    }

    return percentages;
    //note: remember to free percentages after use.
}


void calcAverages(Response* responses[], int response_count, float output[], int output_size) {
    float averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    int counts[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    for (int i = 0; i < response_count; i++) {
        for (int j = 0; j < MAX_QUESTION_AMOUNT; j++) {
            if (responses[i]->answers[j] == NULL) {
                break; //break if we reach the end of the answers.
            }
            //increment the averages and counts.
            switch(responses[i]->answers[j]->corresponding_question->question_type) {
                case 'C':
                    averages[0] += responses[i]->answers[j]->score;
                    counts[0]++;
                    break;
                case 'I':
                    averages[1] += responses[i]->answers[j]->score;
                    counts[1]++;
                    break;
                case 'G':
                    averages[2] += responses[i]->answers[j]->score;
                    counts[2]++;
                    break;
                case 'U':
                    averages[3] += responses[i]->answers[j]->score;
                    counts[3]++;
                    break;
                case 'P':
                    averages[4] += responses[i]->answers[j]->score;
                    counts[4]++;
                    break;
            }
        }
    }
    //calculate the averages.
    for (int i = 0; i < output_size; i++) {
        output[i] = averages[i] /= counts[i];
    }
}

void calcAveragesIndividual(Response* r, float output[], int output_size) {
    float averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    int counts[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (r->answers[i] == NULL) {
            break; //break if we reach the end of the answers.
        }
        //increment the averages and counts.
        switch(r->answers[i]->corresponding_question->question_type) {
            case 'C':
                averages[0] += r->answers[i]->score;
                counts[0]++;
                break;
            case 'I':
                averages[1] += r->answers[i]->score;
                counts[1]++;
                break;
            case 'G':
                averages[2] += r->answers[i]->score;
                counts[2]++;
                break;
            case 'U':
                averages[3] += r->answers[i]->score;
                counts[3]++;
                break;
            case 'P':
                averages[4] += r->answers[i]->score;
                counts[4]++;
                break;
        }
    }
    //calculate the averages.
    for (int i = 0; i < output_size; i++) {
        output[i] = averages[i] /= counts[i];
    }
}

//output functions
void outputPercentages(Question* question_bank[], Response* responses[], int response_count, char* likert_options[]) {
    printf("\nFOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (question_bank[i] == NULL) {
            break;
        }
        printf("\n");
        float* percentages = calcPercentage(responses, response_count, *question_bank[i]);
        printf("%c%d. %s\n", question_bank[i]->question_type, question_bank[i]->question_number, question_bank[i]->question_content);
        for (int j = 0; j < MAX_LIKERT_AMOUNT; j++) {
            printf("%.2f: %s\n", percentages[j], likert_options[j]);
        }
        free(percentages);
    }
}

void outputPerRespondentAverages(Response* responses[], int response_count) {
    printf("\nSCORES FOR ALL THE RESPONDENTS\n\n");
    for (int i = 0; i < response_count; i++) {
        float averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
        calcAveragesIndividual(responses[i], averages, MAX_CATEGORY_AMOUNT);
        printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", averages[0], averages[1], averages[2], averages[3], averages[4]);
    }

}

void outputAverages(Response* responses[], int response_count) {
    printf("\nAVERAGE SCORES PER RESPONDENT\n\n");
    float averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    calcAverages(responses, response_count, averages, MAX_CATEGORY_AMOUNT);
    printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", averages[0], averages[1], averages[2], averages[3], averages[4]);
}

//cleanup functions
void freeStringArray(char** arr, int max_size) {
    if (arr == NULL) return; // check if array is NULL
    for (int i = 0; i < max_size; i++) {
        if (arr[i] != NULL) {
            free(arr[i]);
            arr[i] = NULL; // set to NULL to prevent double freeing
        }
    }
}

void freeQuestionBank(Question** question_bank, int max_size) {
    if (question_bank == NULL) return; // check if question_bank is NULL
    for (int i = 0; i < max_size; i++) {
        if (question_bank[i] != NULL) {
            free(question_bank[i]->question_content);
            free(question_bank[i]);
            question_bank[i] = NULL; // set to NULL to prevent double freeing
        }
    }
}

void freeResponse(Response* r) {
    if (r == NULL) return; // check if response is NULL
    free(r->major);
    r->major = NULL; // set to NULL to prevent double freeing
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (r->answers[i] != NULL) {
            free(r->answers[i]->answer_content);
            free(r->answers[i]);
            r->answers[i] = NULL; // set to NULL to prevent double freeing
        }
    }
}

void freeResponses(Response** responses, int response_count) {
    if (responses == NULL) return; // check if responses is NULL
    for (int i = 0; i < response_count; i++) {
        freeResponse(responses[i]);
        free(responses[i]);
        responses[i] = NULL; // set to NULL to prevent double freeing
    }
}

void freeFilters(Filter** filters) {
    if (filters == NULL) return; // check if filters is NULL
    for (int i = 0; i < MAX_FILTER_AMOUNT; i++) {
        if (filters[i] != NULL) {
            free(filters[i]->major);
            free(filters[i]);
            filters[i] = NULL; // set to NULL to prevent double freeing
        }
    }
}

int main(){
    int* control_bits = getControlBits();
    //print out control bits for debug.
    //printf("Control Bits: %d, %d, %d\n", control_bits[0], control_bits[1], control_bits[2]);
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

    //before we can get the responses, we must determine the number of responses in the survey. 


    int response_count = getResponseCount();
    //print the number of responses for debug.
    // printf("Number of responses: %d\n", response_count);

    //now we can get the responses.
    Response** responses = malloc(sizeof(Response*) * response_count);
    for (int i = 0; i < response_count; i++) {
        responses[i] = getNextResponse(question_bank);
        if (responses[i]->major == NULL) {
            response_count = i; //this might cause problems
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


    //next, filtering logic must be applied. 
    //there are three types of logic: 
    //0. Major- filter by major, including only responses with a matching major. 
    //1. Citizenship (yes/no) - include responses only with a positive yes/no answer.
    //2. Age - include responses from those within a given age range of [min, max].

    //STEPS 
    //1. read the filtering terms from stdin, which will be in string format (1 filter per line).
    //2. parse the filtering terms, and apply the logic to the responses.
    //2a. keep track of how many responses are included in the filtered array, as this will be used in the output. 
    //3. create a "filtered" array of responses, including only those that meet the filtering criteria. (if there's no criteria, add all responses to the filtered array.)
    //4. output the results by passing the filtered array to the output functions.


    Filter** filters = (Filter **)malloc(sizeof(Filter *) * MAX_FILTER_AMOUNT);
    int filter_count = getFilters(filters); //fills array, returns number of filters.
    //print out the filters for debug.
    // for (int i = 0; i < MAX_FILTER_AMOUNT; i++) {
    //     if (filters[i] == NULL) {
    //         break;
    //     }
    //     switch(filters[i]->type) {
    //         case 0:
    //             printf("Major: %s\n", filters[i]->major);
    //             break;
    //         case 1:
    //             printf("Yes/No: %s\n", filters[i]->yes_no ? "yes" : "no");
    //             break;
    //         case 2:
    //             printf("Age: %d-%d\n", filters[i]->age[0], filters[i]->age[1]);
    //             break;
    //     }
    // }

    //perform filter logic. 

    Response** filtered_responses = malloc(sizeof(Response*) * response_count);
    int filtered_responses_count = getFilteredResponses(responses, response_count, filtered_responses, filters, filter_count); //fill the filtered_responses array with the filtered responses, and return the number of responses in the filtered array.

    //output the results.
    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\n");
    printf("SURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %d\n", filtered_responses_count);

    if(control_bits[0] == 1){
       outputPercentages(question_bank, filtered_responses, filtered_responses_count, likert_options); 
    }
    if (control_bits[1] == 1) {
        outputPerRespondentAverages(filtered_responses, filtered_responses_count);
    }
    if (control_bits[2] == 1) {
        outputAverages(filtered_responses, filtered_responses_count);  
    }
    

    


    // Free allocated memory
    freeStringArray(questions, MAX_QUESTION_AMOUNT);
    freeStringArray(question_opts, MAX_QUESTION_AMOUNT);
    freeStringArray(likert_options, MAX_LIKERT_AMOUNT);
    freeQuestionBank(question_bank, question_count);
    freeResponses(responses, response_count);
    freeFilters(filters);
    free(filtered_responses); //no need to free the responses again, they should be freed already above. 
    return 0; 
}
