#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
using namespace std;

int main() {
    chdir("/opt/FXWinWrap/");
    system("bash launch.sh");
return 0;
}
