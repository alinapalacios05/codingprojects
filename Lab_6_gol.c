/*
 * Swarthmore College, CS 31
 * Copyright (c) 2020 Swarthmore College Computer Science Department,
 * Swarthmore PA, Professors Tia Newhall, Kevin Webb, and Vasanta Chaganti
 * Alina Palacios and Maria Quiroz

// Top-Level Comments: For gol.c, we implemented various helper functions to 
// successfully play Game of Life. We included two helper functions called 
// count_neighbors and update_nb. Count-neighbors was responsible for checking
// every cell on the grid and counting the neighbors the current cell. To do
// this, we used the operand % to wrap around the grid when checking for live
// cells at the edges of the grid. For update_nb, this function was responsible
// for determining whether a cell was dead or alive based on the number of 
// neighbors the current cell had. Finally, we added conditions to the play_gol 
// functions that would determine whether to animate cells when the output_mode
// was either 1 or 0. 

*
 * To run:
 * ./gol file1.txt  0  # run with config file file1.txt, do not print board
 * ./gol file1.txt  1  # run with config file file1.txt, ascii animation
 */

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>

struct gol_data {

   int rows;  // the row dimension
   int cols;  // the column dimension
   int iters; // number of iterations to run the gol simulation
   int pairs; // total coordinate pairs
   int output_mode; // set to:  OUTPUT_NONE or OUTPUT_ASCII   
   int *og_board; //memory address of original board
   int *new_board; //memory address of new board

};

/****************** Function Prototypes **********************/
// Function prototypes, declared here so they can be called in main

// implements the main gol game-playing loop
void play_gol(struct gol_data *data);

// initializes game data from the input file and command-line args
int init_game_data_from_args(struct gol_data *data, char *argv[]);

// prints board to the terminal (for OUTPUT_ASCII mode) 
void print_board(struct gol_data *data, int round);

// counts cells' neighbors
void count_neighbors(struct gol_data *data);

// updates new generation of cells
void update_nb(struct gol_data *data, int x, int y, int neighs);

/**********************************************************/
int main(int argc, char *argv[]) {

   int ret;
   struct gol_data data;
   double secs;

   /* check number of command line arguments */
   if (argc < 3) {
      printf("usage: ./gol <input-file.txt> <0|1>\n");
      printf("(0 with no visualization, 1: with ascii visualization)\n");
      exit(1);
   }

   /* Initialize game state (all fields in data) from information 
    * read from input file */
   ret = init_game_data_from_args(&data, argv);
   print_board(&data, 0);
   if (ret != 0) {
      printf("Error init'ing with file %s, mode %s\n", argv[1], argv[2]);
      exit(1);
   } 


   struct timeval start, end;
   long micros;
                
   gettimeofday(&start, NULL);

   data.output_mode = atoi(argv[2]);

   /* Invoke play_gol in different ways based on the run mode */
   if (data.output_mode == OUTPUT_NONE) {  // run with no animation
      play_gol(&data);
   }
   else if (data.output_mode == OUTPUT_ASCII) { // run with ascii animation
           play_gol(&data);
   
           print_board(&data, data.iters);
   } 
   else {
        printf("Unknown output mode: %d\n", data.output_mode);
        exit(1);
   }

   /* The total runtime in seconds, including fractional seconds
    * (e.g., 10.5 seconds should NOT be truncated to 10).
    */

   secs = 0.0;
   gettimeofday(&end, NULL);
   micros = ((end.tv_sec-start.tv_sec) * 1000000) + (end.tv_usec-start.tv_usec);
   secs = micros / 1000000.0;


   // Printing the total runtime, in seconds. */
   fprintf(stdout, "Total time: %0.3f seconds\n", secs);
   fprintf(stdout, "Number of live cells after %d rounds: %d\n\n",
        data.iters, total_live);




  // TODO: clean-up before exit make sure to call
  //       frees, etc. to ensure there are no memory 
  //       leaks with valgrind
   // free up memory for boards
   free(data->og_board);
   free(data->new_board); 

   return 0;
}

/**********************************************************/
/* initialize the gol game state from command line arguments
 *       argv[1]: name of file to read game config state from
 *       argv[2]: run mode value
 * data: pointer to gol_data struct to initialize
 * argv: command line args 
 *       argv[1]: name of file to read game config state from
 *       argv[2]: run mode
 * returns: 0 on success, 1 on error
 */
