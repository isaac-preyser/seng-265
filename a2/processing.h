#ifndef _PROCESSING_H_
#define _PROCESSING_H_

/* add your include and prototypes here*/
#include "dyn_survey.h" //for types Response, Filter, Question, Answer

int getFilteredResponses(Respondent* responses[], int response_count, Respondent* filtered_responses[], Filter** filters, int filter_count);

int directScore(char* answer, char* likert_options[]);
int reverseScore(char* answer, char* likert_options[]);

void calculateScores(Respondent* responses[], int response_count, char* likert_options[]);
double* calcPercentage(Respondent* responses[], int response_count, Question q);

void calcAverages(Respondent* responses[], int response_count, double output[], int output_size);
void calcAveragesIndividual(Respondent* r, double output[], int output_size);

#endif
