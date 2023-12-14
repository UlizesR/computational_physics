// ========================================================= 
// Program to compute roots of a 2nd order polynomial
// Tasks: Input from user , logical statements ,
// use of functions , exit
// Tests:
// a,b,c=123        D= −8
// a,b,c= 1 −8 16   D= 0        x1= 4
// a,b,c= 1 −1 −2   D= 9.       x1= 2. x2= −1. 
// a,b,c= 2.3 −2.99 −16.422     x1= 3.4 x2= −2.1
// =========================================================
 
#include <iostream>
#include <cstdlib>
#include <cmath>

double Discriminant(double a, double b, double c);
void Roots(double a, double b, double c, double &x1, double &x2);

int main()
{
    double a, b, c, D;
    double x1, x2;

    std::cout << "Enter a, b, c: ";
    std::cin >> a >> b >> c;
    std::cout << "a = " << a << " b = " << b << " c = " << c << "\n";

    // Test i f we have a well defined polynomial of 2nd degree
    if (a == 0.0)
    {
        std::cout << "a = 0. Not a 2nd degree polynomial\n";
        exit(1);
    }

    // Compute the discriminant
    D = Discriminant(a, b, c);
    std::cout << "Discriminant: D = " << D << "\n";

    // Compute the roots
    if (D > 0.0)
    {
        Roots(a, b, c, x1, x2);
        std::cout << "Roots: x1 = " << x1 << " x2 = " << x2 << "\n";
    }
    else if (D == 0.0)
    {
        Roots(a, b, c, x1, x2);
        std::cout << "Double Root: x1 = " << x1 << "\n";
    }
    else
    {
        std::cout << "No real roots\n";
        std::exit(1);
    }

    return 0;
}

// =========================================================
// This is the function that computes the discriminant
// =========================================================
double Discriminant(double a, double b, double c)
{
    return b * b - 4 * a * c;
}

// =========================================================
// This is the function that computes the roots
// =========================================================
void Roots(double a, double b, double c, double &x1, double &x2)
{
    double D = Discriminant(a, b, c);

    if (D >= 0.0)
    {
        x1 = (-b + std::sqrt(D)) / (2 * a);
        x2 = (-b - std::sqrt(D)) / (2 * a);
    }
    else
    {
        std::cout << "No real roots\n";
        std::exit(1);
    }
}