int init_game_data_from_args(struct gol_data *data, char *argv[]) {
   int rows, cols, iters, coords;
   int i, j, r, c;
                                     
   FILE *f = fopen(argv[1], "r");
   if (f == NULL) {
      perror("fopen");
      return 1;
   }

   //reads in info from file
   fscanf(f, "%d %d %d %d", &rows, &cols,
                  &iters, &coords);

   // copy read in information to struct data
   data->rows = rows;
   data->cols = cols;
   data->iters = iters;

   // allocate in a single malloc of NxM int-sized elements:
   data->og_board = malloc(sizeof(int) * rows * cols);
   data->new_board = malloc(sizeof(int) * rows *cols);

   if (data->og_board == NULL) {
      printf("ERROR: malloc failed!\n");
      exit(1);
   }

   // initially sets both boards with zeros 
   for (i = 0; i < rows; i++) {
       for (j = 0; j < cols; j++) {
           data->og_board[i*cols + j] = 0;
           data->new_board[i*cols + j] = 0;
       }
   }

   // this loop reads in coordinates into r and c
   // then sets those coords on og_board as 1
   for (i = 0; i < coords; i++) {
       fscanf(f, "%d %d", &r, &c);

       data->og_board[(r)*cols + (c)] = 1;
   }

   /* fclose, closes the file since we are done 
    * reading from it.
    */
   fclose(f);
   return 0;
}

/**********************************************************/
/* the gol application main loop function:
 *   runs rounds of GOL, 
 *     * updates program state for next round (world and total_live)
 *     * performs any animation step based on the output/run mode
 *
 *   data: pointer to a struct gol_data initialized with
 *         all GOL game playing state
 */
void play_gol(struct gol_data *data) {
   int k;
   int round = 0;

   for (k = 0; k < data->iters; k++) {
       count_neighbors(data);
  
       round += 1;

       if (data->output_mode == OUTPUT_ASCII) {
          print_board(data, round);
          usleep(900000);
          system("clear");
       }
   }
   
}
  
/**********************************************************/
/* Print the board to the terminal. 
 *   data: gol game specific data
 *   round: the current round number
 */
void print_board(struct gol_data *data, int round) {
   int i, j;
   total_live = 0;

   /* Print the round number. */
   fprintf(stderr, "Round: %d\n", round);

   for (i = 0; i < data->rows; i++) {
       for (j = 0; j < data->cols; j++) {
           if (data->og_board[i*data->cols + j] == 1) {
              fprintf(stderr, " @");
              total_live += 1;
           }
           else {
                fprintf(stderr, " .");
           }
       }
       fprintf(stderr, "\n");
   }

   /* Print the total number of live cells. */
   fprintf(stderr, "Live cells: %d\n\n", total_live);
}

/**********************************************************/
/* Count the total neighboring cells of a given cell
 *   data: gol game specfic data
 */
void count_neighbors(struct gol_data *data) {
   int tracker;
   int new_y;
   int new_x;

   // loops through every cell
   for (int x = 0; x < data->rows; x++) {
       for (int y = 0; y < data->cols; y++) {
           // reset tracker to 0
           tracker = 0;
            
           //counts total neighbors
           for (int i = -1; i < 2; i++) {
               for (int j = -1; j < 2; j++) {
                   new_x = ((x + i + data->rows) % data->rows);
                   new_y = ((y + j + data->cols) % data->cols);

                   tracker += data->og_board[(new_x)*data->cols + (new_y)];
               }
           }
           //subtract center cell from total
           tracker -= data->og_board[(x*data->cols + y)];
           //updates cell's status on new board
           update_nb(data, x, y, tracker);
       }
   }
   int *temp = data->og_board;  
   data->og_board = data->new_board;
   data->new_board = temp;
}

/**********************************************************/
/*Updates new board based on how many neighbors a cell has
 *   data: gol game specfic data
 *   x and y: are used to know the location of the current 
 *      cell being updated
 *   neighs: total neighbors the current cell has
 */
void update_nb(struct gol_data *data, int x, int y, int neighs) {

   if (data->og_board[x*data->cols + y] == 1) {
      if (neighs <= 1) {
         data->new_board[x*data->cols + y] = 0;
      }
      else if (neighs >= 4) {
              data->new_board[x*data->cols + y] = 0;                                               
      }
      else {
          data->new_board[x*data->cols + y] = data->og_board[x*data->cols + y];
     }
   }

   else {
        if (neighs == 3) {
           data->new_board[x*data->cols + y] = 1;
        }
        else {
            data->new_board[x*data->cols + y] = data->og_board[x*data->cols + y];
        }
   }
}


