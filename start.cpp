#include <iostream>
#include <fstream>
//g++.exe -static -static-libgcc -static-libstdc++ -g start.cpp -o start

int main() {
    std::string filename = "pyScripts/main.py";
    std::string command = "py ";
    command += filename;
    system(command.c_str());
    return 0;
}