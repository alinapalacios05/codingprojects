/*
 * Swarthmore College, CS 31
 * Copyright (c) 2020 Swarthmore College Computer Science Department,
 * Swarthmore PA, Professor Vasanta Chaganti
 * Lab 4, Alina Palacios and Maria Quiroz
 * */

/* 
 *  The purpose of this program is to compute the statistics on a set of values that it reads in file from. The first function called get_values reads in the values and dynamically allocates more space by douubling the space of the old array and making a new one with doubled the space. The old array is freed, leaving more space. Next, a bubble sorter is used to organize the values of the input files from greatest to  least. Once the values are organized, the third function calculates the max, min,
 median and std dev of the input file. Finally, the stat values are printed out.  
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "readfile.h"

/* 
 * N: strart size for first dynamically allocated array of values
 * MAXFILENAME: max length of input file name string
 */
#define N             20
#define MAXFILENAME   32
// you can add your own constants (using #define) here if needed

/* function prototypes */
float *get_values(int *size, int *capacity, char *filename);
void sort_array(float *values, int num);
void print_stats(float *values, int num, int a_size);


/**********************************************************************/
int main(int argc, char *argv[]) {

  //
  char filename[MAXFILENAME];
  float *vals=NULL;
  int size, capacity;

  // this code checks command line args to make sure program was run
  // with filename argument.  If not, calls exit to quit the program
  if(argc != 2) {
    printf ("usage: ./stats filename\n");
    exit(1);
  }
  // this copies the filename command line argument into the 
  // string variable filename
  strncpy(filename, argv[1], MAXFILENAME-1);

  // call get_values function:
  vals = get_values(&size, &capacity, filename);

  return 0;
}
/**********************************************************************/
/* This function reads in values from the input file into a dynamically
 * allocated array of floats that it returns.  It uses a doubling 
 * algorithm to increase the size of the array as it needs more space
 * for the values read in from the file.
 * 
 *   size: set to the number of data values read in from the file
 *   capacity: set to the total number of buckets in the returned array
 *   filename: the name of the file to open
 *
 *   returns: the base address of the array of values read in 
 *            or NULL on error
 *
 *  
 */
float *get_values(int *size, int *capacity, char *filename){
  float *values = NULL; //array of numbers in file
  int num = 0; //initial index being filled in array
  int a_size = 20; //size of initial array
  int ret; //holds return of 0 or -1 from read_float
  float *array_1; //new array
  float f; //address read in by read_float
  int i; //loop
  

  if(open_file(filename)) {  //open the file
    return NULL;
  }

  values = (float*)malloc(sizeof(float)*20); //create initial array
 
  ret = read_float(&f); //check if valid float is read in
  while (ret == 0) { //while numbers are in file, add numbers to array
      if (num > a_size) { //check if index is bigger than array size
          a_size = 2 * a_size; //double size of array 
          array_1 = (float*)malloc(sizeof(float)*a_size); //create new array
          
          //copy values of old array to new array
          for (i = 0 ; i < num; i++){
              array_1[i] = values[i];
          } 

          free(values); //free space of the old array 
          values = array_1;} //copy new array to values 

      ret= read_float(&values[num]); //add numbers in file to array
            
      num = num + 1; //keeps track of number of buckets there are in the array 
  }
 
  sort_array(values, num);

  print_stats(values, num, a_size);

  close_file(); // close the file
  return values;  // return the values array
}

/* This functions sort the values in the input value from greatest to least using bububble sort. 
*/
void sort_array(float *values, int num){
    int keepGoing=1;
    float first;

    while(keepGoing==1)
    {
      keepGoing=0;
      for(int i=0; i<num; i++){
         if(values[i]<values[i+1]){
           first = values[i];
           values[i] = values[i+1];
           values[i+1] = first;
           keepGoing=1;
        }
      }
    }
  }

/* This function calculates and prints out the stats of the input values (mean, 
 * median, max, min and std dev. 
*/

void print_stats(float *values, int num, int a_size) {
  int unused_array; 
  float total; 
  float mean; 
  int middle; 
  int ev_upper; 
  int ev_lower; 
  float median; 
  float sdev; 
  float sub_mean;
  float result;
  float new_mean;
  float total2; 

      printf("\n Results:\n -------\n");

      //print num values
      printf(" num values:\t%d\n", num);

      //print min
      printf(" min:\t%13.3f\n", values[num-1]);

      //print max
      printf(" max:\t%13.3f\n", values[0]);

      //calculate mean
      for(int i=0; i<num; i++){
         total = total + values[i];
      }
      mean = total / num;
      //print mean
      printf(" mean:\t%13.3f\n", mean);

      //calculate and print median
      if (num%2 != 0){
         middle = num / 2;
         printf(" median:\t%5.3f\n", values[middle]);
      }
      else{
         ev_upper = num - (num/2);
         ev_lower = (num/2) - 1;

         median = (values[ev_upper] + values[ev_lower])/2;
         printf(" median:\t%5.3f\n", median);
      }
         
     total2 = 0; 
     for(int i = 0; i<num; i++){
       sub_mean = abs(values[i]-mean);
       result = sub_mean*sub_mean;
       total2 = total2 + result;
     }
     new_mean = total2/num;
     sdev = sqrt(new_mean);

     printf(" std dev:\t%5.3f\n", sdev);

     //calculate unused array capacity
     unused_array = a_size - num;
     //print unused array capacity
     printf(" unused array capacity:\t%d\n", unused_array);

}
