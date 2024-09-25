
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


//alternatively, could include the file in the gcc command. 
//gcc -o program02 program02.c program01.c

int expo(int a, int b){

        double c = pow(a,b);

        printf("Answer is %f\n", c);
        return c;

}
