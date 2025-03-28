#if !defined(ANAGRAM_H)
#define ANAGRAM_H

typedef struct PrimaryNode {
  char* key;
  struct PrimaryNode* next;
  struct SecondaryNode* secondary_list;
} PrimaryNode;

typedef struct SecondaryNode {
  char* word;
  struct SecondaryNode* next;
} SecondaryNode;

int read_words_array(char* filename, char*** words);
PrimaryNode* make_anagram_list(char** words, int n);

PrimaryNode* create_primary_node(char* key);
SecondaryNode* create_secondary_node(char* word);

void free_primary_list(PrimaryNode* head);
void free_secondary_list(SecondaryNode* head);

int secondary_list_length(SecondaryNode* head);

char* generate_key(char* word);

void insert_word(char* word, PrimaryNode** head);
void insert_word_into_secondary(char* word, SecondaryNode** head);

void print_list(PrimaryNode* head);

#endif
