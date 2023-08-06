!    -*- f90 -*-
! -*- coding: utf-8 -*-
! written by Ralf Biehl at the Forschungszentrum Juelich ,
! Juelich Center for Neutron Science 1 and Institute of Complex Systems 1
!    jscatter is a program to read, analyse and plot data
!    Copyright (C) 2018  Ralf Biehl
!
!    This program is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    This program is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with this program.  If not, see <http://www.gnu.org/licenses/>.
!

! f2py -c fscatter.f95 -m fscatter


module cloud
    use typesandconstants
    use utils
    use QSHEP3D_MOD
    !$ use omp_lib
    implicit none

contains

    function ffx(qx,r,fa,rms) result(Sq)
        ! calculates  scattering intensity I=F*conjg(F)
        ! in direction point
        ! adds rms random displacements to positions r

        ! point on unit sphere 3 x 1, scattering amplitude, positions Nx3 , rms
        real(dp), intent(in) :: qx(3), fa(:), r(:,:), rms
        ! scattering  formfactor Sq
        real(dp)             :: Sq, rr(size(r,1),3)

        ! local variables
        complex(dp) :: iqr(size(r,1)), Fq

        rr = 0._dp
        iqr = jzero
        Fq = jzero
        Sq = 0._dp

        if (rms>0) then
            rr=r+random_gauss(size(r,1),3)*rms
            iqr= j1 * matmul(rr,qx)
        else
            iqr= j1 * matmul( r,qx)
        end if
        Fq = sum( fa* exp(iqr) )
        Sq = REALPART(Fq*conjg( Fq ) )

    end function ffx

    function ffxa(qx,r,fa,rms) result(Sq)
        ! calculates  scattering intensity I=F*conjg(F) and F
        ! in direction point
        ! adds rms random displacements to positions r

        ! point on unit sphere 3 x 1, scattering amplitude, positions , rms
        real(dp), intent(in) :: qx(3), fa, r(:,:), rms
        ! scattering  formfactor Sq
        real(dp)             :: Sq(2), rr(size(r,1),3)

        ! local variables
        complex(dp) :: iqr(size(r,1)), Fq

        if (rms>0) then
            rr=r+random_gauss(size(r,1),3)*rms
            iqr= j1 * matmul(rr,qx)
        else
            iqr= j1 * matmul( r,qx)
        end if

        Fq= sum( fa* exp(iqr) )
        Sq(1)=REALPART(Fq*conjg( Fq ) )
        Sq(2)=REALPART(Fq)

    end function ffxa

    function ffq(point,r,q,blength,iff,formfactor,rms,ffpolydispersity) result(res)
        ! calculates  scattering amplitude F and scattering intensity I=F*conjg(F)
        ! in direction point
        ! scales formfactor for polydispersity and adds rms random displacements to positions r

        ! one point point on unit sphere 3 x 1
        real(dp), intent(in) :: point(:)
        ! wavevector scalar
        real(8), intent(in) :: q
        ! positions N x 3, scattering length xN
        real(dp), intent(in) :: r(:,:) , blength(:)
        ! indices formfactor
        integer, intent(in)     :: iff(:)
        ! formfactor ixN
        real(dp), intent(in) :: formfactor(:,:)
        ! root mean square displacements, polydispersity sigma
        real(dp), intent(in) :: rms, ffpolydispersity
        ! return value with q, formfactor F*f.conjg, scattering amplitude F
        real(dp),dimension(3) :: res

        ! local variables
        real(dp)    :: sizerms(size(r,1)), volrmsfactor(size(r,1)), fa(size(r,1)), fai(size(formfactor,2)-1)
        real(dp)    :: qx(3), rg(size(r,1),3), rg1(size(r,1),1) !, rr(size(r,1),3)
        complex(dp) :: iqr(size(r,1))
        complex(dp) :: Fq
        integer     :: i

        Fq=0*j1
        iqr=0*j1
        rg1=0_dp
        qx=0_dp
        rg=0_dp
        res=0_dp
        sizerms=0_dp
        volrmsfactor=0_dp
        fa=0_dp
        fai=0_dp

        if (ffpolydispersity>0) then
            ! normal distribution of size factor
            rg1=random_gauss(size(r,1),1)
            sizerms = rg1(:,1) * ffpolydispersity + 1_dp
            ! corresponding relative volume change
            where( sizerms <= 0._dp )  sizerms=0._dp
            volrmsfactor=sizerms**3
            ! interpolate with rms
            do i =1,size(r,1)
                fa(i) = blength(i) * volrmsfactor(i) * interp_s(sizerms(i)*q, formfactor(1,:), formfactor(iff(i)+1,:))
            end do
        else
            ! interpolate
            do i =1,size(fai)
                fai(i) = interp_s(q, formfactor(1,:), formfactor(i+1,:))
            end do
            ! distribute according to iff
            do i =1,size(fa,1)
                fa(i)=blength(i)*fai(iff(i))
            end do
        endif

        qx=q*point
        if (rms>0) then
            rg=random_gauss(size(r,1),3)*rms
            iqr= j1 * matmul(r+rg,qx)
        else
            iqr= j1 * matmul(r   ,qx)
        end if

        Fq= sum( fa* exp(iqr) )
        res(1)=q
        res(2)=REALPART(Fq*conjg( Fq ))
        res(3)=REALPART(Fq)

    end function ffq

    function sphereaverage_ffq(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average for ffq as orientational average on points distributed on unit sphere
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        real(dp), intent(in)    :: relError
        integer, intent(in)     :: iff(:)
        real(dp)                :: sphave(3)

        if (relError >1) then
            sphave=sphereaverage_ffqfib(q,r,blength,iff,formfactor,rms,ffpolydispersity, int(relError))
        else
            sphave=sphereaverage_ffq_pseudrand(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError)
        end if
    end function sphereaverage_ffq

    function sphereaverage_ffq_pseudrand(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average  by pseudo random numbers on unit sphere
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        real(dp), intent(in)    :: relError
        integer, intent(in)     :: iff(:)
        integer                 :: i,npoints
        integer, parameter      :: steps =20
        real(dp)                :: points(steps,3),qsph(steps,3),sphave(3),result(3),mean(3),prevmean(3)

        ! initialisation
        result=0
        npoints=0

        ! first iteration
        qsph=randompointsonsphere(steps, 0, 1.0_dp)
        points=rphitheta2xyz(qsph)
        do i=1,size(points,1)
            result=result+ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
            npoints=npoints+1
        end do
        prevmean=result/npoints

        ! increase randompoints until error is small enough
        do
            qsph=randompointsonsphere(steps, npoints, 1.0_dp)
            points=rphitheta2xyz(qsph)
            do i=1,size(points,1)
                result=result+ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
                npoints=npoints+1
            end do
            mean=result/npoints
            ! test if error is smaller to break
            if ((abs(mean(2)-prevmean(2))  < relError*abs(mean(2)))  .AND. &
                (abs(mean(3)-prevmean(3))  < relError*abs(mean(3)))) then
                exit
            end if
            prevmean = mean
        end do

        ! return result
        sphave(1)=q
        ! calc averages
        sphave(2)=mean(2)
        sphave(3)=mean(3)

    end function sphereaverage_ffq_pseudrand

    function sphereaverage_ffqfib(q,r,blength,iff,formfactor,rms,ffpolydispersity, relError) result(sphave)
        ! sphere average as average on fibonacci lattice for ffq
        ! returns mean

        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:),rms, ffpolydispersity
        integer, intent(in)     :: relError
        integer, intent(in)     :: iff(:)
        real(dp)                :: qfib(2*relError+1,3),points(2*relError+1,3),sphave(3),results(2*relError+1,3)
        integer                 :: i

        ! create Fibonacci lattice on unit sphere
        qfib=fibonacciLatticePointsOnSphere(relError,1.0_dp)
        ! to cartesian coordinates
        points=rphitheta2xyz(qfib)    ! to cartesian
        results=0
        ! for all points
        do i=1,size(points,1)
            results(i,:) = ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
        end do
        sphave(1)=q
        ! calc averages
        sphave(2)=sum(results(:,2), 1)/size(results,1)
        sphave(3)=sum(results(:,3), 1)/size(results,1)

    end function sphereaverage_ffqfib

    function average_ffqxyz(q,r,blength,iff,formfactor,rms,ffpolydispersity,points) result(ave)
        ! average ffq on explicit given list of points on unit sphere in cartesian coordinates
        ! returns mean

        ! scattering vector, positions, blength, formfactor, points to average
        real(dp), intent(in)    :: q, r(:,:), blength(:), formfactor(:,:), points(:,:)
        real(dp), intent(in)    :: rms, ffpolydispersity
        integer, intent(in)     :: iff(:)
        real(dp)                :: ave(3),fq(3)
        integer                 :: i

        fq=0
        ave=0
        ! for all points
        do i=1,size(points,1)
            fq=ffq(points(i,:),r,q,blength,iff,formfactor,rms,ffpolydispersity)
            ave(2) = ave(2) + fq(2)
            ave(3) = ave(3) + fq(3)
        end do
        ave(1)=q
        ! calc averages
        ave(2)=ave(2)/size(points,1)
        ave(3)=ave(3)/size(points,1)

    end function average_ffqxyz

    function average_ffqrpt(q,r,blength,iff,formfactor,rms,ffpolydispersity,points) result(ave)
        ! average ffq on explicit given list of points on unit sphere in sperical coordinates for list of q
        ! returns mean

        ! scattering scalar N, positions Nx3, blength N, formfactor Nx?, points to average
        real(dp), intent(in)    :: q(:), r(:,:), blength(:), formfactor(:,:), points(:,:)
        ! rms 1, polydispersity 1
        real(dp), intent(in)    :: rms, ffpolydispersity
        ! index in formfactor N
        integer, intent(in)     :: iff(:)
        real(dp)                :: ave(size(q,1),3), xyz(size(points,1),3)
        integer                 :: i

        ! to cartesian coordinates
        xyz=rphitheta2xyz(points)    ! to cartesian
        do i=1,size(q, 1)
            ave(i,:) = average_ffqxyz(q(i),r,blength,iff,formfactor,rms,ffpolydispersity,xyz)
        end do

    end function average_ffqrpt

    function scattering_Debye(q,r,blength,iff,formfactor,ncpu)  result(qsq)
    ! Debye equation  definition as in _scattering

        ! scattering vector
        real(dp), intent(in)    :: q(:), blength(:)
        ! formfactor ixN, positions
        real(dp), intent(in)    :: formfactor(:,:),r(:,:)
        ! number of cores (negative = not used cores), indices formfactor
        integer, intent(in)     :: ncpu,iff(:)
        integer                 :: k
        ! return value with q, Sq
        real(dp)                :: qsq(2,size(q,1))
        ! num of threads
        integer                 :: num_threads

        num_threads=omp_get_num_procs()
        if (ncpu<0) then
            num_threads=max(num_threads+ncpu,1)
        else if (ncpu>0) then
            num_threads=min(ncpu,num_threads)
        end if
        call omp_set_num_threads(num_threads)

        !$omp parallel do
        do k = 1,size(q,1)
            qsq(:,k)=scattering_Debye_q(q(k),r,blength,iff,formfactor)
        end do
        !$omp end parallel do

    end function scattering_Debye

    function scattering_Debye_q(q,r,blength,iff,formfactor)  result(qsq)
    ! Debye equation  for one q

        ! scattering vector, blength,formfactor ixN, positions
        real(dp), intent(in)    :: q, blength(:),formfactor(:,:),r(:,:)
        ! indices formfactor
        integer, intent(in)     :: iff(:)
        integer                 :: i,j,k
        ! return value with q, Sq
        real(dp)                :: qsq(2),qrij,sq,fa(size(formfactor,2)-1)

        qrij=0
        qsq(1)=q
        qsq(2)=0
        sq=0
        if (q==0) then
            qsq(2)=sum(blength)**2
        else
            do k =1,size(formfactor,2)-1
                fa(k) = interp_s(q, formfactor(1,:), formfactor(k+1,:))
            end do
            do i =1,size(r,1)
                do j=i+1,size(r,1)
                    qrij=q*sqrt(sum((r(i,:)-r(j,:))**2))
                    sq= sq + 2*blength(i)*fa(iff(i))*blength(j)*fa(iff(j))*sin(qrij)/qrij
                end do
                sq= sq + blength(i)**2 * fa(iff(i))**2
            end do
            qsq(2)=sq
        end if
    end function scattering_Debye_q

    function mosaicAverage3D_single(qxzw, r, blength, formfactoramp, psi, phi, theta, mosaic, rms, dorient, &
                            &n, x, y, z, f, nr, lcell, lnext, xyzmin, xyzdel, rmax, rsq, a)  result(qsq)
        ! 3D scattering using a 3D formfactoramplitude of particles
        ! uses inverse distance weighting (Shepard's method) as modified from Renka (see toms661.f90)
        ! to interpolate the 3D formfactor

        ! scattering vectors Nx3, blength N , formfactor 4xN
        real(dp), intent(in)     :: qxzw(:,:), blength(:), formfactoramp(:,:)
        ! positions Nx3, orientation angles phi N, theta N, rms, dorient
        real(dp), intent(in)     :: r(:,:), psi(:), phi(:), theta(:), rms, dorient
        ! mosaic orientation x3 to rotate qxzw as rot vector with norm as angle in rad
        real(dp), intent(in)     :: mosaic(3)

        ! interpolation input nodes
        real(dp), intent(in)     :: x(:), y(:), z(:), f(:)
        ! interplation cells and next nodes indices, number of points, number of rows in the cell
        integer(4), intent(in)   :: lcell(:,:,:),lnext(:), n, nr
        ! interpolation output minimum nodal coordinates and cell dimensions, squares of the radii r(k)
        real(dp), intent(in)     :: xyzmin(3), xyzdel(3), rmax, rsq(:)
        ! coefficients for quadratic nodal function Q(K) in column K, interpolated fa
        real(dp) , intent(in)    :: a(:, :)

        ! locals
        integer(4)               :: i, j
        integer(4)               :: xyz(3) = (/1,2,3/)  ! Euler rotation order
        ! rotation vector i in rpt coordinates, rotation matrix, , rotated qxzw
        real(dp)                 :: rot(3,3)
        real(dp)                 :: qrot(3), qxzwf(size(qxzw,1),3), dr(size(r,1),size(r,2)), dor(size(r,1),3)
        ! interpolated fa
        real(dp)                 :: fa(size(r,1))
        ! return value with q, Sq
        real(dp)                 :: qsq(size(qxzw,1))

        ! init
        qsq = 0._dp
        rot = 0._dp
        qrot = 0._dp

        ! rotate all qxzw by single mosaic orientation
        if (sum(abs(mosaic)) > 0.0_dp)  then
            rot = rotationmatrix(mosaic, sqrt(sum(mosaic**2)))
            qxzwf =  transpose(matmul(transpose(rot), transpose(qxzw)))
        else
            ! rotation is diagonal
            qxzwf = qxzw
        end if

        !  add common rms displament to positions and dorient for angles for all qxzwf
        ! this reduces noise for individual qxzwf
        dr = r + random_gauss(size(r,1),size(r,2)) * rms
        dor = random_gauss(size(phi,1),3)*dorient

        ! for all points and calc fa
        do i=1,size(qxzwf,1)
            fa=0._dp
            ! loop over particles to interpolate fa with correct orientation phi,theta
            do j=1,size(r,1)
                ! get rotation matrix to current psi,phi,theta angles
                ! rotation matrix 3x3  but transpose as we rotate q instead of f(xyz)
                rot = transpose(eulerrotationmatrix(xyz, psi(j) + dor(j,1), phi(j)+ dor(j,2), theta(j)+ dor(j,3)))
                ! rotate qxzw(i) and calc fa(j)
                qrot = matmul(rot,qxzwf(i,:))
                fa(j) = QS3VAL( qrot(1), qrot(2), qrot(3), n,x,y,z,f,nr,lcell,lnext,xyzmin,xyzdel,rmax,rsq,a)
            end do
            ! no rms
            qsq(i) = ffx(qxzwf(i,:), dr, blength*fa, 0.0_dp)
        end do

    end function mosaicAverage3D_single

    function mosaicAverage3D(qxzw, mosaic, r, blength, formfactoramp, nr, psi, phi, theta, rms, dorient, ncpu)  result(qsq)
        ! 3D scattering using a 3D formfactoramplitude of particles
        ! uses inverse distance weighting (Shepard's method) as modified from Renka (see toms661.f90)
        ! to interpolate the 3D formfactor
        ! mosaic rotation vectors define define set of orientations to average over (rotate r )

        ! scattering vectors Nx3, mosaic rotation vectors Nx4 to average over, blength N , formfactor 4xN
        real(dp), intent(in)     :: qxzw(:,:),  mosaic(:,:), blength(:), formfactoramp(:,:)
        ! positions Nx3, orientation angles psi N, phi N, theta N, rms, dorient
        real(dp), intent(in)     :: r(:,:), psi(:), phi(:), theta(:), rms, dorient
        ! ncpu, number of rows, columns, and planes in the cell grid =(n/3)**0.333
        integer(4), intent(in)   :: ncpu, nr
        integer(4)               :: n, nq=17, nw=32

        ! locals
        integer(4)               :: i, j, ier

        ! interpolation input nodes
        real(dp)                 :: x(size(formfactoramp,2)),y(size(formfactoramp,2)),z(size(formfactoramp,2))
        real(dp)                 :: f(size(formfactoramp,2)), fa0
        ! interplation cells and next nodes indices
        integer(4)               :: lcell(nr,nr,nr)
        integer(4)               :: lnext(size(formfactoramp,2))
        ! interpolation output minimum nodal coordinates and cell dimensions, squares of the radii r(k)
        real(dp)                 :: xyzmin(3), xyzdel(3), rmax, rsq(size(formfactoramp,2))
        ! coefficients for quadratic nodal function Q(K) in column K, interpolated fa
        real(dp)                 :: a(9,size(formfactoramp,2))

        ! return value with q, Sq
        real(dp)                 :: qsq(size(qxzw,1)), temp(size(qxzw,1))

        ! num of threads
        integer                  :: num_threads
        num_threads=omp_get_num_procs()
        if (ncpu<0) then
            num_threads=max(num_threads+ncpu,1)
        else if (ncpu>0) then
            num_threads=min(ncpu,num_threads)
        end if
        call omp_set_num_threads(num_threads)

        ! init
        n=int(size(formfactoramp,2),4)
        x=formfactoramp(1,:)
        y=formfactoramp(2,:)
        z=formfactoramp(3,:)
        f=formfactoramp(4,:)
        qsq = 0._dp

        ! QSHEP3 precalcs arrays to efficient do 3D lin interpolation
        ! init formfactoramp for interpolation to get coefficients a,lcell, lnext,....
        call QSHEP3 ( n, x, y, z, f, nq, nw, nr, lcell, lnext, xyzmin, xyzdel, rmax, rsq, a, ier )
        if (ier > 0) then
            ! test if QSHEP3 failed
            qsq(:) = -ier
            stop -1
        end if

        ! loop over all points in cone to do orientational average in cone
        !$omp parallel do private(temp)
        do i=1,size(mosaic,1)
            temp = mosaicAverage3D_single(qxzw, r, blength, formfactoramp, psi, phi, theta, mosaic(i,:3),rms, dorient, &
                                        &n, x, y, z, f, nr, lcell, lnext, xyzmin, xyzdel, rmax, rsq, a)
            !$omp critical
            qsq = qsq + temp * mosaic(i,4)
            !$omp end critical
        end do
        !$omp end parallel do

        ! get q=(0,0,0) to normalize
        fa0 = QS3VAL( 0._dp, 0._dp, 0._dp, n,x,y,z,f,nr,lcell,lnext,xyzmin,xyzdel,rmax,rsq,a)

        ! finally normalize
        qsq = qsq / sum(mosaic(:,4))/ fa0**2

    end function mosaicAverage3D

    function mosaicAverage(qxzw, mosaic, r, blength, iff, formfactoramp, rms, ncpu)  result(qsq)
        ! 3D scattering using a 1D formfactoramplitude of particles
        ! linear interpolation of formfactor
        ! mosaic are rotation vectors defining set of orientations to average over (rotate r)
        ! rotation vectors with angle=norm(v(:3)) , rot_vector= v(:3)/norm(v(:3)), probability v(4)

        ! scattering vectors Nx3, mosaic rotation vectors Nx4 to average over, blength N , formfactor 4xN
        real(dp), intent(in)     :: qxzw(:,:),  mosaic(:,:), blength(:), formfactoramp(:,:)
        ! positions Nx3, rms
        real(dp), intent(in)     :: r(:,:), rms
        ! ncpu, index formfactor
        integer(4), intent(in)   :: ncpu, iff(:)

        ! locals
        integer(4)               :: i, j
        ! rotation vector i in rpt coordinates, rotation matrix, rotated qxzw, q scalar
        real(dp)                 :: rot(3,3), qxzwf(size(qxzw,1),3), qnorm(3) ,q, temp(3), dr(size(r,1),size(r,2))
        real(dp)                 :: ffpolydispersity = 0._dp

        ! return value with q, Sq
        real(dp)                 :: qsq(size(qxzw,1),2)

        ! num of threads
        integer                  :: num_threads
        num_threads=omp_get_num_procs()
        if (ncpu<0) then
            num_threads=max(num_threads+ncpu,1)
        else if (ncpu>0) then
            num_threads=min(ncpu,num_threads)
        end if
        call omp_set_num_threads(num_threads)

        ! init
        qsq = 0._dp
        temp = 0._dp

        ! loop over all points in cone to do orientational average in cone
        do i=1,size(mosaic,1)
            ! rotate all qxzw by single mosaic orientation
            ! as we rotate q instead of r we use transposed rot matrix
            if (sum(abs(mosaic(i,:3))) > 0.0_dp)  then
                rot = rotationmatrix(mosaic(i,:3), sqrt(sum(mosaic(i,:3)**2)))
                qxzwf =  transpose(matmul(transpose(rot), transpose(qxzw)))
            else
                ! rotation is diagonal
                qxzwf = qxzw
            end if

            !  add common rms displament to positions for all qxzwf
            ! this reduces noise for individual qxzwf
            dr= r + random_gauss(size(r,1),size(r,2))*rms

            ! for all q points
            !$omp parallel do private(temp, q, qnorm)
            do j=1,size(qxzwf,1)
                ! abs value of q
                q = sqrt(sum(qxzwf(j,:)**2))
                ! we need  normalized qxzwf and ake only the Sq return value in (2)
                if (q>0) then
                    qnorm = qxzwf(j,:) / q
                else
                    qnorm = 1._dp
                end if
                temp = ffq(qnorm, dr, q, blength, iff, formfactoramp, 0._dp, ffpolydispersity)
                !$omp critical
                qsq(j,:) = qsq(j,:) +  temp(2:) * mosaic(i,4)
                !$omp end critical
            end do
            !$omp end parallel do

        end do

        ! finally normalize
        qsq = qsq / sum(mosaic(:,4))

    end function mosaicAverage

end module cloud
