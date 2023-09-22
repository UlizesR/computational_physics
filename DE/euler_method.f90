program euler 
    real, external :: f
    real :: x,y,h, xg
    integer :: n,i 
    print *, "Please enter the initial value of x"
    read *, x
    print *, "Please enter the initial value of y"
    read *, y
    print *, "Please enter the step size"
    read *, h
    print *, "Please enter the value of the given x"
    read *, xg
    n = int((xg-x)/h+0.5)

    do i=1,n 
        x = x + h
        y = y + h*f(x,y)
    end do
    print *, "The value of x and y are", x, y
end 

real function f(x,y)
real :: x,y
f=x+2*y 

end