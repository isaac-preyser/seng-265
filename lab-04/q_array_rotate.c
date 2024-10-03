#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 10

//function def

void rotate(int* arr, int len, int n); 


int main(){

        int i = 0;
        char *sep = "";
        // declare and initialize an int array arr_1 of size MAX_SIZE and initialize it with random values
        // For example, declare and initialize arr_1 to {1,2,3,4,5,6,7,8,9,10}
        int arr_1[MAX_SIZE] = {1,2,3,4,5,6,7,8,9,10};

        // This for statement prints the content of arr_1 to console
        for (i = 0; i < MAX_SIZE; i++) {
            printf("%s%d", sep, arr_1[i]);
            sep = ", ";
        }
        printf("\n");

        // call rotate() with num = 1
        rotate(arr_1, MAX_SIZE, 1);

        sep = "";
        for (i = 0; i < MAX_SIZE; i++) {
            printf("%s%d", sep, arr_1[i]);
            sep = ", ";
        }
        printf("\n");
        // Outcome on console from the above for loop should be 2, 3, 4, 5, 6, 7, 8, 9, 10, 1

        // call rotate() with num = 2
        rotate(arr_1, MAX_SIZE, 2);

        sep = "";
        for (i = 0; i < MAX_SIZE; i++) {
            printf("%s%d", sep, arr_1[i]);
            sep = ", ";
        }
        printf("\n");
        // Outcome on console from the above for loop should be 4, 5, 6, 7, 8, 9, 10, 1, 2, 3

}


 /*
  * Design a function rotate(int num, .........) that take a number as a parameter (int num) and any other parameters as required
  * When called, the function will modify arr_1 by moving each of its values to an index lowered by num. If the new index becomes negative, then MAX_SIZE is added to get the correct index
  * For example, if num = 2, then a number at index 4 is moved to index 2 (4 - num) and a number at index 1 is moved to index 9(1 - num + MAX_SIZE)
  * Another example, if at the start, arr_1 is {2,4,6,8,1,5},
  * calling arr_1 with num = 2 should change arr_1 to {6,8,1,5,2,4}
  */

//making the key assumption that the user does not specify n longer than the array length.
//also assuming that arr is always statically allocated.  
void rotate(int* arr, int len, int n){
   // printf("allocating buffer space.. (n = %d)\n", n);
    int* buffer = (int*)malloc(sizeof(int) * n);
    if (buffer == NULL){
        fprintf(stderr, "broski, malloc failed.");
        exit(1);
    } else {
       // printf("success! (size = %d)\n");
    }

    //perform rotation

    //store the first 'n' elements in the buffer
    for (int i = 0; i < n; i++) {
        buffer[i] = arr[i];
    }

    //shift the remaining elements in the array to the left
    for (int i = n; i < len; i++) {
        arr[i - n] = arr[i];
    }

    //move the buffered elements to the end of the array
    for (int i = 0; i < n; i++) {
        arr[len - n + i] = buffer[i];
    }

    free(buffer);
}