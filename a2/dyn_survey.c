#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "input_handling.h" //contains all the functions for reading in data.
#include "dyn_survey.h" //contains all the structs.
#include "output.h" 
#include "processing.h" 
#include "emalloc.h" //for cleanup functions (wrote this before emalloc dropped)


//plan: 
//NOTE: everything comes piped in from stdin and all output is piped to stdout.
//1. Read control bits, and store them in int control_bits[3]. (found on line 0)
//2. Read the questions, and create a bank of questions. line 1 contains the questsions, and line 2 will have the question properties (direct or reverse). 
//3. read the likert terms, and store them in a string array. 
//4. read responses (one per line), and store them in an array of responses. 
//5. process data and present results.
//6. free all memory.


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
    Respondent** responses = malloc(sizeof(Respondent*) * response_count);
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
    //     printf("Respondent %d:\n", i + 1);
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

    Respondent** filtered_responses = malloc(sizeof(Respondent*) * response_count);
    int filtered_responses_count = getFilteredResponses(responses, response_count, filtered_responses, filters, filter_count); //fill the filtered_responses array with the filtered responses, and return the number of responses in the filtered array.


    outputResults(control_bits, question_bank, filtered_responses, filtered_responses_count, likert_options);

    


    //cleanup
    cleanup(questions, question_opts, likert_options, question_bank, question_count, responses, response_count, filters, filtered_responses);

    return 0; 
}
