#if !defined(PATIENCE_H)
#define PATIENCE_H

#define NUM_CARDS 52

typedef struct {
  int head;
  int* deck;
} CardStack;

typedef struct {
  int** array;
  size_t length;
} PairsResult;

int play(int* deck, int verbose);
int* many_plays(int n);

int* create_deck();
int draw_card(CardStack* stack);
void pprint_ints(int* arr, int n, int max_length);

void free_pairs_result(PairsResult* result);
PairsResult* add_to_11(int* arr, int n);
PairsResult* jqk(int* arr, int n);

#endif
