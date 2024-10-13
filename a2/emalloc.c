#include <stdlib.h>
#include <stdio.h>
#include "emalloc.h"
#include "dyn_survey.h"


void *emalloc(size_t n) {
    void *p; 

    p = malloc(n);
    if (p == NULL) {
        fprintf(stderr, "malloc of %zu bytes failed", n); 
        exit(1);
    }   

    return p;
}

//cleanup functions: 
void freeStringArray(char** arr, int max_size) {
    if (arr == NULL) return; // check if array is NULL
    for (int i = 0; i < max_size; i++) {
        if (arr[i] != NULL) {
            free(arr[i]);
            arr[i] = NULL; // set to NULL to prevent double freeing
        }
    }
    // assuming arr is in stack memory; no need to free it.
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
    //question_bank is in stack memory; no need to free it.
}

//frees a response and all its answers within the struct. 
void freeResponse(Respondent* r) {
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
    free(r);
}

//frees all responses within an arbitrary array of responses, and the array itself.
void freeResponses(Respondent** responses, int response_count) {
    if (responses == NULL) return; // check if responses is NULL
    for (int i = 0; i < response_count; i++) {
        freeResponse(responses[i]); // frees the response and all its answers within. 
        responses[i] = NULL; // set to NULL to prevent double freeing
    }
    free(responses);
}

//frees an array of filter structs. 
void freeFilters(Filter** filters) {
    if (filters == NULL) return; // check if filters is NULL
    for (int i = 0; i < MAX_FILTER_AMOUNT; i++) {
        if (filters[i] != NULL) {
            free(filters[i]->major);
            free(filters[i]);
            filters[i] = NULL; // set to NULL to prevent double freeing
        }
    }
    free(filters);
}

//mass cleanup function that frees all allocated memory.
void cleanup(char** questions, char** question_opts, char** likert_options, Question** question_bank, int question_count, Respondent** responses, int response_count, Filter** filters, Respondent** filtered_responses) {
    //free allocated memory
    freeStringArray(questions, MAX_QUESTION_AMOUNT);
    freeStringArray(question_opts, MAX_QUESTION_AMOUNT);
    freeStringArray(likert_options, MAX_LIKERT_AMOUNT);
    freeQuestionBank(question_bank, question_count);
    freeResponses(responses, response_count);
    freeFilters(filters);
    free(filtered_responses);
}

