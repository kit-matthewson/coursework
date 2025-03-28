/*
  Shuffle function by Richard Everson from https://ele.exeter.ac.uk/mod/resource/view.php?id=3703540
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/*
 * Structure to hold a value to be shuffled and a random value that on which the values
 * will be sorted.
 */
struct pair
{
    int value;
    long rand;
};

int cmp(const void *a, const void *b)
{
    /* Compare pairs based on their random member */
    struct pair *ap = (struct pair *)a;
    struct pair *bp = (struct pair *)b;
    return ap->rand - bp->rand;
}

void shuffle(int *x, int n, int seed)
{
    /*
     * Shuffle the n elements of the integer array x in place.
     *
     * Parameters
     * ----------
     *
     * x : array of integers to be shuffled
     *
     * n : length of x
     *
     * seed : integer seed for the random number generator. If seed is a
     *        positive integer, the random number generator is initialised with
     *        that seed on the first call to shuffle; the seed is ignored on all
     *        other calls. If seed is negative, the generator is initialised
     *        with the time so different random number sequences and therefore
     *        shuffles are produced each time the program is run.
     */

    int j;
    struct pair pairs[n];

    /* Seed the random number generator */
    if (seed < 0)
        seed = time(NULL);
    srandom(seed);

    /* Build array of pairs */
    for (j = 0; j < n; j++) {
        pairs[j].value = x[j];
        pairs[j].rand = random();
    }

    /* Sort pairs array according to their rand element */
    qsort(pairs, n, sizeof(struct pair), cmp);

    /* Unpack values that are now in random order */
    for (j = 0; j < n; j++)
        x[j] = pairs[j].value;
    return;
}
