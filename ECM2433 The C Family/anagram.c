#include <ctype.h>
#include <errno.h>
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#include "anagram.h"

/* anaquery.c depends on this file and so has a conflicting main */
/* #define RUN_MAIN */

#ifdef RUN_MAIN
#include "histogram.h"

/*
 * Produces a data structure of anagrams of words from a given file.
 *
 * Usage: anagram <filename>
 * Parameters:
 * - filename: The name of the file to read the input words from, with each word on a new line.
 */
int main(int argc, char** argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
    return 1;
  }

  char** words;
  int num_words = read_words_array(argv[1], &words);
  if (num_words < 1) {
    printf("Reading words file failed.\n");
    return 1;
  }

  printf("Read %d words, creating linked list...\n", num_words);
  PrimaryNode* head = make_anagram_list(words, num_words);
  printf("Created linked list, calculating statistics...\n");

  /* Find the statistics on the anagrams */
  int max_variations_count = 0;
  PrimaryNode* max_variations_node = NULL;

  int longest_pair_count = 0;
  PrimaryNode* longest_pair_node = NULL;

  int variants[11];
  int i;
  for (i = 0; i < 11; i++) {
    variants[i] = 0;
  }

  PrimaryNode* current = head;
  while (current != NULL) {
    int variations = secondary_list_length(current->secondary_list);
    int len = strlen(current->key);

    if (variations > max_variations_count) {
      max_variations_node = current;
      max_variations_count = variations;
    }

    if (2 <= variations && variations <= 12) {
      variants[variations - 2]++;
    }

    if (variations == 2 && len > longest_pair_count) {
      longest_pair_count = len;
      longest_pair_node = current;
    }

    current = current->next;
  }

  /* Print statistics */
  printf("\nThe key with the most variations is '%s', forming %d words:\n",
         max_variations_node->key, max_variations_count);
  SecondaryNode* secondary_list = max_variations_node->secondary_list;
  while (secondary_list != NULL) {
    printf("   %s\n", secondary_list->word);
    secondary_list = secondary_list->next;
  }

  printf("\nThe longest pair of words has the key '%s', with:\n",
         longest_pair_node->key);
  secondary_list = longest_pair_node->secondary_list;
  while (secondary_list != NULL) {
    printf("   %s\n", secondary_list->word);
    secondary_list = secondary_list->next;
  }

  printf("\nHistogram of log(variants):\n");
  int labels[11];
  double values[11];
  for (i = 0; i < 11; i++) {
    labels[i] = i + 2;

    if (variants[i] > 0) {
      values[i] = log(variants[i]);
    } else {
      values[i] = 0;
    }
  }
  histogram(labels, values, 11, 80);

  /* Because the nodes take ownership of their key/word, this also frees words[] */
  free_primary_list(head);

  return 0;
}

#endif

/*
 * Reads an array of words from a file, where each word is on a new line.
 * Places this array at `words`.
 *
 * Parameters:
 * - filename: The name of the file to read from.
 * - words: Pointer to a `char[]` where the read words will be stored.
 * Returns:
 * - The number of words read (and so length of `words`).
 * - -1 if an error occurs.
 */
int read_words_array(char* filename, char*** words) {
  FILE* fp;

  if ((fp = fopen(filename, "r")) == NULL) {
    printf("Unable to read file %s: %d: %s\n", filename, errno,
           strerror(errno));
    return -1;
  }

  /* Count the number of lines in the file */
  int lines = 0;
  char buffer[256];

  while (fgets(buffer, sizeof(buffer), fp) != NULL) {
    lines++;
  }

  rewind(fp);

  /* Generate a list of words */
  *words = malloc(sizeof(char*) * lines);
  if (!*words) {
    fprintf(stderr, "Memory allocation failed\n");
    fclose(fp);
    return -1;
  }

  int i, j;
  for (i = 0; i < lines; i++) {
    /* Read a line and remove the '\n' */
    fgets(buffer, sizeof(buffer), fp);
    buffer[strcspn(buffer, "\n")] =
        '\0'; /* Find the location of the first '\n' and replace it with '\0' */

    /* Add the word to `words` */
    (*words)[i] = malloc(strlen(buffer) + 1);
    if (!(*words)[i]) {
      fprintf(stderr, "Memory allocation failed\n");
      fclose(fp);
      for (j = 0; j < i; j++) {
        free((*words)[j]);
      }
      free(*words);
      return -1;
    }

    strcpy((*words)[i], buffer);
  }

  fclose(fp);

  return lines;
}

/*
 * Calculates the length of a secondary linked list/
 *
 * Parameters:
 * - head: Pointer to the head of the linked list.
 * Returns:
 * - Length of the linked list.
 */
int secondary_list_length(SecondaryNode* head) {
  int length = 0;

  while (head != NULL) {
    length++;
    head = head->next;
  }

  return length;
}

/*
 * Constructs an anagram list from an array of words.
 *
 * Parameters:
 * - words: Array of words to store in the linked list.
 * - n: The length of `words`.
 * Returns:
 * - The head node of a primary linked list, where each primary node contains the head of a secondary linked list of words.
 */
PrimaryNode* make_anagram_list(char** words, int n) {
  PrimaryNode* head = NULL;
  int i, j;

  for (i = 0; i < n; i++) {
    insert_word(words[i], &head);
  }

  return head;
}

