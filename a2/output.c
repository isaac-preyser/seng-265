#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dyn_survey.h" //for types Response, Filter, Question, Answer
#include "output.h" //for output functions
#include "processing.h" //for calcPercentage, calcAverages, calcAveragesIndividual


//output functions
void outputPercentages(Question* question_bank[], Respondent* responses[], int response_count, char* likert_options[]) {
    printf("\nFOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    for (int i = 0; i < MAX_QUESTION_AMOUNT; i++) {
        if (question_bank[i] == NULL) {
            break;
        }
        printf("\n");
        double* percentages = calcPercentage(responses, response_count, *question_bank[i]);
        printf("%c%d. %s\n", question_bank[i]->question_type, question_bank[i]->question_number, question_bank[i]->question_content);
        for (int j = 0; j < MAX_LIKERT_AMOUNT; j++) {
            printf("%.2f: %s\n", percentages[j], likert_options[j]);
        }
        free(percentages);
    }
}

void outputPerRespondentAverages(Respondent* responses[], int response_count) {
    printf("\nSCORES FOR ALL THE RESPONDENTS\n\n");
    for (int i = 0; i < response_count; i++) {
        double averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
        calcAveragesIndividual(responses[i], averages, MAX_CATEGORY_AMOUNT);
        printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", averages[0], averages[1], averages[2], averages[3], averages[4]);
    }

}

void outputAverages(Respondent* responses[], int response_count) {
    printf("\nAVERAGE SCORES PER RESPONDENT\n\n");
    double averages[MAX_CATEGORY_AMOUNT] = {0}; // initialize to zero
    calcAverages(responses, response_count, averages, MAX_CATEGORY_AMOUNT);
    printf("C:%.2f,I:%.2f,G:%.2f,U:%.2f,P:%.2f\n", averages[0], averages[1], averages[2], averages[3], averages[4]);
}


void outputResults(int* control_bits, Question** question_bank, Respondent** filtered_responses, int filtered_responses_count, char** likert_options) {
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
}

