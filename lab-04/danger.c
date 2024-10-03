#include <stdio.h>

#define MAX_NUMS  5

void rogue(int *numbers, int num)
{
    int i;

    for (i = -2; i <= num; i++) {
        numbers[i] = 111 * i + 11; //dear god why are we attempting to access arr[-2 and -1]
    }
}


int main() {
    int innocent = 123;
    int nums[MAX_NUMS] = {1, 2, 3, 4, 5};
    int really_innocent = 456;
    int i;

    printf("%d %d\n", innocent, really_innocent);
    for (i = 0; i < MAX_NUMS; i++) {
        printf("%d: %d\n", i, nums[i]);
    }
    //program seg faults here. can't complete this portion of the lab w/o editing this function to 
    //**not** illegally access memory. 
    rogue(nums, MAX_NUMS); //I hate this function with a burning passion inside of my chest

    printf("----------------\n");
    printf("%d %d\n", innocent, really_innocent);
    for (i = 0; i < MAX_NUMS; i++) {
        printf("%d: %d\n", i, nums[i]);
    }
}
