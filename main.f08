program solve_diff_eq
  implicit none
  
  integer, parameter :: n = 1000 ! number of steps
  real, parameter :: t0 = 0.0, tf = 10.0 ! initial and final times
  real, parameter :: y0 = 1.0 ! initial condition
  real, parameter :: a = -0.5 ! coefficient in the differential equation
  
  real :: t, y, h
  integer :: i
  
  ! Step size
  h = (tf - t0) / n
  
  ! Initial values
  t = t0
  y = y0
  
  ! Output initial values
  print *, t, y
  
  ! Loop over time steps
  do i = 1, n
    ! Compute derivatives
    y = y + h * (a * y)
    
    ! Update time
    t = t + h
    
    ! Output values
    print *, t, y
  end do
end program solve_diff_eq