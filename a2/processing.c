#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "processing.h"
#include "dyn_survey.h"


//filtering function

int getFilteredResponses(Respondent* responses[], int response_count, Respondent* filtered_responses[], Filter** filters, int filter_count) {
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
    

//calculation functions

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


void calculateScores(Respondent* responses[], int response_count, char* likert_options[]) {
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
double* calcPercentage(Respondent* responses[], int response_count, Question q) {
    double* percentages = (double *)malloc(sizeof(double) * MAX_LIKERT_AMOUNT); 
    if (percentages == NULL) {
        fprintf(stderr, "allocating space for *percentages in double calcPercentage");
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
        percentages[i] = (double) counts[i] / response_count * 100;
    }

    return percentages;
    //note: remember to free percentages after use.
}


void calcAverages(Respondent* responses[], int response_count, double output[], int output_size) {
    double averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
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

void calcAveragesIndividual(Respondent* r, double output[], int output_size) {
    double averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
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
