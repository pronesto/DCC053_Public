/**
 * Quick and dirty experiment to demonstrate what restrictification does.
 * Date: September 14th, 2024
 */

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

void dot0(int a[], int b[], int r[], int size) {
	int i;
	for (i = 0; i < size; i++) {
		r[i] = a[i];
		if (!b[i])
			r[i] = b[i];
	}
}

void dot1(int *restrict a, int *restrict b, int *restrict r, int size) {
	int i;
	for (i = 0; i < size; i++) {
		r[i] = a[i];
		if (!b[i])
			r[i] = b[i];
	}
}

int sum_array(int a[], int size) {
	int sum = 0;
	int i;
	for (i = 0; i < size; i++) {
		sum += a[i];
	}
	return sum;
}

void init_array(int a[], int size) {
	int i;
	for (i = 0; i < size; i++) {
		a[i] = i%3;
	}
}

double run_experiment(int option, int* result, int *arr1, int *arr2, size_t size) {
	clock_t start, end;
	start = clock();
	if (option % 2 == 0) {
		dot0(arr1, arr2, result, size);
	} else {
		dot1(arr1, arr2, result, size);
	}
	end = clock();
  return ((double) (end - start)) / CLOCKS_PER_SEC;
}

int main(int argc, char** argv) {
	if (argc != 4) {
		fprintf(stderr, "Syntax: %s <size> <option> <num_exps>\n", argv[0]);
		exit(1);
	}
 
  // Read command-line arguments:
	size_t size = atoi(argv[1]);
	int option = atoi(argv[2]);
  char num_exps = atoi(argv[3]);

  // Initialize the arrays:
	int *arr1 = (int*)malloc(2 * sizeof(int) * size);
	int *arr2 = (int*)malloc(2 * sizeof(int) * size);
	int *result = (int*)malloc(sizeof(int) * size);
	init_array(arr1, size);
	init_array(arr2, size);
 
  // Print out options and set potential aliasing:
	if (option % 3) {
		fprintf(stderr, "Creating aliasing!\n");
		result = arr1;
	} else {
		fprintf(stderr, "No aliasing!\n");
	}
	if (option % 2 == 0) {
		printf("Without restrict\n");
	} else {
		printf("With restrict\n");
	}

  // Run the experiment. Discard the first result, though:
  run_experiment(option, result, arr1, arr2, size);
  double total_time = 0.0;
  for (char i = 0; i < num_exps; ++i) {
    double time = run_experiment(option, result, arr1, arr2, size);
    total_time += time;
    printf("%lf, ", time);
  }
	printf(", %lf, %d\n", total_time/num_exps, sum_array(result, size));
}
