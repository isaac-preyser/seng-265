#include <stdio.h>

int main()
{
    int a;
    int b;
    int *pp;

    a = 10;
    b = 20;

    printf("%d %d\n", a, b);
    //10 20\n

    pp = &a; //pointer set to the address of a. 
    *pp = 333; //set the value stored at the address of pp to 333. (a = 333)

    printf("%d %d\n", a, b);
    //333 20\n

    pp = &b; //pointer set to the address of b. 
    a = 444; 
    b = 555;

    printf("%d %d\n", a, b);
    //444 555
    printf("%d\n", *pp);
    //555
    printf("%p\n", (void *)pp);
    //some memory address allocated from the heap will be printed here- this changes from run to run as heap is allocated at runtime. 
}
