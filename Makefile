all: cut_dups

cut_dups: cut_dups.c
	gcc -g -Wall -Werror -Wextra -Wpedantic -O0 -o $@ $<
