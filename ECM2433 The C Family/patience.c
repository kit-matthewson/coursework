#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <wchar.h>

#include "patience.h"
#include "shuffle.h"

/* pstatistics.c depends on this file and so has a conflicting main */
/* #define RUN_MAIN */

#ifdef RUN_MAIN
int main(int argc, char** argv) {
  int seed = -1;

  if (argc > 1) {
    seed = atoi(argv[1]);
  }

  int* deck = create_deck();
  shuffle(deck, NUM_CARDS, seed);

  int remaining = play(deck, 1);

  if (remaining > 0) {
    printf("Loss: %d cards remain\n", remaining);
  } else if (remaining == 0) {
    printf("Win: no cards remain\n");
  } else {
    return 1;
  }

  free(deck);

  return 0;
}
#endif

/*
 * Simulates a game of patience.
 *
 * Parameters:
 * - deck: Array of integers in [1:13] representing the deck.
 * - verbose: 0 to give no output, 1 to print visible cards.
 * Returns:
 * - Number of cards remaining in the deck at the end of the game.
 * - -1 if memory allocation fails.
 */
int play(int* deck, int verbose) {
  CardStack card_stack;
  card_stack.deck = deck;
  card_stack.head = NUM_CARDS - 1;

  int visible[9];

  visible[0] = draw_card(&card_stack);
  visible[1] = draw_card(&card_stack);
  int num_visible = 2;

  while (card_stack.head >= 0 && num_visible < 10) {
    /* Because every cover may result in a new 11 pair or JQK triple, we must repeat this until no cards are covered */
    bool changed;
    do {
      changed = false;

      /* Deal with 11 pairs: we cover the first pair until none remain */
      PairsResult* pairs = add_to_11(visible, num_visible);
      if (pairs == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return -1;
      }

      if (pairs->length > 0) {
        int* pair = pairs->array[0];

        if (verbose) {
          pprint_ints(visible, num_visible, 9);
          printf("    %d and %d add to 11\n", visible[pair[0]],
                 visible[pair[1]]);
        }

        if (card_stack.head <= 1) {
          card_stack.head = -1;
          break;
        } else {
          visible[pair[0]] = draw_card(&card_stack);
          visible[pair[1]] = draw_card(&card_stack);
        }

        changed = true;
      }
      free_pairs_result(pairs);

      /* Deal with JQK pairs by covering the first triple until none remain */
      PairsResult* jqks = jqk(visible, num_visible);
      if (jqks == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return -1;
      }

      if (jqks->length > 0) {
        int* triple = jqks->array[0];

        if (verbose) {
          pprint_ints(visible, num_visible, 9);
          printf("    JQK visible\n");
        }

        if (card_stack.head <= 2) {
          card_stack.head = -1;
          break;
        }

        visible[triple[0]] = draw_card(&card_stack);
        visible[triple[1]] = draw_card(&card_stack);
        visible[triple[2]] = draw_card(&card_stack);

        changed = true;
      }
      free_pairs_result(jqks);

    } while (changed);

    /* We have covered as many cards as possible, so must start a new pile */
    if (verbose) {
      pprint_ints(visible, num_visible, 9);
      printf("    start a new pile\n");
    }

    if (card_stack.head <= 0) {
      card_stack.head = -1;
      break;
    }

    if (num_visible >= 9) {
      break;
    }

    int draw = draw_card(&card_stack);
    visible[num_visible] = draw;
    num_visible++;
  }

  return card_stack.head + 1;
}

/*
 * Constructs a complete deck of 52 cards.
 *
 * Returns:
 * - Pointer to an array of `#NUM_CARDS` integers in the range [1:13].
 * - `NULL` if memory allocation fails.
 */
int* create_deck() {
  int* deck = malloc(sizeof(int) * NUM_CARDS);
  if (!deck) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  int i;
  for (i = 0; i < NUM_CARDS; i++) {
    deck[i] = (i % 13) + 1;
  }
  return deck;
}

/* Draws a card off the card stack, returns it, and decrements the head pointer.
 *
 * Parameters:
 * - stack: The `CardStack` to draw from
 * Returns:
 * - Top element of `stack`
 * - `-1` if stack is empty
 */
int draw_card(CardStack* stack) {
  if (stack->head < 0) {
    fprintf(stderr, "Tried to draw from empty deck\n");
    return -1;
  }

  return stack->deck[stack->head--];
}

