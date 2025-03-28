#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "anagram.h"

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
  if (head == NULL) {
    printf("Failed to create linked list.\n");
    return 1;
  }
  printf("Created linked list of anagrams.\n\n");

  while (1) {
    char word[100];
    printf("Enter a word: ");
    scanf("%99s", word);
    char* key = generate_key(word);
    
    PrimaryNode* current = head;
    while (current != NULL && strcmp(current->key, key)) {
      current = current->next;
    }

    if (current == NULL) {
      printf("Word not found in list.\n");
    } else {
      int num_anagrams = secondary_list_length(current->secondary_list);
      printf("Word has %d anagrams:\n", num_anagrams);

      SecondaryNode* secondary_head = current->secondary_list;
      while (secondary_head != NULL) {
        printf("   %s\n", secondary_head->word);
        secondary_head = secondary_head->next;
      }
    }

    printf("\n");
  }

  free_primary_list(head);
}
