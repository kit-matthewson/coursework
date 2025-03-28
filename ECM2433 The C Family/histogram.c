#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Prints a histogram.
 *
 * Parameters:
 * - x: Array of word lengths.
 * - y: Array of percentages corresponding to word lengths.
 * - n: Number of different word lengths.
 * - width: Width of the histogram in characters.
 */
void histogram(int* x, double* y, int n, int width) {
  /* Find the largest element of y */
  double max = 0;

  int i;
  for (i = 0; i < n; i++) {
    if (y[i] > max) {
      max = y[i];
    }
  }

  /* The number of '*' symbols per percentage point */
  double unit_char = max / width;

  /* Print the bars */
  double j;
  for (i = 0; i < n; i++) {
    printf("%-3d ", x[i]);
    for (j = 0.0; j < y[i]; j += unit_char) {
      printf("*");
    }
    printf("  %.3f\n", y[i]);
  }
}

/*
 * Computes the frequency of word lengths in an array of words.
 *
 * Parameters:
 * - strings: Array of words.
 * - n: Number of words in the array.
 *
 * Returns:
 * - Pointer to an integer array where each index represents a word length,
 *   and the value at that index represents the count of words of that length.
 * - Returns NULL if memory allocation fails.
 */
int* histogram_lengths(char** strings, int n) {
  /* Find the length of the longest string */
  int max = 0;
  int i;

  for (i = 0; i < n; i++) {
    int len = strlen(strings[i]);
    if (len > max) {
      max = len;
    }
  }

  /* Construct the output array */
  int* H = (int*)malloc((max + 1) * sizeof(int));

  if (H == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  memset(H, 0, (max + 1) * sizeof(int)); /* Fill the array with '0' */

  for (i = 0; i < n; i++) {
    int len = strlen(strings[i]);
    H[len]++;
  }

  return H; /* The caller will have to free H */
}
