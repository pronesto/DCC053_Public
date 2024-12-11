#include <iostream>

class List {
private:
    int elements[100];
    int size;

public:
    List() : size(0) {}

    void add(int element) {
        if (size < 100) {
            elements[size++] = element;
        }
    }

    int getSize() const {
        return size;
    }
};

// Main function
int main() {
    List myList;
    myList.add(1);
    myList.add(2);
    myList.add(3);
    std::cout << "Size: " << myList.getSize() << std::endl;
    return 0;
}

