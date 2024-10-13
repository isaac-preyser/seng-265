#ifndef _DYN_SURVEY_H_
#define _DYN_SURVEY_H_

/* add your library includes, constants and typedefs here*/

//define some constants.
#define MAX_LINE_LENGTH 3000
#define MAX_QUESTION_AMOUNT 200
#define MAX_RESPONSE_AMOUNT 50
#define MAX_LIKERT_AMOUNT 6 // 6 likert options. 
#define MAX_CATEGORY_AMOUNT 5 // 5 categories- C, I, G, U, P.
#define MAX_FILTER_AMOUNT 10 //max of 10 filters permitted. 

//a2 TODOS: 
// convert all static arrays to dynamic arrays using realloc(). - do this last, as it doesn't seem to be necessary to make all tests pass. 
// figure out some way to keep track of how many times we have expanded our array. 


// convert Responses[] array to a Respondent* [] array (to be more flexible with how memory is allocated.) - DONE
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
} Response;

typedef struct {
    char* major;
    int yes_no; // 0 or 1 (boolean)
    int dob[3]; // [0] = year, [1] = month, [2] = day.
    Response* answers[MAX_QUESTION_AMOUNT]; 
} Respondent; //having types response and respondent is a terrible idea, THEY WILL GET CONFUSED.
//consider (as I wrote initially) changing the name of the Response struct to Answer.

typedef struct {
    char* major;
    int yes_no; // 0 or 1 (boolean)
    int age[2]; //age[0] = min age, age[1] = max age.
    int type; //0 = major, 1 = yes_no, 2 = age.
} Filter; 


#endif
