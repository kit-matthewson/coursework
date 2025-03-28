#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "histogram.h"
#include "patience.h"
#include "shuffle.h"

int main(int argc, char** argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <count>\n", argv[0]);
    return 1;
  }

  int n = atoi(argv[1]);
  int* result = many_plays(n);

  int labels[NUM_CARDS + 1];
  double values[NUM_CARDS + 1];

  int i;
  for (i = 0; i < NUM_CARDS + 1; i++) {
    labels[i] = i;
    values[i] = ((double)result[i] / n) * 100;
  }

  printf("Games simulated: %d\n", n);
  printf("Win rate: %.3f%% (loss: %.3f%%)\n", values[0], 100 - values[0]);
  printf("\nHistogram of cards remaining at game end (%%):\n");
  histogram(labels, values, NUM_CARDS + 1, 80);

  return 0;
}

/*
 * Plays patience `n` times and records the number of cards remaining at the end of each game.
 *
 * Parameters:
 * - n: The number of games to play.
 * Returns:
 * - An `int[53]` array, where the ith element is the number of times the game ended with i cards remaining.
 * - `NULL` if memory allocation fails.
*/
int* many_plays(int n) {
  int* result = malloc(sizeof(int) * (NUM_CARDS + 1));
  if (!result) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  int i;
  for (i = 0; i < NUM_CARDS + 1; i++) {
    result[i] = 0;
  }

  for (i = 0; i < n; i++) {
    int* deck = create_deck();
    shuffle(deck, NUM_CARDS, time(NULL) + (i * 100));

    int remaining = play(deck, 0);
    if (remaining < 0) {
      return NULL;
    }

    result[remaining]++;
  }

  return result;
}
