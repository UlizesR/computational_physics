program newton_raphson 
    implicit none
    real :: x
    integer :: iteration 
    print *, "Enter the initial guess"
    read *, x
    call ntraph(x, iteration)
    print *, "The root is ", x


end program newton_raphson

real function f(x)
    real :: x
    f = 3*x**2 - 1
end 

real function df(x)
    real :: x
    df = 6*x
end

subroutine ntraph(x, iteration)
    implicit none   
    real, external :: f, df
    real :: error, x, tol
    integer :: iteration
    tol = 0.0000001
    iteration = 0
    10 error = -f(x)/df(x)
    x = x + error
    iteration = iteration + 1
    if (abs(error) .gt. tol) then
        goto 10
        print *, "Tolerance is ", tol
        print *, "Number of iterations is ", iteration
    end if
end 