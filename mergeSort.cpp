/*
  Copyright (c) 2020
  Swarthmore College Computer Science Department, Swarthmore PA
  J. Brody, A. Danner, M. Gagne, L. Meeden, Z. Palmer, A. Soni, M. Wehar
  Distributed as course material for Fall 2020
  CPSC 035: Data Structures and Algorithms
  https://tinyurl.com/yyr8mdoh
*/

#include <iostream>
#include "mergeSort.h"
using namespace std;

// TODO: you will need to write an appropriate "merge" function here
// It does not need to be in your header file because no one else will call it.
int* merge(int* array1, int* array2, int len1, int len2){
  //function that takes two arrays and returns a new array of sorted elements
  int newLen = len1+len2;
  int* newArray = new int[newLen];
  //pick elements in sorted order
  //compare first elements and add smaller one
  int ind1 = 0;
  int ind2 = 0;
  int newind = 0;
  
  while (newind<newLen) {
    //adds from array1 if element is smaller than or equal to corresponding one in array2
    if(ind1<len1 && ind2<len2 && array1[ind1]<=array2[ind2]){
      newArray[newind] = array1[ind1];
      ind1++;
    }
    //adds from array2 if element is smaller than corresponding one in array1
    else if(ind2<len2 && ind1<len1 && array1[ind1]>array2[ind2]){
      newArray[newind] = array2[ind2];
      ind2++;
    }
    else if(ind1 == len1 && ind2<len2){ //add everything left in array2
      newArray[newind] = array2[ind2];
      ind2++;
    }
    else if(ind2 == len2 && ind1 < len1){ //add everything left in array1
      newArray[newind] = array1[ind1];
      ind1++;
    }
    newind++;
  }
  return newArray;
}

void mergeSort(int *array, int length) {
  //"Divide and conquer" - main array -> two sub arrays that are then merged in right order
  if(length>1){
      int half = length/2;
      int* array1 = new int [half];

      for (int i=0; i < half; i++) {
        array1[i] = array[i];
      }
      
      int* array2 = new int [length-half];

      int j=0;
      for (int i=half; i < length; i++) {
        //this will be array2's j'th position but array's i'th position
        array2[j] = array[i];
        j++;
      }
      //for loop to fill array1
      mergeSort(array1, half);
      mergeSort(array2, length-half);
      
      int* sortedArray = merge(array1, array2, half, length-half);
      //call merge

      //copy data into *array
      for(int i=0; i<length; i++) {
        array[i] = sortedArray[i];
      }
      delete [] array1; 
      delete [] array2;
      delete [] sortedArray;
     //delete array1 and array2 and redundant sortedArray
  }
  
}
