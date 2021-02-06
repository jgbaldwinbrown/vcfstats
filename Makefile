all: cut_dups

cut_dups: cut_dups.c
	gcc -Wall -Werror -Wextra -Wpedantic -O3 -o $@ $<
