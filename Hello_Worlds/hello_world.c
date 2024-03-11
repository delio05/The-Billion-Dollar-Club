// Jaden's hello world. Complicated as possible
#include <stdio.h>
#include <string.h>

#define H (char)(72)
#define e (char)(101)
#define l (char)(108)
#define o (char)(111)
#define W (char)(87)
#define r (char)(114)
#define d (char)(100)
#define space (char)(32)
#define exclam (char)(33)

#define MAX_BUFFER 256

int main() {
    char hello[MAX_BUFFER];
    hello[0] = H;
    hello[1] = e;
    hello[2] = l;
    hello[3] = l;
    hello[4] = o;
    hello[5] = space;
    hello[6] = W;
    hello[7] = o;
    hello[8] = r;
    hello[9] = l;
    hello[10] = d;
    hello[11] = exclam;
    hello[12] = '\0';

    for (int i = 0; i < strlen(hello); i++) {
        printf("%c", hello[i]);
    }

    printf("\n");

    return 0;
}
