#include <iostream>
#include <fstream>


//g++.exe -static -static-libgcc -static-libstdc++ -g dataComp.cpp -o dataComp

int main() {
    std::string filename = "pyScripts/plot.py";
    std::string command = "py ";
    command += filename;
    system(command.c_str());
    return 0;
}