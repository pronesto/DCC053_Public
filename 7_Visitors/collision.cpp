#include <iostream>

struct Object {};
struct Car: public Object {int x;};
struct Wall: public Object {int y;};

void _collide(Car* c, Car* w) {
  std::cout << "car" << " wall\n";
}

void _collide(Car* c, Wall* w) {
  std::cout << "car" << " wall\n";
}

void _collide(Wall* c, Car* w) {
  std::cout << "car" << " wall\n";
}

void _collide(Wall* c, Wall* w) {
  std::cout << "car" << " wall\n";
}

void collide(Object* o0, Object* o1) {
  std::cout << "Calling dispatch\n";
  _collide(o0, o1);
}

int main() {
  struct Object* o0 = new Car();
  struct Object* o1 = new Wall();
  collide(o0, o1);
}
