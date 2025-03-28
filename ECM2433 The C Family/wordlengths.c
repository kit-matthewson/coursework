#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "histogram.h"

int main(int argc, char** argv) {
  if (argc != 2) {
    printf("Usage: %s <filename>\n", argv[0]);
    return -1;
  }

  FILE* fp;
  char buffer[256];

  /* Load the file pointer */
  if ((fp = fopen(argv[1], "r")) == NULL) {
    printf("Unable to read file %s: %d: %s\n", argv[1], errno, strerror(errno));
    return 1;
  }

  /* Count the number of lines in the file and find the longest word */
  int lines = 0;
  int max_length = 0;

  while (fgets(buffer, sizeof(buffer), fp) != NULL) {
    int length = strlen(buffer) - 1;
    if (length > max_length) {
      max_length = length;
    }

    lines++;
  }
  rewind(fp);

  /* Iterate over each word */
  char** words = malloc(sizeof(char*) * lines);
  if (!words) {
    fprintf(stderr, "Memory allocation failed\n");
    fclose(fp);
    return 1;
  }

  int i, j;
  for (i = 0; i < lines; i++) {
    /* Read a line and remove the '\n' */
    fgets(buffer, sizeof(buffer), fp);
    buffer[strcspn(buffer, "\n")] =
        '\0'; /* Find the location of the first '\n' and replace it with '\0' */

    /* Add the word to `words` */
    words[i] = malloc(sizeof(strlen(buffer) + 1));

    if (!words[i]) {
      fprintf(stderr, "Memory allocation failed\n");
      fclose(fp);

      for (j = 0; j < i; j++) {
        free(words[j]);
      }
      free(words);

      return 1;
    }

    strcpy(words[i], buffer);
  }

  /* Construct array of percentages of words of each length */
  int* word_lengths = (int*)malloc((max_length + 1) * sizeof(int));

  if (word_lengths == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    return -1;
  }

  word_lengths = histogram_lengths(words, lines);

  double* word_percentages = (double*)malloc((max_length + 1) * sizeof(double));

  if (word_percentages == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    return -1;
  }

  /* Draw the histogram (skipping 'words of length 0') */
  int x[max_length + 1];

  printf("Distribution of words in '%s':\n", argv[1]);
  for (i = 0; i < max_length; i++) {
    x[i] = i + 1;
    word_percentages[i] = (word_lengths[i + 1] / (float)lines) * 100;
  }

  histogram(x, word_percentages, max_length, 80);

  /* Free resources */
  free(word_lengths);
  free(word_percentages);

  for (i = 0; i < lines; i++) {
    free(words[i]);
  }

  fclose(fp);

  return 0;
}
