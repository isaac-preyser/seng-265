#ifndef _EMALLOC_H_
#define _EMALLOC_H_

#include "dyn_survey.h" //for structs. 

void *emalloc(size_t);

void freeStringArray(char**, int);
void freeQuestionBank(Question**, int);
void freeResponse(Respondent*);
void freeResponses(Respondent**, int);
void freeFilters(Filter**);
void cleanup(char**, char**, char**, Question**, int, Respondent**, int, Filter**, Respondent**);



#endif
