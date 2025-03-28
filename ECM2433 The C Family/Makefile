CC = gcc
CFLAGS = -ansi

wordlengths: wordlengths.o histogram.o
	$(CC) $(CFLAGS) -o wordlengths wordlengths.o histogram.o

demo_histogram: demo_histogram.o histogram.o
	$(CC) $(CFLAGS) -o demo_histogram demo_histogram.o histogram.o

anagram: anagram.o histogram.o
	$(CC) $(CFLAGS) -o anagram anagram.o histogram.o -lm

anaquery: anaquery.o anagram.o
	$(CC) $(CFLAGS) -o anaquery anaquery.o anagram.o -lm

patience: patience.o shuffle.o
	$(CC) $(CFLAGS) -o patience patience.o shuffle.o -lgsl -lgslcblas -lm

pstatistics: pstatistics.o patience.o shuffle.o histogram.o
	$(CC) $(CFLAGS) -o pstatistics pstatistics.o patience.o shuffle.o histogram.o -lgsl -lgslcblas -lm

histogram.o: histogram.c histogram.h
wordlengths.o: wordlengths.c
demo_histogram.o: demo_histogram.c
anagram.o: anagram.c anagram.h
anaquery.o: anaquery.c
shuffle.o:  shuffle.c shuffle.h
patience.o: patience.c patience.h
pstatistics.o: pstatistics.c

clean:
	rm -f histogram.o wordlengths.o demo_histogram.o anagram.o anaquery.o shuffle.o patience.o pstatistics.o

rm_execs:
	rm -f wordlengths demo_histogram anagram anaquery patience pstatistics

all:
	make wordlengths
	make demo_histogram
	# make anagram
	make anaquery
	# make patience
	make pstatistics
