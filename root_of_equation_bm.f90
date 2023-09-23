program bisection 
    implicit none
    real, external :: f
    real :: a, b, c
    print *, "Enter the interval [a,b] : "
    read *, a, b

10  c = (a+b)/2
     
    if (f(c) == 0) then 
        print *, "The root is : ", c
    else if (f(a) * f(c) .gt. 0) then
        a = c
        goto 10
    else 
        b = c
        goto 10
    end if
    
end program bisection

real function f(x)
    real :: x 
    f = 3*x -1
end 