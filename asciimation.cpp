/*
  Copyright (c) 2020
  Swarthmore College Computer Science Department, Swarthmore PA
  J. Brody, A. Danner, M. Gagne, L. Meeden, Z. Palmer, A. Soni, M. Wehar
  Distributed as course material for Fall 2020
  CPSC 035: Data Structures and Algorithms
  https://tinyurl.com/yyr8mdoh
*/

#include <iostream>
#include <string>
#include <utility>

#include "adts/list.h"
#include "asciimationFunctions.h"
#include "linkedList.h"

using namespace std;

int main(int argc, char** argv) {
    // TODO: write your program here
    
    if (argc == 2 || argc == 3) {
      string temp = argv[1];
      if(temp == "--reverse"){
        string FileName = argv[2]; 
        List<pair<int, string>>* movList = loadMovie(FileName);
      //create a new list then reverse contents of the first list
        int length = movList->getSize();
        List<pair<int, string>>* RevList = new LinkedList<pair<int, string>>;
        for(int i = 0; i<length; i++){
          pair<int, string> p1 = movList->get(i);
          RevList->insertFirst(p1); //new list in reverse order
        }
        playMovie(RevList);
      }
      else{
        string FileName = argv[1]; 
        List<pair<int, string>>* movList = loadMovie(FileName);
        playMovie(movList);
      }
    }
    else{
      cout <<"Incorrect number of arguments"<<endl; 
    }

    return 0;
}
