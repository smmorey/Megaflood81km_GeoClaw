! qinit routine for initializing lake into solution, q
! polygon METHOD (with 3 points)
subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)

    use geoclaw_module, only: grav

    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! Lake Height
    real(kind=8), parameter :: h = 3088.d0	

    ! Box 1 
    real(kind=8), parameter :: b1_x0 = 93.0d0
    real(kind=8), parameter :: b1_x1 = 93.53d0
    real(kind=8), parameter :: b1_y0 = 28.94d0
    real(kind=8), parameter :: b1_y1 = 29.23d0
    ! Box 2 
    real(kind=8), parameter :: b2_x0 = 93.53d0
    real(kind=8), parameter :: b2_x1 = 94.3d0
    real(kind=8), parameter :: b2_y0 = 29.05d0
    real(kind=8), parameter :: b2_y1 = 29.31d0
    ! Box 3 
    real(kind=8), parameter :: b3_x0 = 94.3d0
    real(kind=8), parameter :: b3_x1 = 94.49d0
    real(kind=8), parameter :: b3_y0 = 29.23d0
    real(kind=8), parameter :: b3_y1 = 29.4d0
    ! Box 4 (Contains Dam)   
    real(kind=8), parameter :: b4_x0 = 94.33d0
    real(kind=8), parameter :: b4_x1 = 94.96d0
    real(kind=8), parameter :: b4_y0 = 29.4d0
    real(kind=8), parameter :: b4_y1 = 29.6d0
    ! Box 5   
    real(kind=8), parameter :: b5_x0 = 94.02d0
    real(kind=8), parameter :: b5_x1 = 94.46d0
    real(kind=8), parameter :: b5_y0 = 29.6d0
    real(kind=8), parameter :: b5_y1 = 29.78d0
    
    ! Other storage
    integer :: i,j
    real(kind=8) :: x,y

    do i=1-mbc,mx+mbc
        x = xlower + (i - 0.5d0)*dx
        do j=1-mbc,my+mbc
            y = ylower + (j - 0.5d0)*dy
	    !Fill boxes
	    if ((x>b1_x0).and.(x<b1_x1).and.(y>b1_y0).and.(y<b1_y1)) then
                q(1,i,j) = max(0.d0,(h - aux(1,i,j))) 
	    else if ((x>b2_x0).and.(x<b2_x1).and.(y>b2_y0).and.(y<b2_y1)) then
	        q(1,i,j) = max(0.d0,(h - aux(1,i,j)))
	    else if ((x>b3_x0).and.(x<b3_x1).and.(y>b3_y0).and.(y<b3_y1)) then
	        q(1,i,j) = max(0.d0,(h - aux(1,i,j)))
	    else if ((x>b4_x0).and.(x<b4_x1).and.(y>b4_y0).and.(y<b4_y1)) then
	        q(1,i,j) = max(0.d0,(h - aux(1,i,j)))
	    else if ((x>b5_x0).and.(x<b5_x1).and.(y>b5_y0).and.(y<b5_y1)) then
	        q(1,i,j) = max(0.d0,(h - aux(1,i,j)))
            else
		q(1,i,j) = 0.d0
	    endif
        enddo
    enddo
    
end subroutine qinit
