#include <stdio.h>
#include <stdlib.h>

// Base "Animal" structure
typedef struct Animal {
  unsigned short age;

  // Method pointers
  void (*inc_age)(struct Animal* this);
  unsigned short (*get_age)(struct Animal* this);
} Animal;

// Base "Animal" structure
typedef struct Elf {
  unsigned short age;

  // Method pointers
  void (*inc_age)(struct Animal* this);
  unsigned short (*get_age)(struct Animal* this);

  char* name;

  // More method pointers:
  void (*set_name)(struct Elf* this, char* name);
} Elf;

// Base "Animal" methods
void animal_inc_age(Animal* this) {
  this->age++;
}

unsigned short animal_get_age(Animal* this) {
  return this->age;
}

// "Elf" methods
void elf_inc_age(Animal* this) {
  // Well, elves live much longer...
  this->age += 7;
}

// "Elf" methods
void elf_set_name(Elf* this, char* name) {
  // Well, elves live much longer...
  this->name = name;
}

// Constructor for "Animal"
Animal* new_animal(unsigned short age) {
  Animal* a = (Animal*)malloc(sizeof(Animal));
  a->age = age;
  a->inc_age = animal_inc_age;
  a->get_age = animal_get_age;
  return a;
}

// Constructor for "Elf"
Elf* new_elf(unsigned short age, char* name) {
  Elf* a = (Elf*)malloc(sizeof(Elf));
  a->age = age;
  a->inc_age = elf_inc_age;
  a->get_age = animal_get_age;
  a->name = name;
  a->set_name = elf_set_name;
  return a;
}

int main() {
  // Create an Animal
  Animal* a = new_animal(5);
  printf("Animal's initial age: %u\n", a->get_age(a));
  a->inc_age(a);
  printf("Animal's age after increment: %u\n", a->get_age(a));

  // Create an Elf
  Animal* ae = (Animal*)new_elf(100, "Celebrimbor");
  printf("Elf's initial age: %u\n", ae->get_age(ae));
  ae->inc_age((Animal*)ae);
  printf("Elf's age after increment: %u\n", ae->get_age(ae));

  // Create an Elf whose "static type" is Animal:
  Elf* e = new_elf(50, "Celebrimbor");
  printf("Animal/elf's initial age: %u\n", e->get_age(e));
  ae->inc_age(ae);
  printf("Animal/elf's age after increment: %u\n", e->get_age(e));

  // Cleanup
  free(a);
  free(e);
  free(ae);

  return 0;
}
