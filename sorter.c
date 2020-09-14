/*
 * Swarthmore College, CS 31
 * Copyright (c) 2020 Swarthmore College Computer Science Department,
 * Swarthmore PA, Professor Vasanta Chaganti

Alina Palacios, Mari Quiroz, Alex Comaniciu
CS31 Spring
02/04/2020

This program reads a collection of unsorted floats from a file, stores these
floats in an array, gives the user information about the floats, and then sorts
them from smallest to largest magnitude and prints the sorted array out.
*/

#include <stdio.h>      // the C standard I/O library
#include <stdlib.h>     // the C standard library
#include <string.h>     // the C string library
#include "readfile.h"   // my file reading routines

#define MAXFILENAME  128
#define ARRAYSIZE    1000

void get_filename_from_commandline(char filename[], int argc, char *argv[]);
void sort_array(float values[], int numbers);
int check_array(float values[], int numbers);

int main (int argc, char *argv[]) {

  int ret;                    /* for storing function return values */
  char filename[MAXFILENAME]; /* the input filename  */
  float values[ARRAYSIZE];    /* stores values read in from file */
  int numbers;
  float max;
  float min;

  get_filename_from_commandline(filename, argc, argv);

  ret = open_file(filename);
  if(ret == -1) {
    printf("ERROR: can't open %s\n", filename);
    exit(1);
  }

  ret = read_int(&numbers);
   if(ret == -1) {
    printf("ERROR: read_int failed\n");
    exit(1);
   }
  ret = read_float(&min);
   if(ret == -1) {
    printf("ERROR: read_float failed\n");
    exit(1);
   }
  ret = read_float(&max);
   if(ret == -1) {
    printf("ERROR: read_float failed\n");
    exit(1);
   }


  printf("Reading file named %s\n", filename);
  printf("The file contains %d floating point numbers, ranging from %.2f to"
      " %.2f\n",  numbers, min, max);

  for (int i=0; i<numbers; i++){
  ret = read_float(&values[i]);
   if(ret == -1) {
    printf("ERROR: read_float failed\n");
    exit(1);
  }
  }
  printf("The unsorted values are: ");
  for (int i=0; i<numbers; i++){
  printf("%.2f ",values[i]);
  }
  printf("\n");
  
  sort_array(values, numbers);

  ret = check_array(values, numbers);
  if(ret == -1) {
    printf("ERROR: array not sorted\n");
    exit(1);
  }
  printf("The sorted values are: ");
  for (int i=0; i<numbers; i++){
  printf("%.2f ",values[i]);
  }
  printf("\n");

  close_file();
  return 0;
}
/* THE FOLLOWING FUNCTION IS PROVIDED FOR YOU
 * DO NOT MODIFY, OR DO SO AT YOUR OWN RISK!
 *
 * This function gets the filename passed in as a command line option
 * and copies it into the filename parameter. It exits with an error
 * message if the command line is badly formed.
 *
 *   filename: the string to fill with the passed filename
 *   argc, argv: the command line parameters from main
 *               (number and strings array)
 */
void get_filename_from_commandline(char filename[], int argc, char *argv[]) {

  if(argc != 2) {
    printf("Usage: ./exp integer_file\n");
    exit(1);
  }
  if(strlen(argv[1]) >= MAXFILENAME) {
    printf("Filename, %s, is too long, cp to shorter name and try again\n",
        filename);
    exit(1);
  }
  strcpy(filename, argv[1]);
}
  /* sort_array
   * This function sorts the given array of floats using bubble sort. It updates
   * the array values[] such that all the floats are sorted in acsending order.
   *
   * @param name: values[], an array of floats, numbers, and int representing 
   * the number of floats in the array values[]
   * @return: nothing
   */
  void sort_array(float values[],int numbers){
      for(int i=0; i<numbers; i++){
        for(int j=0; j<numbers-i-1; j++){
        if(values[j]>values[j+1]){
          int temp = values[j];
          values[j] = values[j+1];
          values[j+1]=temp;
        }
         }
      }
  }
 /* check_array
  * This function checks whether or not the "sorted array" was actually sorted
  * by comparing the values in the array to eachother to check if they are in
  * ascending order.
  *
  * @param name: values[], an array of floats, numbers, and int representing
  * the number of floats in the array values[]
  * @return: the function returns -1 if the array is not sorted properly and 0
  * if it is.
  */
  int check_array(float values[], int numbers){
      for(int i=0; i<numbers-1; i++){
         if (values[i] > values[i+1]){
           return -1;
         }
      }
  return 0;
  }
