#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node{
    int data;
    struct node *next;
} node;

#define NODE_INITIALIZER {0, NULL}

void add_data(node *l, int d)
{
    node *p = (node *) malloc (sizeof(node));
    memset(p, 0, sizeof(node));
    p->data = d;
    p->next = l->next;
    l->next = p;
}

void print_list(node *l)
{
    node *p = l->next;
    int is_first = 1;
    while(p != NULL) {
        if (!is_first) printf(" ");
        is_first = 0;
        printf("%d", p->data);
        p = p->next;
    }
}

int main()
{
    node l = NODE_INITIALIZER;
    int i = 100;
    while(i--) {
        int d = rand() % 100;
        printf("Generated: %d\n", d);
        add_data(&l, d);
    }

    print_list(&l);
}
