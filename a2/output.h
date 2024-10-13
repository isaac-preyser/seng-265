#ifndef _OUTPUT_H_
#define _OUTPUT_H_

/* add your include and prototypes here*/
#include "dyn_survey.h" //for types Response, Filter, Question, Answer


void outputPercentages(Question* question_bank[], Respondent* responses[], int response_count, char* likert_options[]);
void outputPerRespondentAverages(Respondent* responses[], int response_count);
void outputAverages(Respondent* responses[], int response_count);
void outputResults(int* control_bits, Question** question_bank, Respondent** filtered_responses, int filtered_responses_count, char** likert_options); 


#endif
