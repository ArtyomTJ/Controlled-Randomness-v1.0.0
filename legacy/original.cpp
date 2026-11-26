// Original program, preserved for provenance.
//
// This is the implementation that started the Controlled Randomness
// project. It is kept verbatim (apart from this header) so that the
// historical record is exact. See docs/LEGACY.md for what it does and why
// the maintained implementation differs.
//
// Build (any C++ compiler):
//   g++ -std=c++17 -O2 -o original original.cpp
//
// The maintained implementation is in src/cpp/controlled_randomness.cpp.

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>

int main() {
    std::srand(std::time(nullptr)); // Инициализация генератора случайных чисел
    int c, d, a, b, i = 0, x, y;

    std::cout << "Введите два любых (оба положительных или оба отрицательных, и не 1) числа от -20 до 20: ";
    std::cin >> c >> d;

    if ((c == 1 || d == 1) || (c < -20 || c > 20) || (d < -20 || d > 20)) {
        std::cout << "Ошибка: числа должны быть в диапазоне от -20 до 20 и не равны 1." << std::endl;
        return 1;
    }

    std::cout << "Вы выбрали " << c << " " << d << std::endl;

    a = 1;
    b = 1;
    x = 1;
    y = 1;

    while (!(a == c && b == d)) {
        a = std::rand() % 41 - 20; // Генерация случайного числа от -20 до 20
        b = std::rand() % 41 - 20;
        i++;

        if ((c > 0 && d > 0)) { // Если оба числа положительные
            if ((x < 0 && y < 0 && a > 0 && b > 0) || 
                (x < 0 && y < 0 && ((a < 0 && b > 0) || (a > 0 && b < 0))) || 
                (a > 0 && b > 0 && ((x < 0 && y > 0) || (x > 0 && y < 0))) || 
                (((x < 0 && y > 0) || (x > 0 && y < 0)) && ((a < 0 && b > 0) || (a > 0 && b < 0))) || 
                (x == 0 || y == 0) || 
                (x == 0 && y == 0)) {
                x = a;
                y = b;
            }
            if ((x > 0 && y > 0 && a > 0 && b > 0) && 
                (std::abs(((c + d) / 2.0) - ((x + y) / 2.0)) > std::abs(((c + d) / 2.0) - ((a + b) / 2.0)))) {
                x = a;
                y = b;
            }
        } else { // Если оба числа отрицательные
            if ((x > 0 && y > 0 && a < 0 && b < 0) || 
                (x > 0 && y > 0 && ((a < 0 && b > 0) || (a > 0 && b < 0))) || 
                (a < 0 && b < 0 && ((x < 0 && y > 0) || (x > 0 && y < 0))) || 
                (((x < 0 && y > 0) || (x > 0 && y < 0)) && ((a < 0 && b > 0) || (a > 0 && b < 0))) || 
                (x == 0 || y == 0) || 
                (x == 0 && y == 0)) {
                x = a;
                y = b;
            }
            if ((x < 0 && y < 0 && a < 0 && b < 0) && 
                (std::abs(((std::abs(c) + std::abs(d)) / 2.0) - ((std::abs(x) + std::abs(y)) / 2.0)) > 
                 std::abs(((std::abs(c) + std::abs(d)) / 2.0) - ((std::abs(a) + std::abs(b)) / 2.0)))) {
                x = a;
                y = b;
            }
        }
    }

    std::cout << "i = " << i << std::endl;
    return 0;
}
