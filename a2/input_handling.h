#ifndef _INPUT_HANDLING_H_
#define _INPUT_HANDLING_H_

/* add your include and prototypes here*/
#include "dyn_survey.h"

Question* constructQuestion(char* question, char* answer_option);
Response* constructAnswer(char* answer, Question* corresponding_question);
Filter* constructFilter(char* line);




int* getControlBits();

void getOptions(char* arr[], int max_size, const char* delimiters);
void getQuestions(char* arr[]);
void getQuestionOptions(char* arr[]);
void getLikertOptions(char* arr[]);

int getResponseCount();

int getFilters(Filter** filters);

void parseMajor(char* token, Respondent* r);
void parseYesNo(char* token, Respondent* r);
void parseDateOfBirth(char* token, Respondent* r);
void parseAnswers(Respondent* r, Question* question_bank[]);
Respondent* getNextResponse(Question* question_bank[]);


#endif
