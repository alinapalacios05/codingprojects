/*
  Copyright (c) 2020
  Swarthmore College Computer Science Department, Swarthmore PA
  J. Brody, A. Danner, M. Gagne, L. Meeden, Z. Palmer, A. Soni, M. Wehar
  Distributed as course material for Fall 2020
  CPSC 035: Data Structures and Algorithms
  https://tinyurl.com/yyr8mdoh
*/

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unistd.h>
#include <utility>


#include "adts/list.h"
#include "asciimationFunctions.h"
#include "linkedList.h"

using namespace std;

List<pair<int, string>>* loadMovie(string filename) {
    ifstream myFile;
    
    myFile.open(filename);
    if(!myFile.is_open()) {
      throw runtime_error("file " + filename + "failed to open ");
    }

    string data;
    string newstr = "";
    LinkedList<pair<int, string>>* list = new LinkedList<pair<int, string>>();

    int frame;
    getline(myFile, data);
    //first 'data' is an integer(time for frame)

    while (!myFile.eof()) {
 
      frame = stoi(data);
      //13 iterations for the string
      for(int i=0; i<13; i++){  
          getline(myFile, data);
          newstr = newstr + data + "\n"; //keep on appending lines to newstr
      }
      pair<int,string> p1(frame, newstr);
      newstr = "";
      list->insertLast(p1);
      getline(myFile, data);
      
      
  }
    return list; 
}

void playMovie(List<pair<int, string>>* list) {
  //for loop to go thru 13 pairs, and cout/display the string in the pair
  int length = list->getSize();
  for(int i = 0; i < length; i++) {
    pair<int,string> pair1= list->get(i);
    int time = pair1.first; 
    cout<< pair1.second; 
    usleep(time *(1000000/15)); //sleep
    system("clear");
    
  }

} 