/*
 * Prints an array of integers such that it has a fixed width.
 *
 * Parameters:
 * - arr: The array of integers to print.
 * - n: The length of `arr`.
 * - max_length: The maximum length to account for.
 */
void pprint_ints(int* arr, int n, int max_length) {
  int i;
  for (i = 0; i < max_length; i++) {
    if (i < n) {
      printf("%-3d", arr[i]);
    } else {
      printf("   ");
    }
  }
}

/*
 * Frees a `PairsResult`.
 *
 * Parameters:
 * - result: Pointer to the `PairsResult` to free.
 */
void free_pairs_result(PairsResult* result) {
  int i;
  for (i = 0; i < result->length; i++) {
    free(result->array[i]);
  }
  free(result->array);
  free(result);
}

/* Finds all pairs of cards that sum to 11 and returns their indicies.
 *
 * Parameters:
 * - arr: Array of integers.
 * - n: Length of `arr`.
 * Returns:
 * - `PairsResult` struct containing an array of int[2] pairs of indices into `arr` and the length of this array.
 * - `NULL` if memory allocation fails.
 */
PairsResult* add_to_11(int* arr, int n) {
  /* Allocate enough memory for the maximum number of pairs */
  int** pairs = malloc(sizeof(int*) * ((n * (n - 1)) / 2));
  if (!pairs) {
    fprintf(stderr, "Memory allocation failed");
    return NULL;
  }

  int num_pairs = 0;

  int i, j;
  for (i = 0; i < n - 1; i++) {
    for (j = i + 1; j < n; j++) {
      if (arr[i] + arr[j] == 11) {
        int* pair = malloc(sizeof(int) * 2);
        if (!pair) {
          fprintf(stderr, "Memory allocation failed\n");
          for (i = 0; i < num_pairs; i++) {
            free(pairs[i]);
          }
          free(pairs);
          return NULL;
        }

        pair[0] = i;
        pair[1] = j;

        pairs[num_pairs] = pair;

        num_pairs++;
      }
    }
  }

  PairsResult* result = malloc(sizeof(PairsResult));
  if (!result) {
    fprintf(stderr, "Memory allocation failed\n");
    for (i = 0; i < num_pairs; i++) {
      free(pairs[i]);
    }
    free(pairs);
    return NULL;
  }

  result->array = pairs;
  result->length = num_pairs;

  return result;
}

/*
 * Finds all triples of J (11), Q (12), and K (13) and returns their indicies.
 *
 * Parameters:
 * - arr: Array of integers.
 * - n: Length of `arr`.
 * Returns:
 * - `PairsResult` of all the JQK triples found.
 * - `NULL` if memory allocation fails.
 */
PairsResult* jqk(int* arr, int n) {
  int* res = malloc(sizeof(int) * 12);
  if (!res) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  /* First we find all the Jacks, Queens, and Kings */
  int* j_arr = &res[0];
  int* q_arr = &res[4];
  int* k_arr = &res[8];

  int num_j = 0, num_q = 0, num_k = 0;

  int i;
  for (i = 0; i < n; i++) {
    int n = arr[i];

    if (n == 11) {
      j_arr[num_j] = i;
      num_j++;
    } else if (n == 12) {
      q_arr[num_q] = i;
      num_q++;
    } else if (n == 13) {
      k_arr[num_k] = i;
      num_k++;
    }
  }

  PairsResult* result = malloc(sizeof(PairsResult));
  int** triples = malloc(sizeof(int*) * num_j * num_q * num_k);

  if (!result || !triples) {
    fprintf(stderr, "Memory allocation failed\n");
    free(res);
    free(triples);
    free(result);
    return NULL;
  }

  int num_triples = 0;

  int j, q, k;
  for (j = 0; j < num_j; j++) {
    for (q = 0; q < num_q; q++) {
      for (k = 0; k < num_k; k++) {
        int* triple = malloc(sizeof(int) * 3);
        if (!triple) {
          fprintf(stderr, "Memory allocation failed\n");

          for (i = 0; i < num_triples; i++) {
            free(triples[i]);
          }
          free(triples);
          free(result);

          return NULL;
        }

        triple[0] = j_arr[j];
        triple[1] = q_arr[q];
        triple[2] = k_arr[k];

        triples[num_triples] = triple;

        num_triples++;
      }
    }
  }

  result->array = triples;
  result->length = num_j * num_q * num_k;

  free(res);

  return result;
}
