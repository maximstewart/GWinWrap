#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
using namespace std;

int main() {
    chdir("/opt/GWinWrap/");
    system("python3 GWinWrap.py");
return 0;
}
