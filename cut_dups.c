#include "stdio.h"
#include "stdlib.h"
#include "string.h"

void index_cols(size_t largest_col_to_keep, size_t *col_indices, size_t *col_widths, char *line, ssize_t nread) {
    size_t indices_counted = 0;
    size_t pos = 0;
    col_indices[0] = 0;
    
    while(indices_counted <= largest_col_to_keep) {
        if (pos > (size_t) nread) {
            fputs("too few columns!", stderr);
            exit(1);
        }
        if (line[pos] == '\t' || line[pos] == '\n') {
            col_widths[indices_counted] = pos - col_indices[indices_counted];
            indices_counted++;
            col_indices[indices_counted] = pos+1;
        }
        pos++;
    }
}

void print_cols(char *line, size_t *col_indices, size_t *col_widths, size_t ncols_to_keep, size_t *cols_to_keep) {
    for (size_t keep_index=0; keep_index<ncols_to_keep; keep_index++) {
        size_t keep_col = cols_to_keep[keep_index];
        char *print_pos = line + col_indices[keep_col];
        int print_width = (int) col_widths[keep_col];
        if (keep_index == 0) {
            printf("%.*s", print_width, print_pos);
        } else {
            printf("\t%.*s", print_width, print_pos);
        }
    }
    printf("\n");
}

void keep_cols(size_t *cols_to_keep, size_t ncols_to_keep, size_t largest_col_to_keep) {
    size_t *col_indices = malloc(sizeof(size_t)*(largest_col_to_keep + 2));
    size_t *col_widths = malloc(sizeof(size_t)*(largest_col_to_keep + 1));
    if (col_indices == NULL || col_widths == NULL) {
        fputs("malloc failed!", stderr);
        exit(1);
    }
    char *line = NULL;
    size_t len = 0;
    ssize_t nread = 0;
    
    while ((nread = getline(&line, &len, stdin)) != -1) {
        index_cols(largest_col_to_keep, col_indices, col_widths, line, nread);
        print_cols(line, col_indices, col_widths, ncols_to_keep, cols_to_keep);
    }
    free(col_indices);
    free(col_widths);
    free(line);
}

int main(int argc, char **argv) {
    size_t *cols_to_keep = malloc(sizeof(cols_to_keep) * argc);
    if (cols_to_keep == NULL) {
        fputs("malloc failed!", stderr);
        exit(1);
    }
    size_t ncols_to_keep = argc-1;
    size_t largest_col_to_keep = 0;
    for (size_t i=0; i<ncols_to_keep; i++) {
        cols_to_keep[i] = atoi(argv[i+1]);
        if (cols_to_keep[i] > largest_col_to_keep) {
            largest_col_to_keep = cols_to_keep[i];
        }
    }
    keep_cols(cols_to_keep, ncols_to_keep, largest_col_to_keep);
    free(cols_to_keep);
}
