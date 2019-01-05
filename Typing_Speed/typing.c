#include <stdio.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>

//Function creates a list of 9 words for the user, and tests the speed at which the user types all those words correctly into the standard output.


// Calculate number takes a Bool Array, a, (indicating which words have already been used), and a number, b, (how many words are left) and returns the array position of the random unused word.

int calculate_number(_Bool a[], int b) {
// return_val is set to 0. Temp randomly generates a number of the nth unused word.
   int return_val = 0;
   int temp = rand() % b;

   for(int i = 0; i < 9; i++)  {
      if(a[i] == 0 && temp != 0) {
         temp--;
         return_val++;
      } else if (a[i] == 0 && temp == 0) {
        // if the ith position is unused (a[i] == 0) and it is the nth word (temp == 0), return the value
         a[i] = 1;
         return return_val; }
      else {return_val++;}
   }
   return 100;
}



int main () {

   const char * words[9] = {"The","quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"};
   //Bool tracks which words are used
   _Bool used_words[9] = {0}; 
   char input[10];
   int current_words = 9;

   printf("This is a word typing game where you will be timed on how fast you can type 9 words. \n");
   printf("Are you ready to start the game? Enter 'yes' (in lower case) to start \n");

   scanf("%s", input);
   
   //Starts when the user says they are ready
   while(strcmp(input,"yes") != 0) {
      printf("Enter 'yes' when you are ready \n");
      scanf("%s", input);
   }

   struct timeval time_begin, time_end, time_diff;
   gettimeofday(&time_begin, NULL);
   
   srand(time(NULL));
   
   // While the user has not gone through all 9 words
   while(current_words != 0) {
      int position = calculate_number(used_words,current_words);
      
      printf("Please type the following word: %s \n", words[position]);
      
      // While the user has not gotten that particular word correct
      while(1) {
      scanf("%s", input);
      // If the words match, take one off of current words and break
      if(strcmp(input, words[position]) == 0) {current_words--; break;}
      printf("Incorrect entry, please try again \n");
      }
   }
   
   // Calculates end time and does the subtraction.
   gettimeofday(&time_end, NULL);
   timersub(&time_end, &time_begin, &time_diff);
   
   printf("Congratulations! You completed the challenge in %ld seconds %ld usec \n", time_diff.tv_sec, time_diff.tv_usec);
   
}
