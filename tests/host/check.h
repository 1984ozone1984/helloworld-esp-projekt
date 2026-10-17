// Minimal host-tier assertions: print the failing expression, count failures.
#pragma once
#include <stdio.h>
#include <string.h>

static int check_failures;

#define CHECK(cond) do { if (!(cond)) { \
    printf("FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond); check_failures++; } } while (0)
#define CHECK_STR(got, want) do { if (strcmp((got), (want)) != 0) { \
    printf("FAIL %s:%d: got \"%s\" want \"%s\"\n", __FILE__, __LINE__, (got), (want)); \
    check_failures++; } } while (0)
#define CHECK_DONE() (printf("%s\n", check_failures ? "FAILED" : "ok"), check_failures != 0)
