#include <iostream>

class MyString1 {
private:
    char* data;
    size_t length;

public:
    size_t getLength() const {
        return length;
    }
};

class MyString2 {
private:
    char* data;
    size_t length;

public:
    virtual size_t getLength() const {
        return length;
    }
};

int main() {
  MyString1 s1;
  MyString2 s2;
  std::cout << sizeof(s1) << std::endl;
  std::cout << sizeof(s2) << std::endl;
}