/*
 * Creates and initializes a `PrimaryNode` with the given key.
 *
 * Parameters:
 * - key: The key to assign to the `PrimaryNode`.
 * Returns:
 * - A pointer to the allocated primary node.
 * - `NULL` if memory allocation fails.
 */
PrimaryNode* create_primary_node(char* key) {
  PrimaryNode* node = malloc(sizeof(PrimaryNode));
  if (!node) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  node->key = key;
  node->next = NULL;
  node->secondary_list = NULL;

  return node;
}

/*
 * Creates and initializes a `SecondaryNode` with the given word.
 *
 * Parameters:
 * - word: The word to assign to the `SecondaryNode`.
 * Returns:
 * - A pointer to the allocated secondary node.
 * - `NULL` if memory allocation fails.
 */
SecondaryNode* create_secondary_node(char* word) {
  SecondaryNode* node = malloc(sizeof(SecondaryNode));
  if (!node) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  node->word = word;
  node->next = NULL;

  return node;
}

/*
 * Frees the memory allocated for a primary list and its associated secondary lists.
 *
 * Parameters:
 * - head: The head of the list to free.
 */
void free_primary_list(PrimaryNode* head) {
  while (head != NULL) {
    PrimaryNode* next = head->next;
    free_secondary_list(head->secondary_list);
    free(head->key);
    free(head);
    head = next;
  }
}

/*
 * Frees the memory allocated for a secondary list.
 *
 * Parameters:
 * - head: The head of the list to free.
 */
void free_secondary_list(SecondaryNode* head) {
  while (head != NULL) {
    SecondaryNode* next = head->next;
    free(head->word);
    free(head);
    head = next;
  }
}

/*
 * Casts two `void*` to `char*` and compares them alphabetically.
 *
 * Parameters:
 * - a: A pointer to the first character.
 * - b: A pointer to the second character.
 * Returns:
 * - An integer >0 if `a > b`, <0 if `a < b`, or 0 if `a == b`.
 */
int char_compare(const void* a, const void* b) {
  return (*(char*)a - *(char*)b);
}

/*
 * Gernerates a key for a word by sorting the letters of alphabetically and converting to lower case.
 * i.e., "Cat" -> "act"
 *
 * Parameters:
 * - word: The word to sort.
 * Returns:
 * - A pointer to a new string containing the key.
 * - `NULL` if memory allocation fails.
 */
char* generate_key(char* word) {
  size_t len = strlen(word);
  char* sorted = malloc(len + 1);
  if (!sorted) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  memcpy(sorted, word, len);
  sorted[len] = '\0';

  qsort(sorted, len, sizeof(char), char_compare);

  int i;
  for (i = 0; i < strlen(sorted); i++) {
    sorted[i] = tolower(sorted[i]);
  }

  return sorted;
}

/*
 * Inserts a word at the end of a secondary linked list.
 *
 * Parameters:
 * - word: The word to insert.
 * - head: Pointer to the head pointer of the secondary linked list, where the underlying `SecondaryNode*` may be modified in place.
 */
void insert_word_into_secondary(char* word, SecondaryNode** head) {
  SecondaryNode* new_node = create_secondary_node(word);
  if (!new_node) {
    return;
  }

  if (*head == NULL) {
    *head = new_node;
    return;
  }

  /* Add to the start of the secondary linked list */
  new_node->next = *head;
  *head = new_node;
}

/*
 * Inserts a word into the linked list.
 *
 * Parameters:
 * - word: The word to insert.
 * - head: Pointer to the head pointer of the primary linked list, where the underlying `PrimaryNode*` may be modified in place.
 */
void insert_word(char* word, PrimaryNode** head) {
  /* Get the word's key */
  char* key = generate_key(word);
  if (!key) {
    return;
  }

  PrimaryNode* current = *head;
  PrimaryNode* previous = NULL;

  /* Iterate over the primary list until we find the end of the list or a key <=
   * to one we want to insert. */

  /* Because the input words are expected to be in alphabetical order, it is most
   * efficient to store them in reverse alphabetical order, as it is fastest to
   * add new words to the front of the linked list.
   */
  while (current != NULL && strcmp(current->key, key) > 0) {
    previous = current;
    current = current->next;
  }

  /* We have found the existing primary node for this key */
  if (current != NULL && strcmp(current->key, key) == 0) {
    insert_word_into_secondary(word, &current->secondary_list);
    free(key); /* Key is unused */
    return;
  }

  /* There is no node for this key yet, we need to make one */
  PrimaryNode* new_primary = create_primary_node(key);
  if (!new_primary) {
    free(key);
    return;
  }

  insert_word_into_secondary(word, &new_primary->secondary_list);

  if (previous == NULL) {
    /* Insert at the beginning */
    new_primary->next = *head;
    *head = new_primary;
  } else {
    /* Insert in the middle or end */
    new_primary->next = current;
    previous->next = new_primary;
  }
}

/*
 * Prints a primary list and its secondary list (for debugging purposes).
 *
 * Parameters:
 * - head: Pointer to the head of the primary list to print.
 */
void print_list(PrimaryNode* head) {
  PrimaryNode* current_primary = head;

  while (current_primary != NULL) {
    printf("%s --> ", current_primary->key);

    SecondaryNode* current_secondary = current_primary->secondary_list;
    while (current_secondary != NULL) {
      printf("%s", current_secondary->word);
      if (current_secondary->next != NULL) {
        printf(" -> ");
      }
      current_secondary = current_secondary->next;
    }
    printf("\n");
    current_primary = current_primary->next;
  }
}
