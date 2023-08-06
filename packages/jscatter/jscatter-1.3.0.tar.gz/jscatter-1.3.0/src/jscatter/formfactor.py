# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015-2019  Ralf Biehl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

r"""
**Particle solution**

The scattering intensity of isotropic particles in solution with particle concentration :math:`c_p`
and structure factor :math:`S(q)` (:math:`S(q)=1` for non interacting particles) is

.. math:: I(q)= c_p I_p(q) S(s) = c_p I_0 F(q) S(q)

In this module the scattering intensity :math:`I_p(q)` of a single particle with
real scattering length densities is calculated in units :math:`nm^2=10^{-14} cm^2`.
For the structure factor :math:`S(q)` see :ref:`structurefactor (sf)`.

If the scattering length density is not defined as e.g. for beaucage model
the normalized particle form factor :math:`F(q)` with :math:`F(q=0)=1` is calculated.

Conversion of single particle scattering :math:`I_p(q)` to particle in solution
(units :math:`\frac{1}{cm}` with :math:`c` in mol/liter) is
:math:`I_{[1/cm]}(q)=N_A \frac{c_p}{1000} 10^{-14} I_{p,[nm^2]}(q)`.

**Particle formfactors**

The particle formfactor is  (:math:`\hat{F} ; normalized`)

.. math:: F(q) &= F_a(q)F^*_a(q)=|F_a(q)|^2 \\
          \hat{F}(q) &= \hat{F_a}(q)\hat{F^*_a}(q)=|\hat{F_a}(q)|^2

and particle scattering amplitude

.. math:: F_a(q) &= \int_V b(r) e^{iqr} \mathrm{d}r  = \sum_N b_i e^{iqr} \\
          \hat{F_a}(q) &= \int_V b(r) e^{iqr} \mathrm{d}r  / \int_V b(r) \mathrm{d}r  = \sum_N b_i e^{iqr}  / \sum_N b_i

The forward scattering per particle is (the later only for homogeneous particles)

.. math:: I_0=(\int_V b(r) \mathrm{d}r )^2= V_p^2(\rho_{particle}-\rho_{solvent})^2

Here :math:`V_p` is particle volume and :math:`\rho` is the average scattering length density.

For polymer like particles (e.g. Gaussian chain) of :math:`N` monomers with monomer partial volume
:math:`V_{monomer}` the particle volume is :math:`V_p=N V_{monomer}`.

The solution forward scattering :math:`c_pI_0` can be calculated from the monomer concentration as

.. math:: c_pI_0 = c_p V_p^2(\rho_{particle}-\rho_{solvent})^2 =
                  c_{monomer} N V_{monomer}^2(\rho_{monomer}-\rho_{solvent})^2



The scattering of **arbitrary shaped particles** can be calculated by :py:func:`~.cloudscattering.cloudScattering`
as a cloud of points representing the desired shape.

In the same way **distributions of particles** as e.g. clusters of particles or nanocrystals can be calculated.
Oriented scattering of e.g. oriented nanoclusters can be calculated by
:py:func:`~.cloudscattering.orientedCloudScattering`.

Methods to build clouds of scatterers e.g. a cube decorated with spheres at the corners can be
found in :ref:`Lattice` with examples. The advantage here is that there is no double counted overlap.

**Distribution of parameters**

Experimental data might be influenced by multimodal parameters (like multiple sizes)
or by one or several parameters distributed around a mean value.
See :ref:`Distribution of parameters`

------


Some **scattering length densities** as guide to choose realistic values for SLD and solventSLD :
 - neutron scattering  unit nm\ :sup:`-2`:
    - D2O                            = 6.335e-6 A\ :sup:`-2` = 6.335e-4 nm\ :sup:`-2`
    - H2O                            =-0.560e-6 A\ :sup:`-2` =-0.560e-4 nm\ :sup:`-2`
    - protein                        |ap| 2.0e-6 A\ :sup:`-2` |ap| 2.0e-4 nm\ :sup:`-2`
    - gold                           = 4.500e-6 A\ :sup:`-2` = 4.500e-4 nm\ :sup:`-2`
    - SiO2                           = 4.185e-6 A\ :sup:`-2` = 4.185e-4 nm\ :sup:`-2`
    - protonated polyethylene        =-0.315e-6 A\ :sup:`-2` =-0.315e-4 nm\ :sup:`-2` *bulk density*
    - protonated polyethylene glycol = 0.64e-6 A\ :sup:`-2` = 0.64e-4 nm\ :sup:`-2` *bulk density*

 - Xray scattering  unit nm^-2:
    - D2O                            = 0.94e-3 nm\ :sup:`-2` = 332 e/nm\ :sup:`3`
    - H2O                            = 0.94e-3 nm\ :sup:`-2` = 333 e/nm\ :sup:`3`
    - protein                        |ap| 1.20e-3 nm\ :sup:`-2` |ap| 430 e/nm\ :sup:`3`
    - gold                           = 13.1e-3 nm\ :sup:`-2` =4662 e/nm\ :sup:`3`
    - SiO2                           = 2.25e-3 nm\ :sup:`-2` = 796 e/nm\ :sup:`3`
    - polyethylene                   = 0.85e-3 nm\ :sup:`-2` = 302 e/nm\ :sup:`3` *bulk density*
    - polyethylene glycol            = 1.1e-3 nm\ :sup:`-2` = 390 e/nm\ :sup:`3` *bulk density*

Density SiO2 = 2.65 g/ml quartz; |ap| 2.2 g/ml quartz glass.

Using bulk densities for polymers in solution might be wrong.
E.g. polyethylene glycol (PEG) bulk has 390 e/nm³ but SAXS of PEG in water shows nearly matching conditions
which corresponds to roughly 333 e/nm³ [Thiyagarajan et al Macromolecules, Vol. 28, No. 23, (1995)]
Reasons are a solvent dependent specific volume (dependent on temperature and molecular weight)
and mainly hydration water density around PEG.


"""

import inspect
import os
import sys
import warnings
import numbers

import numpy as np
import scipy
import scipy.constants as constants
import scipy.integrate
import scipy.special as special

from . import formel
from . import parallel
from . import structurefactor as sf
from .dataarray import dataArray as dA
from .dataarray import dataList as dL

from .cloudscattering import cloudScattering, orientedCloudScattering, orientedCloudScattering3Dff
from .cloudscattering import fa_cuboid, fa_disc, fa_ellipsoid

try:
    from . import fscatter

    useFortran = True
except ImportError:
    useFortran = False

_path_ = os.path.realpath(os.path.dirname(__file__))

# variable to allow printout for debugging as if debug:print 'message'
debug = False


def guinier(q, Rg=1, A=1):
    """
    Classical Guinier

    :math:`I(q) = A e^{-Rg^2q^2/3}` see genGuinier with alpha=0

    Parameters
    ----------
    q :array
    A : float
    Rg : float

    """
    return genGuinier(q, Rg=Rg, A=A, alpha=0)


def genGuinier(q, Rg=1, A=1, alpha=0):
    r"""
    Generalized Guinier approximation for low wavevector q scattering q*Rg< 1-1.3

    For absolute scattering see introduction :ref:`formfactor (ff)`.

    Parameters
    ----------
    q : array of float
        Wavevector
    Rg : float
        Radius of gyration in units=1/q
    alpha : float
        Shape [α = 0] spheroid,    [α = 1] rod-like    [α = 2] plane
    A : float
        Amplitudes

    Returns
    -------
    dataArray
        Columns [q,Fq]

    Notes
    -----
    Quantitative analysis of particle size and shape starts with the Guinier approximations.
     - For three-dimensional objects the Guinier approximation is given by
       :math:`I(q) = A e^{-Rg^2q^2/3}`
     - This approximation can be extended also to rod-like and plane objects by
       :math:`I(q) =(\alpha \pi q^{-\alpha})  A e^{-Rg^2q^2/(3-\alpha) }`

    If the particle has one dimension of length L that is much larger than
    the others (i.e., elongated, rod-like, or worm-like), then there is a q
    range such that qR_c < 1 <<  qL, where α = 1.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,5,300)
     spheroid=js.ff.genGuinier(q, Rg=2, A=1, alpha=0)
     rod=js.ff.genGuinier(q, Rg=2, A=1, alpha=1)
     plane=js.ff.genGuinier(q, Rg=2, A=1, alpha=2)
     p=js.grace()
     p.plot(spheroid,le='sphere')
     p.plot(rod,le='rod')
     p.plot(plane,le='plane')
     p.yaxis(scale='l',min=1e-4,max=1e4)
     p.xaxis(scale='l')
     p.legend(x=0.03,y=0.1)
     #p.save(js.examples.imagepath+'/genGuinier.jpg')

    .. image:: ../../examples/images/genGuinier.jpg
     :align: center
     :width: 50 %
     :alt: genGuinier


    References
    ----------
    .. [1] Form and structure of self-assembling particles in monoolein-bile salt mixtures
           Rex P. Hjelm, Claudio Schteingart, Alan F. Hofmann, and Devinderjit S. Sivia
           J. Phys. Chem., 99:16395--16406, 1995

    """
    q = np.atleast_1d(q)
    if alpha == 0:
        pre = 1
    elif alpha == 1 or alpha == 2:
        pre = alpha * np.pi * q ** -alpha
    else:
        raise TypeError('alpha needs to be in 0,1,2')
    I = pre * A * np.exp(-Rg ** 2 * q ** 2 / (3 - alpha))
    result = dA(np.c_[q, I].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.Rg = Rg
    result.A = A
    result.alpha = alpha
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def beaucage(q, Rg=1, G=1, d=3):
    r"""
    Beaucage introduced a model based on the polymer fractal model.

    Beaucage used the numerical integration form (Benoit, 1957) although the analytical
    integral form was available [1]_. This is an artificial connection of Guinier and Porod Regime .
    Better use the polymer fractal model [1]_ used in gaussianChain.
    For absolute scattering see introduction :ref:`formfactor (ff)`.

    Parameters
    ----------
    q : array
        Wavevector
    Rg : float
        Radius of gyration in 1/q units
    G : float
        Guinier scaling factor, transition between Guinier and Porod
    d : float
        Porod exponent for large wavevectors

    Returns
    -------
    dataArray
        Columns [q,Fq]

    Notes
    -----
    Equation 9+10 in [1]_

    .. math:: I(q) &= G e^{-q^2 R_g^2 / 3.} + C q^{-d} \left[erf(qR_g / 6^{0.5})\right]^{3d}

                C &= \frac{G d}{R_g^d} \left[\frac{6d^2}{(2+d)(2+2d)}\right]^{d / 2.} \Gamma(d/2)

    with the Gamma function :math:`\Gamma(x)` .

    Polymer fractals:

    | d = 5/3    fully swollen chains,
    | d = 2      ideal Gaussian chains and
    | d = 3      globular e.g. collapsed chains. (volume scattering)
    | d = 4      surface scattering at a sharp interface/surface
    | d = 6-dim  rough surface area with a dimensionality dim between 2-3 (rough surface)
    | d < r      mass fractals (eg gaussian chain)

    The Beaucage model is used to analyze small-angle scattering (SAS) data from
    fractal and particulate systems. It models the Guinier and Porod regions with a
    smooth transition between them and yields a radius of gyration and a Porod
    exponent. This model is an approximate form of an earlier polymer fractal
    model that has been generalized to cover a wider scope. The practice of allowing
    both the Guinier and the Porod scale factors to vary independently during
    nonlinear least-squares fits introduces undesired artefact's in the fitting of SAS
    data to this model.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.1,5,300)
     d2=js.ff.beaucage(q, Rg=2, d=2)
     d3=js.ff.beaucage(q, Rg=2, d=3)
     d4=js.ff.beaucage(q, Rg=2,d=4)
     p=js.grace()
     p.plot(d2,le='d=2 gaussian chain')
     p.plot(d3,le='d=3 globular')
     p.plot(d4,le='d=4 sharp surface')
     p.yaxis(scale='l',min=1e-4,max=5)
     p.xaxis(scale='l')
     p.legend(x=0.15,y=0.1)
     #p.save(js.examples.imagepath+'/beaucage.jpg')

    .. image:: ../../examples/images/beaucage.jpg
     :align: center
     :width: 50 %
     :alt: beaucage



    .. [1] Analysis of the Beaucage model
            Boualem Hammouda  J. Appl. Cryst. (2010). 43, 1474–1478
            http://dx.doi.org/10.1107/S0021889810033856

    """
    q = np.atleast_1d(q)
    Rg = float(Rg)
    C = G * d / Rg ** d * (6 * d ** 2 / ((2. + d) * (2. + 2. * d))) ** (d / 2.) * special.gamma(d / 2.)
    I = G * np.exp(-q ** 2 * Rg ** 2 / 3.) + C / q ** d * (special.erf(q * Rg / 6 ** 0.5)) ** (3 * d)
    I[q == 0] = 1
    result = dA(np.c_[q, I].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.GuinierScalingfactor = G
    result.GuinierDimension = d
    result.Rg = Rg
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def guinierPorod3d(q, Rg1, s1, Rg2, s2, G2, dd):
    r"""
    Generalized Guinier-Porod Model with high Q power law with 3 length scales.

    An empirical model connecting the Guinier model with a transition to Porod scattering at high Q.
    The model represents the most general case containing three Guinier regions [1]_.

    Parameters
    ----------
    q : float
        Wavevector  in units of 1/nm
    Rg1 : float
        Radii of gyration for the short size of scattering object in units nm.
    Rg2 : float
        Radii of gyration for the overall size of scattering object in units nm.
    s1 : float
        Dimensionality parameter for the short size of scattering object (s1=1 for a cylinder)
    s2 : float
        Dimensionality parameter for the overall size of scattering object (s2=0 for a cylinder)
    G2 : float
        Intensity for q=0.
    d : float
        Porod exponent

    Returns
    -------
    dataArray
        Columns [q,Iq]
         Iq scattering intensity

    Notes
    -----
    Equ. 5 in [1]_ as:

    .. math:: I(Q) &= \frac{G_2}{Q^{s_2}} exp\big(\frac{-Q^2R_{g2}^2}{3-s_2}\big) \; for Q \leq Q_2

              I(Q) &= \frac{G_1}{Q^{s_1}} exp\big(\frac{-Q^2R_{g1}^2}{3-s_1}\big) \; for Q_2 \leq Q \leq Q_1

              I(Q) &= \frac{D}{Q^d} \; for Q \geq Q_1

    with equ 4

    .. math:: Q_1 &= \frac{1}{R_{g1}} \big( \frac{(d-s_1)(3-s_1)}{2} \big)^{1/2}

              D &= G_1 exp(\frac{-Q_1^2R_{g1}^2}{3-s_1})Q_1^{d-s_1}

              Q_2 &= \big[frac{s_1-s_2}{\frac{2}{3-s_2}R_{g2}^2 - \frac{2}{3-s_1}R_{g1}^2 }  \big]^{1/2}

              G_2 &= G_1 exp\big[ -Q_2^2 \big(\frac{R_{g1}^2}{3-s_1} - \frac{R_{g2}^2}{3-s_2} \big) \big] Q_2^{s_2-s_1}

    For fitting limit parameters to :math:`3>s_1>s_2` and :math:`R_{g2} >R_{g1}`. For more details see [1]_


    For a cylinder with length L and radius R (see [1]_)
    :math:`R_{g2} = (L^2/12+R^2/2)^{\frac{1}{2}}`  and :math:`R_{g1}=R/\sqrt{2}`


    Examples
    --------
    ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     I=js.ff.guinierPorod3d(q,Rg1=1,s1=1,Rg2=10,s2=0,G2=1,dd=4)
     p=js.grace()
     p.plot(I)
     p.xaxis(scale='l',label='q / nm\S-1')
     p.yaxis(scale='l',label='I(q) / a.u.')
     #p.save(js.examples.imagepath+'/guinierPorod3d.jpg')

    .. image:: ../../examples/images/guinierPorod3d.jpg
     :align: center
     :width: 50 %
     :alt: guinierPorod3d

    References
    ----------
    .. [1]  A new Guinier/Porod Model
            B. Hammouda J. Appl. Cryst. (2010) 43, 716-719

    Author M. Kruteva JCNS 2019

    """
    q = np.atleast_1d(q)

    # define parameters for smooth transitions
    Q1 = (1 / Rg1) * ((dd - s1) * (3 - s1) / 2) ** 0.5
    Q2 = ((s1 - s2) / (2 / (3 - s2) * Rg2 ** 2 - 2 / (3 - s1) * Rg1 ** 2)) ** 0.5
    G1 = G2 / (np.exp(-Q2 ** 2 * (Rg1 ** 2 / (3 - s1) - Rg2 ** 2 / (3 - s2))) * Q2 ** (s2 - s1))
    D = G1 * np.exp(-Q1 ** 2 * Rg1 ** 2 / (3 - s1)) * Q1 ** (dd - s1)

    # define functions in different regions
    def _I1_3regions(q):
        res = G2 / q ** s2 * np.exp(-q ** 2 * Rg2 ** 2 / (3 - s2))
        return res

    def _I2_3regions(q):
        res = G1 / q ** s1 * np.exp(-q ** 2 * Rg1 ** 2 / (3 - s1))
        return res

    def _I3_3regions(q):
        res = D / q ** dd
        return res

    I = np.piecewise(q, [q < Q2, (Q2 <= q) & (q < Q1), q >= Q1], [_I1_3regions, _I2_3regions, _I3_3regions])

    result = dA(np.c_[q, I].T)
    result.columnname = 'q; Iq'
    result.setColumnIndex(iey=None)
    result.Rg1 = Rg1
    result.s1 = s1
    result.Rg2 = Rg2
    result.s2 = s2
    result.G1 = G1
    result.G2 = G2
    result.dd = dd
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def guinierPorod(q, Rg, s, I0, d):
    r"""
    Generalized Guinier-Porod Model with high Q power law.

    An empirical model connecting the Guinier model with a transition to Porod scattering at high Q.


    Parameters
    ----------
    q : float
        Wavevector  in units of 1/nm
    Rg : float
        Radii of gyration in units nm.
    s : float
        Dimensionality parameter describing the low Q region.
         - 0 spheres globular
         - 1 rods, linear
         - 2 lamella planar
    d : float
        Porod exponent describing the high Q slope.
    I0 : float
        Intensity, named G in [1]_.

    Returns
    -------
    dataArray
        Columns [q, Iq]
        Iq    scattering intensity

    Notes
    -----
    Equ. 3 in [1]_ as:

    .. math:: I(Q) &= \frac{G}{Q^s}exp\big(\frac{-Q^2R_g^2}{3-s}\big) \; for Q \leq Q_1

              I(Q) &= \frac{D}{Q^d} \; for Q \geq Q_1

    with equ 4

    .. math:: Q_1 &= \frac{1}{R_g} \big( \frac{(d-s)(3-s)}{2} \big)^{1/2}

              D &= G exp(\frac{-Q_1^2R_g^2}{3-s})Q_1^{d-s}



    Examples
    --------
    ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     I=js.ff.guinierPorod(q,s=0,Rg=5,I0=1,d=4)
     p=js.grace()
     p.plot(I)
     p.xaxis(scale='l',label='q / nm\S-1')
     p.yaxis(scale='l',label='I(q) / a.u.')
     #p.save(js.examples.imagepath+'/guinierPorod.jpg')

    .. image:: ../../examples/images/guinierPorod.jpg
     :align: center
     :width: 50 %
     :alt: guinierPorod

    References
    ----------
    .. [1]  A new Guinier/Porod Model
            B. Hammouda J. Appl. Cryst. (2010) 43, 716-719

    Author M. Kruteva JCNS 2019
    """
    q = np.atleast_1d(q)

    # define parameters for smooth transitions
    Q1 = (1 / Rg) * ((d - s) * (3 - s) / 2) ** 0.5
    D = I0 * np.exp(-Q1 ** 2 * Rg ** 2 / (3 - s)) * Q1 ** (d - s)

    # define functions in different regions
    def _I1_2regions(q):
        res = I0 / q ** s * np.exp(-q ** 2 * Rg ** 2 / (3 - s))
        return res

    def _I2_2regions(q):
        res = D / q ** d
        return res

    I = np.piecewise(q, [q < Q1, q >= Q1], [_I1_2regions, _I2_2regions])

    result = dA(np.c_[q, I].T)
    result.columnname = 'q; Iq'
    result.setColumnIndex(iey=None)
    result.Rg = Rg
    result.s = s
    result.I0 = I0
    result.D = D
    result.d = d
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _fa_sphere(qr):
    """
    scattering amplitude sphere with catching the zero
    qr is array dim 1
    """
    fa=np.ones(qr.shape)
    qr0 = (qr!=0)
    fa[qr0] = 3 / qr[qr0] ** 3 * (np.sin(qr[qr0]) - qr[qr0] * np.cos(qr[qr0]))
    return fa


def sphere(q, radius, contrast=1):
    r"""
    Scattering of a single homogeneous sphere.

    Parameters
    ----------
    q : float
        Wavevector  in units of 1/nm
    radius : float
        Radius in units nm
    contrast : float, default=1
        Difference in scattering length to the solvent = contrast

    Returns
    -------
    dataArray
        Columns [q, Iq, fa]
        Iq    scattering intensity
        - fa formfactor amplitude
        - .I0   forward scattering


    Notes
    -----
    .. math:: I(q)=  4\pi\rho^2V^2\left[\frac{3(sin(qR) - qr cos(qR))}{(qR)^3}\right]^2

    with contrast :math:`\rho` and sphere volume :math:`V=\frac{4\pi}{3}R^3`

    The first minimum of the form factor is at qR=4.493

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.1,5,300)
     p=js.grace()
     R=3
     sp=js.ff.sphere(q, R)
     p.plot(sp.X*R,sp.Y,li=1)
     p.yaxis(label='I(q)',scale='l',min=1e-4,max=1e5)
     p.xaxis(label='qR',scale='l',min=0.1*R,max=5*R)
     p.legend(x=0.15,y=0.1)
     #p.save(js.examples.imagepath+'/sphere.jpg')

    .. image:: ../../examples/images/sphere.jpg
     :align: center
     :width: 50 %
     :alt: sphere


    References
    ----------
    .. [1] Guinier, A. and G. Fournet, "Small-Angle Scattering of X-Rays", John Wiley and Sons, New York, (1955).

    """
    R = radius
    qr = np.atleast_1d(q) * R
    fa0 = (4 / 3. * np.pi * R ** 3 * contrast)  # forward scattering amplitude q=0
    faQR = fa0 * _fa_sphere(qr)
    result = dA(np.c_[q, faQR** 2, faQR].T)
    result.columnname = 'q; Iq; fa'
    result.setColumnIndex(iey=None)
    result.radius = radius
    result.I0 = fa0**2
    result.fa0 = fa0
    result.contrast = contrast
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def sphereFuzzySurface(q, R, sigmasurf, contrast):
    r"""
    Scattering of a sphere with a fuzzy interface.

    Parameters
    ----------
    q : float
        Wavevector  in units of 1/(R units)
    R : float
        The particle radius R represents the radius of the particle
        where the scattering length density profile decreased to 1/2 of the core density.
    sigmasurf : float
        Sigmasurf is the width of the smeared particle surface.
    contrast : float
        Difference in scattering length to the solvent = contrast

    Returns
    -------
    dataArray
        Columns [q, Iq]
        Iq    scattering intensity related to sphere volume.
        - .I0   forward scattering

    Notes
    -----
    A radial box profile (H(r-R) Heaviside function) is convoluted with a Gaussian to smear the edge.

    .. math:: \rho(r) \propto H(r-R)\circledast e^{-\frac{1}{2}r^2\sigma_{surf}^2}

    The convolution results in the multiplication of the sphere formfactor amplitude with a gaussian leading to

    .. math:: I(q)=  4\pi\rho^2V^2[F_a(q)]^2

    .. math:: F_a(q)= \frac{3(sin(qR) - qr cos(qR))}{(qR)^3} e^{-\frac{1}{2}q^2\sigma_{surf}^2}


    with contrast :math:`\rho` and sphere volume :math:`V=\frac{4\pi}{3}R^3`.

    The "fuzziness" of the interface is defined by the parameter sigmasurf (width of the Gaussian). The particle
    radius R represents the radius of the particle where the scattering length density profile
    decreased to 1/2 of the core density. sigmasurf is the width of the smeared particle
    surface. The inner regions of the microgel that display a higher density are described by
    the radial box profile extending to a radius of approximately Rbox ~ R - 2(sigma). In
    dilute solution, the profile approaches zero as Rsans ~ R + 2(sigma).

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.1,5,300)
     p=js.grace()
     sFS=js.ff.sphereFuzzySurface(q, 3, 0.01, 1)
     p.plot(sFS,le='sigmasurf=0.01')
     sFS=js.ff.sphereFuzzySurface(q, 3, 0.5, 1)
     p.plot(sFS,le='sigmasurf=0.3')
     sFS=js.ff.sphereFuzzySurface(q, 3, 1, 1)
     p.plot(sFS,le='sigmasurf=1')
     p.yaxis(label='I(q)',scale='l',min=1e-4,max=1e5)
     p.xaxis(label='q / nm\S-1',scale='l')
     p.legend(x=0.15,y=0.1)
     #p.save(js.examples.imagepath+'/sphereFuzzySurface.jpg')

    .. image:: ../../examples/images/sphereFuzzySurface.jpg
     :align: center
     :width: 50 %
     :alt: sphereFuzzySurface


    References
    ----------
    .. [1] M. Stieger, J. S. Pedersen, P. Lindner, W. Richtering, Langmuir 20 (2004) 7283-7292

    """
    q = np.atleast_1d(q)
    f0 = (4 / 3. * np.pi * R ** 3 * contrast) ** 2  # forward scattering q=0

    def _ff(q):
        return f0 * (3 / (q * R) ** 3 * (np.sin(q * R) - q * R * np.cos(q * R)) *
                     np.exp(-sigmasurf ** 2 * q ** 2 / 2.)) ** 2

    ffQR = np.piecewise(q, [q == 0], [f0, _ff])
    result = dA(np.c_[q, ffQR].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.HsRadius = R
    result.I0 = f0
    result.contrast = contrast
    result.sigmasurf = sigmasurf
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _fa_coil(qrg):
    """
    qrg is array dim 1
    fa_coil**2 is Debye function see [2]_ in  sphereCoreShellGaussianCorona
    """
    fa = np.ones(qrg.shape)
    fa[qrg != 0] = (1 - np.exp(-qrg[qrg > 0])) / (qrg[qrg > 0])
    return fa


def sphereGaussianCorona(q, R, Rg, Ncoil, coilequR, coilSLD=0.64e-4, sphereSLD=4.186e-4, solventSLD=6.335e-4, d=1):
    r"""
    Scattering of a sphere surrounded by gaussian coils as model for grafted polymers on particle e.g. a micelle.

    The additional scattering is uniformly distributed at the surface, which might fail for lower aggregation
    numbers as 1, 2, 3.
    Instead of aggregation number equ 1 in [1]_ we use sphere volume and a equivalent volume of the gaussian coils.

    Parameters
    ----------
    q: array of float
        Wavevectors in unit 1/nm
    R : float
        Sphere radius in unit nm
    Rg : float
        Radius of gyration of coils in unit nm
    d : float, default 1
        Coils centre located d*Rg away from the sphere surface
    Ncoil : float
        Number of coils at the surface (aggregation number)
    coilequR : float
        Equivalent radius to calc volume of one coil if densely packed as a sphere.
        Needed to calculate absolute scattering of the coil.
    coilSLD : float
        Scattering length density of coil in bulk.  unit nm^-2.
        default hPEG = 0.64*1e-6 A^-2 = 0.64*1e-4 nm^-2
    sphereSLD : float
        Scattering length density of sphere.unit nm^-2.
        default SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2
    solventSLD : float
        Scattering length density of solvent. unit nm^-2.
        default D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2

    Returns
    -------
    dataArray
        Columns [q,Iq]
         - .coilRg
         - .sphereRadius
         - .numberOfCoils
         - .coildistancefactor
         - .coilequVolume
         - .coilSLD
         - .sphereSLD
         - .solventSLD

    Examples
    --------
    ::

     import jscatter as js
     q=js.loglist(0.1,5,100)
     p=js.grace()
     p.plot(js.ff.sphereGaussianCorona(q,4.4,2,30,2))
     p.yaxis(label='I(q)',scale='l',min=1e-4,max=1)
     p.xaxis(label='q / nm\S-1',scale='l')
     #p.save(js.examples.imagepath+'/sphereGaussianCorona.jpg')

    .. image:: ../../examples/images/sphereGaussianCorona.jpg
     :align: center
     :width: 50 %
     :alt: sphereGaussianCorona

    Notes
    -----
    The defaults result in a silica sphere with hPEG grafted at the surface in D2O.
     - Rg=N**0.5*b    with N monomers of length b
     - Vcoilsphere=N*monomerVolume=4/3.*np.pi*coilequR**3
     - coilequR=(N*monomerVolume/(4/3.*np.pi))**(1/3.)

    References
    ----------
    .. [1] Form factors of block copolymer micelles with spherical, ellipsoidal and cylindrical cores
           Pedersen J.
           Journal of Applied Crystallography 2000 vol: 33 (3) pp: 637-640
    .. [2] Hammouda, B. (1992). J. Polymer Science B: Polymer Physics30 , 1387–1390

    """
    q = np.atleast_1d(q)
    Q = np.where(q == 0, q * 0 + 1e-10, q)
    # scattering amplitude gaussian coil
    cg = coilSLD - solventSLD
    coilVolume = (4 / 3. * np.pi * coilequR ** 3)
    fa_coil = coilVolume * cg * _fa_coil(Rg * Q)
    # amplitude sphere
    cs = sphereSLD - solventSLD
    f0 = (4 / 3. * np.pi * R ** 3 * cs)  # forward scattering Q=0
    fa_sphere = f0 * _fa_sphere(Q * R)
    # total scattering from one sphere and N coils
    #  (   fa_sphere + [ fa_coil + fa_coil+.....] )**2
    # sphere scattering
    res = fa_sphere ** 2
    # N * coil scattering
    res += Ncoil * fa_coil ** 2
    # N times interference between one coil and one sphere
    res += 2 * Ncoil * fa_sphere * fa_coil * np.sin(Q * (R + d * Rg)) / (Q * (R + d * Rg))
    # interference between one coils with distance R+d*Rg
    res += Ncoil * (Ncoil - 1) * (fa_coil * np.sin(Q * (R + d * Rg)) / (Q * (R + d * Rg))) ** 2

    result = dA(np.c_[q, res].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.coilRg = Rg
    result.sphereRadius = R
    result.numberOfCoils = Ncoil
    result.coildistancefactor = d
    result.coilequVolume = coilVolume
    result.coilSLD = coilSLD
    result.sphereSLD = sphereSLD
    result.solventSLD = solventSLD
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def sphereCoreShellGaussianCorona(q, Rc, Rs, Rg, Ncoil, thicknessCoils, coilSLD, coreSLD, shellSLD, solventSLD=0, d=1):
    r"""
    Scattering of a core-shell particle surrounded by gaussian coils as model for grafted polymers on particle.

    The model is in analogy to the sphereGaussianCorona replacing the sphere by a core shell particle in [1]_.
    The additional scattering from the coils is uniformly distributed at the surface,
    which might fail for lower aggregation numbers as 1, 2, 3.
    Instead of aggregation number equ. 1 in [1]_ we use volume of the gaussian coils collapsed to the surface.

    Parameters
    ----------
    q: array of float
        Wavevectors in unit 1/nm.
    Rc,Rs : float
        Radius of core and shell in unit nm.
    Rg : float
        Radius of gyration of coils in unit nm.
    d : float, default 1
        Coils centre located d*Rg away from the sphere surface
        This might be equivalent to Rg
    Ncoil : float
        Number of coils at the surface (aggregation number)
    thicknessCoils : float
        Thickness of a layer if all coils collapsed on the surface as additional shell in nm.
        Needed to calculate absolute scattering of the expanded coils.
        The densely packed coil shell volume is :math:`V_{coils}= 4/3\pi((R_{s}+thicknessCoils)^3-R_s^3)` and
        the volume of a single polymer `V_m =V_{coils} / Ncoils`.
    coilSLD : float
        Scattering length density of coil in bulk as if collapsed on surface unit nm^-2.
    coreSLD,shellSLD : float, default see text
        Scattering length density of core and shell in unit nm^-2.
    solventSLD : float, default 0
        Scattering length density of solvent. unit nm^-2.

    Returns
    -------
    dataArray
        Columns [q,Iq]
         - .coilRg
         - .Radii
         - .numberOfCoils
         - .coildistancefactor
         - .coilequVolume
         - .coilSLD
         - .coreshellSLD
         - .solventSLD

    Examples
    --------
    Example for silica particle coated with protein and some polymer coils.
    The polymer changes the high Q power law from sphere like to polymer coil like dependent on contrast.
    ::

     import jscatter as js
     q=js.loglist(0.01,5,500)
     p=js.grace()
     sol=6-4
     for i,c in enumerate([0,0.3,0.7,1,1.3,1.7,2],1):
         FF=js.ff.sphereCoreShellGaussianCorona(q,Rc=8,Rs=12,Rg=6,Ncoil=20,
                            thicknessCoils=1.5,coilSLD=c*sol,solventSLD=sol,coreSLD=4e-4, shellSLD=2e-4,)
         p.plot(FF,sy=[1,0.2,i],li=i,le=f'coilSLD={c}*solventSLD')
     p.yaxis(label='I(q)',ticklabel=['power',0],scale='l',min=1,max=1e9)
     p.xaxis(label='q / nm\S-1',scale='l',min=0.01,max=5)
     p.legend(x=0.011,y=1000)
     p.title('CoreShellGaussianCorona')
     #p.save(js.examples.imagepath+'/sphereCoreShellGaussianCorona.jpg')

    .. image:: ../../examples/images/sphereCoreShellGaussianCorona.jpg
     :align: center
     :width: 50 %
     :alt: sphereCoreShellGaussianCorona

    Notes
    -----
     - Rg=N**0.5*b    with N monomers of length b
     - Vcoilsphere=N*monomerVolume=4/3.*np.pi*coilequR**3
     - coilequR=(N*monomerVolume/(4/3.*np.pi))**(1/3.)


    References
    ----------
    .. [1] Form factors of block copolymer micelles with spherical, ellipsoidal and cylindrical cores
           Pedersen J
           Journal of Applied Crystallography 2000 vol: 33 (3) pp: 637-640
    .. [2] Hammouda, B. (1992).J. Polymer Science B: Polymer Physics30 , 1387–1390

    """
    q = np.atleast_1d(q)
    Q = np.where(q == 0, q * 0 + 1e-10, q)

    # scattering amplitude gaussian coil
    cg = coilSLD - solventSLD
    coilVolume = 4 / 3. * np.pi * ((Rs + thicknessCoils) ** 3 - Rs ** 3) / Ncoil
    fa_coil = coilVolume * cg * _fa_coil(Rg * Q)

    # amplitude core shell from multiShellSphere with [2] as fa
    fa_coreshell = multiShellSphere(q, [Rc, Rs - Rc], [coreSLD, shellSLD], solventSLD=solventSLD)[[0, 2]]

    # total scattering from one sphere and N coils
    #  (   fa_coreshell + [ fa_coil + fa_coil+.....] )**2
    # core shell scattering
    res = fa_coreshell.Y ** 2
    # N * coil scattering
    res += Ncoil * fa_coil ** 2
    # N times interference between one coil and one sphere
    res += 2 * Ncoil * fa_coreshell.Y * fa_coil * np.sin(Q * (Rs + d * Rg)) / (Q * (Rs + d * Rg))
    # interference between coils of distance R+d*Rg
    res += Ncoil * (Ncoil - 1) * (fa_coil * np.sin(Q * (Rs + d * Rg)) / (Q * (Rs + d * Rg))) ** 2

    result = dA(np.c_[q, res].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.coilRg = Rg
    result.Radiii = [Rc, Rs]
    result.numberOfCoils = Ncoil
    result.coildistancefactor = d
    result.coilVolume = coilVolume
    result.coilSLD = coilSLD
    result.coreshellSLD = [coreSLD, shellSLD]
    result.solventSLD = solventSLD
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def sphereCoreShell(q, Rc, Rs, bc, bs, solventSLD=0):
    r"""
    Scattering of a spherical core shell particle.

    See  multiShellSphere.

    Parameters
    ----------
    q : float
        Wavevector  in units of 1/(R units)
    Rc,Rs : float
        Radius core and radius of shell
        Rs>Rc
    bc,bs : float
        Contrast to solvent scattering length density of core and shell.
    solventSLD : float, default =0
        Scattering length density of the surrounding solvent.
        If equal to zero (default) then in profile the contrast is given.

    Returns
    -------
    dataArray
        Columns [wavevector ,Iq, fa]


    Examples
    --------
    ::

     import jscatter as js
     q=js.loglist(0.01,5,500)
     p=js.grace()
     FF=js.ff.sphereCoreShell(q,6,12,-0.2,1)
     p.plot(FF,sy=[1,0.2],li=1)
     p.yaxis(label='I(q)',scale='l',min=1,max=1e8)
     p.xaxis(label='q / nm\S-1',scale='l')
     #p.save(js.examples.imagepath+'/sphereCoreShell.jpg')

    .. image:: ../../examples/images/sphereCoreShell.jpg
     :align: center
     :width: 50 %
     :alt: sphereCoreShell

    """
    return multiShellSphere(q, [Rc, Rs - Rc], [bc, bs], solventSLD=solventSLD)


def multiShellSphere(q, shellthickness, shellSLD, solventSLD=0):
    r"""
    Scattering of spherical multi shell particle including linear contrast variation in subshells.

    The results needs to be multiplied with the concentration to get the measured scattering.
    The resulting contrastprofile can be accessed as .contrastprofile

    Parameters
    ----------
    q : array
        Wavevectors to calculate form factor, unit e.g. 1/nm.
    shellthickness : list of float
        Thickness of shells starting from inner most, unit in nm.
        There is no limit for the number of shells.
    shellSLD : list of float or list
        List of scattering length densities of the shells in sequence corresponding to shellthickness. unit in nm**-2
         - Innermost shell needs to be constant shell.
         - If an element of the list is itself a list of SLD values it is interpreted as equal thick subshells
           with linear progress between SLD values in sum giving shellthickness.
           Here any shape can be approximated as sequence of linear pieces.
         - If subshell list has only one float e.g. [1e.4] the second value is the SLD of the following shell.
         - If empty list is given as [] the SLD of the previous and following shells are used as smooth transition.
    solventSLD : float, default=0
        Scattering length density of the surrounding solvent.
        If equal to zero (default) then in profile the contrast is given.
        Unit in 1/nm**2

    Returns
    -------
    dataArray
        Columns [wavevector, Iq, Fa]
        Iq                  scattering cross section in units nm**2
         - Fa                   formfactor amplitude
         - .contrastprofile     as radius and contrast values at edge points
         - .shellthickness      consecutive shell thickness
         - .shellcontrast       contrast of the shells to the solvent
         - .shellradii          outer radius of the shells
         - .slopes              slope of linear increase of each shell
         - .outerVolume         Volume of complete sphere
         - .I0                  forward scattering for Q=0
         - .fa0                 forward scattering amplitude for Q=0

    Notes
    -----
    The scattering intensity for a multishell particle with several subshells is

    .. math:: I(q) = F^2_a(q) = \left( \sum_i f_a(q) \right)^2

    The scattering amplitude of a subshell with inner and outer radius :math:`R_{i,o}` is

    .. math:: f_a(q) = 4\pi\int_{R_i}^{R_o} \rho(r) \frac{sin(qr)}{qr}r^2dr

    where we use always the scattering length density difference to the solvent (contrast)
    :math:`\rho(r) = \hat{\rho}(r) - \hat{\rho}_{solvent}`.



    - For **constant scattering length density** :math:`\rho(r) = \rho` we get

      .. math:: f_{a,const}(q) = \frac{4\pi}{3}r^3\rho
                                 \left. \frac{3(sin(qr)-qR cos(qr))}{(qr)^3}\right\rvert_{r=R_i}^{r=R_o}

      with forward scattering contribution

      .. math:: f_{a,const}(q=0) = \frac{4\pi\rho}{3} (R_i^{3} - R_o^{3})

    - For a **linear variation** as :math:`\rho(r)=\Delta\rho(r-R_i)/d + \rho_i` with
      :math:`\Delta\rho=\rho_o-\rho_i` and thickness :math:`d=(R_o-R_i)`
      we may sum a constant subshell as above with :math:`\rho(r)=\rho_i`
      and contribution of the linear increase :math:`\rho(r)=\Delta\rho(r-R_i)/d` resulting in

      .. math:: f_{a,lin}(q) =f_{a,const}(q) + \frac{4\pi\Delta\rho}{d}
                          \left. \frac{(q(2r-R_i))sin(qr)-(q^2r(r-R_i)-2)cos(qr)  }{q^4}
                          \right\rvert_{r=R_i}^{r=R_o}

      with the forward scattering contribution

      .. math:: f_{a,lin}(q=0)= f_{a,const}(q=0) + \frac{\pi \Delta\rho}{3 d}
                              \left(R_{i} - R_{o}\right)^{2} \left(R_{i}^{2} + 2 R_{i} R_{o} + 3 R_{o}^{2}\right)

    - The solution is unstable (digital resolution) for really low QR values, which are set to the I0 scattering.


    Examples
    --------
    Alternating shells with 5 alternating thickness 0.4 nm and 0.6 nm with h2o, d2o scattering contrast in vacuum::

     import jscatter as js
     import numpy as np
     x=np.r_[0.05:10:0.01]
     ashell=js.ff.multiShellSphere(x,[0.4,0.6]*5,[-0.56e-4,6.39e-4]*5)
     #plot it
     p=js.grace()
     p.new_graph(xmin=0.24,xmax=0.5,ymin=0.2,ymax=0.5)
     p[0].plot(ashell)
     p[0].yaxis(label='I(q)',scale='l',min=1e-7,max=0.1)
     p[0].xaxis(label='q / nm\S-1',scale='l',min=0.05,max=10)
     p[1].plot(ashell.contrastprofile,li=1) # a contour of the SLDs
     p[1].subtitle('contrastprofile')
     p[0].title('alternating shells')
     #p.save(js.examples.imagepath+'/multiShellSphere.jpg')

    .. image:: ../../examples/images/multiShellSphere.jpg
     :align: center
     :width: 50 %
     :alt: multiShellSphere

    Double shell with exponential decreasing exterior shell to solvent scattering::

     import jscatter as js
     import numpy as np
     x=np.r_[0.0:5:0.01]
     def doubleexpshells(q,d1,d2,e3,sd1,sd2,sol,bgr):
        fq = js.ff.multiShellSphere(q,[d1,d2,e3*3],[sd1,sd2,((sd2-sol)*np.exp(-np.r_[0:3:9j]))+sol],solventSLD=sol)
        fq.Y = fq.Y + bgr
        return fq

     dde=doubleexpshells(x,0.5,0.5,1,1e-4,2e-4,0,1e-10)
     dde1=doubleexpshells(x,0.5,0.1,0.5,1e-4,3e-4,0,1e-10)

     #plot it
     p=js.grace(1,1)
     p.multi(2,1)
     p[0].plot(dde,le='thick shell')
     p[0].plot(dde1,le='thin shell')
     p[0].yaxis(label='I(q)',min=1e-10,max=3e-4,scale='l')
     p[1].xaxis(label='q / nm\S-1')
     p[1].plot(dde.contrastprofile,li=1,le='thick shell') # a contour of the SLDs
     p[1].plot(dde1.contrastprofile,li=1,le='thin shell')
     p[1].yaxis(label='contrast',min=0,max=3e-4)
     p[1].xaxis(label='r / nm',min=0,max=5)
     p[0].title('core-shell-exp particle')
     p[1].legend(x=3,y=0.0002)
     #p.save(js.examples.imagepath+'/coreShellExp.jpg')

    .. image:: ../../examples/images/coreShellExp.jpg
     :align: center
     :width: 50 %
     :alt: coreShellExp


    """
    if isinstance(shellSLD, numbers.Number): shellSLD = [shellSLD]
    if isinstance(shellthickness, numbers.Number): shellthickness = [shellthickness]
    if len(shellSLD) != len(shellthickness):
        raise Exception('shellSLD and shellthickness should be of same length but got:%i!=%i'
                        % (len(shellSLD), len(shellthickness)))
    Q = np.array(q)
    shelld = []  # list of shellthicknesses
    shelltype = []  # list of types
    SLDs = []  # constant scattering length density of inner radius to outer radius of shell
    Slopes = []  # linear slope from inside to outside of a shell
    for i, sld in enumerate(shellSLD):
        if isinstance(sld, numbers.Number):  # a normal constant shell only ffsph will be used
            shelld.append(shellthickness[i])
            shelltype.append(0)
            SLDs.append(sld)
            Slopes.append(0)
        elif shellthickness[i] == 0:
            shelld.append(shellthickness[i])
            shelltype.append(0)
            SLDs.append(sld[0])
            Slopes.append(0)
        else:  # a sphere with lin progress
            if i == 0:
                raise Exception('innermost shell needs to be constant contrast even if it is small!!')
            if len(sld) == 0:  # linear between neighboring shells
                if i == 0:
                    raise Exception('A SLD at zero (first shell) should be defined')
                shelld.append(shellthickness[i])
                shelltype.append(1)
                SLDs.append(shellSLD[i - 1])
                Slopes.append((shellSLD[i + 1] - shellSLD[i - 1]) / shellthickness[i])
            elif len(sld) == 1:  # linear to following with starting value
                shelld.append(shellthickness[i])
                shelltype.append(1)
                SLDs.append(sld[0])
                Slopes.append((shellSLD[i + 1] - sld[0]) / shellthickness[i])
            else:
                shelld.append([shellthickness[i] / (len(sld) - 1)] * (len(sld) - 1))
                shelltype.append([1] * (len(sld) - 1))
                SLDs.append(sld[:-1])
                slda = np.array(sld)
                Slopes.append((slda[1:] - slda[:-1]) / (shellthickness[i] / (len(sld) - 1)))
    SLDs = np.hstack(SLDs)
    shelld = np.hstack(shelld)
    shelltype = np.hstack(shelltype)
    Slopes = np.hstack(Slopes)
    radii = np.cumsum(shelld)

    # subtract solvent to have in any case the contrast to the solvent
    dSLDs = SLDs - solventSLD

    #  Volume  *  formfactor

    def ffsph(qr, r):
        # constant profile
        return 4 / 3. * np.pi * r * r * r * 3. * (np.sin(qr) - qr * np.cos(qr)) / qr / qr / qr

    def fflin(q, r, ri):
        # lin profile = drho*(r-Ri)/l
        qr = q[:, None] * r
        q2 = q[:, None] ** 2
        return 4 * np.pi / q2 ** 2 * (
                q[:, None] * (2 * r - ri) * np.sin(qr) + q2 * r * (ri - r) * np.cos(qr) + 2 * np.cos(qr))

    def _fa(QQ, r):
        # outer integration boundary r
        Pc = dSLDs * ffsph(QQ[:, None] * r, r)
        if len(r) > 1:  # subtract lower integration boundary
            # innermost shell has r==0 and is not calculated
            Pc[:, 1:] = Pc[:, 1:] - dSLDs[1:] * ffsph(QQ[:, None] * r[:-1], r[:-1])
        # look at slopes, innermost is not slope
        if len(r) > 1:
            # Ri is r[:-1] Rout is r[1:]
            Pl = Slopes[1:] * fflin(QQ, r[1:], r[:-1])
            # subtract lower integration boundary
            Pl = Pl - Slopes[1:] * fflin(QQ, r[:-1], r[:-1])
            Pc[:, 1:] += Pl
        return Pc.sum(axis=1)

    # forward scattering Q=0 -------------
    # constant contribution
    dslds = 4 / 3. * np.pi * radii ** 3 * dSLDs
    dslds[:-1] = dslds[:-1] - 4 / 3. * np.pi * radii[:-1] ** 3 * dSLDs[1:]
    # lin contribution
    Ro = radii[1:]
    Ri = radii[:-1]
    slr = np.zeros_like(Slopes)
    slr[1:] = np.pi / 3. * Slopes[1:] * (Ri - Ro) ** 2 * (Ri ** 2 + 2 * Ri * Ro + 3 * Ro ** 2)

    fa0 = (dslds + slr).sum()
    # ------------------------------------
    # the calculation shows up to be unstable for really small Qr as the binary resolution shows up in the lin part.
    # therefore we limit it to the f0 value below a threshold; the error is of order 1e-4
    ffa = np.piecewise(Q, [Q < 5e-3 / max(radii)], [fa0, _fa], radii)
    # return formfactor and formfactor amplitude
    result = dA(np.c_[q, ffa**2, ffa].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq; fa'
    result.shellthickness = shelld
    result.shellcontrast = SLDs
    result.shellradii = radii
    contrastprofile = np.c_[np.r_[radii - shelld, radii], np.r_[SLDs, SLDs + Slopes * shelld]].T
    result.contrastprofile = contrastprofile[:,
                             np.repeat(np.arange(len(SLDs)), 2) + np.tile(np.r_[0, len(SLDs)], len(SLDs))]
    result.slopes = Slopes
    result.outerVolume = 4. / 3 * np.pi * max(radii) ** 3
    result.I0 = fa0**2
    result.fa0 = fa0
    result.shelltype = shelltype
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _fa_disc(q, R, D, angle):
    """
    disc form factor amplitude, save for q=0 and q<0 result is zero

    q : wavevectors
    D : thickness of discs , array
    R : Radii of discs, array
    angle : angle between axis and scattering vector q in rad

    q<0 result is zero needed in ellipsoidFilledCylinder

    """
    # deal with possible zero in q
    if isinstance(q, numbers.Number):
        q = np.r_[q]
    result = np.zeros((len(q), len(D)))
    if angle != 0:
        sina = np.sin(angle)
        cosa = np.cos(angle)
    else:
        sina = 1
        cosa = 1
    if D[0] > 0 and R[0] > 0:
        fq0 = 2. * np.pi * R ** 2 * D
        fqq = lambda q: fq0 * special.j1(q[:, None] * R * sina) / (q[:, None] * R * sina) * \
                        np.sinc(q[:, None] * D / 2. * cosa / np.pi)
    elif R[0] > 0:
        fq0 = 2. * np.pi * R ** 2 * 1
        fqq = lambda q: fq0 * special.j1(q[:, None] * R * sina) / (q[:, None] * R * sina)
    elif D[0] > 0:
        fq0 = 2. * D
        fqq = lambda q: fq0 * np.sinc(q[:, None] * D / 2. * cosa / np.pi)

    result[np.where(q > 0)[0], :] = fqq(q[np.where(q > 0)])
    result[np.where(q == 0)[0], :] = fq0 * 0.5
    return result


def _fq_disc(QQ, R, D, angle, dSLDs):
    # formfactor of a cylinder with orientation angle alpha
    # outer integration boundary r
    QQ0 = np.r_[0, QQ]
    Pc = dSLDs * _fa_disc(QQ0, R, D, angle)
    if len(R) > 1:  # subtract lower integration boundary
        #  r==0 is not calculated
        Pc[:, 1:] = Pc[:, 1:] - dSLDs[1:] * _fa_disc(QQ0, R[:-1], D[:-1], angle)
    # cylinder without cap
    Pc2 = Pc.sum(axis=1) ** 2
    result = dA(np.c_[QQ, Pc2[1:] * np.sin(angle)].T)
    # store the forward scattering
    result.I0 = Pc2[0]
    return result


def multiShellDisc(q, radialthickness, shellthickness, shellSLD, solventSLD=0, alpha=None, nalpha=60):
    r"""
    Multi shell disc in solvent averaged over axis orientations.

    Parameters
    ----------
    q : array
        Wavevectors, units 1/nm
    radialthickness : float, all >0
        Radial thickness of disc shells from inner to outer, units nm
        radii r=cumulativeSum(radialthickness)
    shellthickness : list of float or float, all >=0
        Thickness of shells from inner to outer, units nm, same length as radialthickness.
         - Innermost thickness is only taken once.
         - total thickness = shellthickness[0]+2*cumulativeSum(shellthickness[1:])
         - For shellthickness =0 a infinitly thin disc is returned.
           The forward scattering I0 needs to be multiplied by a length to have conventional units.
    shellSLD : list of float/list
        Scattering length density of shells in nm^-2.
        A shell can be divided in sub shells if instead of a single float a list of floats is given.
        These list values are used as scattering length of equal thickness subshells.
        E.g. [1,2,[3,2,1]] results in the last shell with 3 subshell of equal thickness.
        The sum of subshell thickness is the thickness given in shellthickness. See second example.
        SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2
    solventSLD : float
        Scattering length density of surrounding solvent in nm^-2.
        D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2
    alpha : float, [float,float] , unit rad
        Orientation, angle between the cylinder axis and the scattering vector q.
        0 means parallel, pi/2 is perpendicular
        If alpha =[start,end] is integrated between start,end
        start > 0, end < pi/2
    nalpha : int, default 30
        Number of points in Gauss integration along alpha.

    Returns
    -------
    dataArray
        Columns [q ,Iq ]
         - .outerDiscVolume
         - .radii
         - .alpha
         - .discthickness
         - .shellSLD
         - .solventSLD
         - .modelname


    Examples
    --------
    Alternating shells with different thickness 0.3 nm h2o and 0.2 nm d2o in vacuum::

     import jscatter as js
     import numpy as np
     x=np.r_[0.0:10:0.01]
     ashell=js.ff.multiShellDisc(x,[0.6,0.4]*2,[0.4,0.6]*2,[-0.56e-4,6.39e-4]*2)
     p=js.grace()
     p[0].plot(ashell)
     bshell=js.ff.multiShellDisc(x,2,2,6.39e-4)
     p[0].plot(bshell)
     p[0].yaxis(label='I(q)',scale='l',min=1e-8,max=0.001)
     p[0].xaxis(label='q / nm\S-1',scale='l',min=0.05,max=10)
     #p.save(js.examples.imagepath+'/multiShellDisc.jpg')

    .. image:: ../../examples/images/multiShellDisc.jpg
     :align: center
     :width: 50 %
     :alt: multiShellDisc

    References
    ----------
    .. [1] Guinier, A. and G. Fournet, "Small-Angle Scattering of X-Rays", John Wiley and Sons, New York, (1955)


    """
    if alpha is None:
        alpha = [0, np.pi / 2]
    if isinstance(shellSLD, numbers.Number):
        shellSLD = [shellSLD]
    if isinstance(shellthickness, numbers.Number):
        shellthickness = [shellthickness]
    if isinstance(radialthickness, numbers.Number):
        radialthickness = [radialthickness]
    if len(shellSLD) != len(shellthickness):
        raise Exception('shellSLD and shellthickness should be of same length but got:%i!=%i'
                        % (len(shellSLD), len(shellthickness)))
    Q = np.atleast_1d(q)
    shelld = []  # list of shellthicknesses
    radii = []  # list of radii
    SLDs = []  # constant scattering length density of inner to outer
    for i, sld in enumerate(shellSLD):
        if isinstance(sld, numbers.Number):  # a normal constant shell only ffsph will be used
            shelld.append(abs(shellthickness[i]))
            radii.append(abs(radialthickness[i]))
            SLDs.append(sld)
        else:  # a shell with steps
            shelld.append([abs(shellthickness[i]) / (len(sld) - 1)] * (len(sld) - 1))
            radii.append([abs(radialthickness[i]) / (len(sld) - 1)] * (len(sld) - 1))
            SLDs.append(sld[:-1])
    SLDs = np.hstack(SLDs)
    shelld = np.cumsum(np.hstack([shelld[0] * 0.5, shelld[1:]]) * 2)
    radii = np.cumsum(np.hstack(radii))
    # subtract solvent to have in any case the contrast to the solvent
    dSLDs = SLDs - solventSLD

    # test if alpha is angle or range
    if isinstance(alpha, (list, set, tuple)) and alpha[0] == alpha[1]:
        alpha = alpha[0]
    if isinstance(alpha, numbers.Number):
        # single angle
        result = _fq_disc(Q, radii, shelld, alpha,dSLDs)
    else:
        # integrate over range
        alpha[1] = min(alpha[1], np.pi / 2.)
        alpha[0] = max(alpha[0], 0.)
        w = np.c_[0:np.pi / 2:90j, np.sin(np.r_[0:np.pi / 2:90j])].T
        result = formel.parQuadratureFixedGauss(_fq_disc, alpha[0], alpha[1], 'angle', weights=w,
                                                n=nalpha, QQ=Q, R=radii, D=shelld, dSLDs=dSLDs)

    result.outerDiscVolume = np.pi * radii[-1] ** 2 * shelld[-1]
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.radii = radii[-1]
    result.discthickness = shelld
    result.alpha = alpha
    result.shellSLD = shellSLD
    result.solventSLD = solventSLD
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def disc(q, R, D, SLD, solventSLD=0, alpha=None):
    """
    Disc form factor .

    Parameters
    ----------
    q : array
        Wavevectors, units 1/nm
    R : float
        Radius in nm
    D : float
        Thickness of shell
    SLD,solventSLD : float
        Scattering length density in nm^-2.
    alpha : float, [float,float] , unit rad
        Orientation, angle between the cylinder axis and the scattering vector q.
        0 means parallel, pi/2 is perpendicular
        If alpha =[start,end] is integrated between start,end
        start > 0, end < pi/2

    Notes
    -----

    See multiShellCylinder

    """
    if alpha is None:
        alpha = [0, np.pi / 2]
    return multiShellCylinder(q, D, [R], [SLD], solventSLD=solventSLD, alpha=alpha)


# noinspection PyIncorrectDocstring
def cylinder(q, L, radius, SLD=1e-3, solventSLD=0, alpha=None, nalpha=90, h=None):
    r"""
    Cylinder form factor including cap.

    Based on multiShellCylinder (see there for detailed description of parameters).

    Parameters
    ----------
    L : float
        Length in nm.
    radius : float
        Radius in nm.
    h : float
        Cap geometry

    Notes
    -----
    Compared to SASview (5.0) this yields a factor 2 less intensity.
    Correctness can be checked as the forward scattering .I0 is independent of orientation
    and should be equal V² (V is volume) if SLD=1 and solvent SLD=0.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,8,500)
     p=js.grace()
     p.multi(1,2)
     R=2
     for L in [20,40,150]:
         cc=js.ff.cylinder(q,L=L,radius=R)
         p[0].plot(cc,li=-1,sy=0,le='L ={0:.0f} R={1:.1f}'.format(L,R))
     L=60
     for R in [1,2,4]:
         cc=js.ff.cylinder(q,L=L/R**2,radius=R)
         p[1].plot(cc,li=-1,sy=0,le='L ={0:.2f} R={1:.1f}'.format(L/R**2,R))
     p[0].yaxis(label='I(q)',scale='l',min=1e-6,max=10)
     p[0].xaxis(label='q / nm\S-1',scale='l',min=0.01,max=6)
     p[1].yaxis(label='I(q)',scale='l',min=1e-7,max=1)
     p[1].xaxis(label='q / nm\S-1',scale='l',min=0.01,max=6)
     p[1].text(r'forward scattering I0\n=(SLD*L\xp\f{}R\S2\N)\S2\N = 0.035530',x=0.02,y=0.1)
     p.title('cylinder')
     p[0].legend(x=0.012,y=0.001)
     p[1].legend(x=0.012,y=0.0001)
     #p.save(js.examples.imagepath+'/cylinder.jpg')

    .. image:: ../../examples/images/cylinder.jpg
     :align: center
     :width: 50 %
     :alt: cylinder

    References
    ----------
    .. [1] Guinier, A. and G. Fournet, "Small-Angle Scattering of X-Rays", John Wiley and Sons, New York, (1955)
    .. [2] http://www.ncnr.nist.gov/resources/sansmodels/Cylinder.html

    """
    if alpha is None:
        alpha = [0, np.pi / 2]
    return multiShellCylinder(q, L, [radius], [SLD], h=h, solventSLD=solventSLD, alpha=alpha, nalpha=nalpha)


def fuzzyCylinder(q, L, radius, sigmasurf, SLD=1e-3, solventSLD=0, alpha=None, nalpha=90):
    r"""
    Cylinder with a fuzzy surface as in fuzzySphere averaged over axis orientations.

    Parameters
    ----------
    q : array
        Wavevectors, units 1/nm
    L : float
        Length of cylinder, units nm.
        L=0 infinite cylinder.
    radius : float
        Radius of the cylinder in nm.
    sigmasurf : float
        Sigmasurf is the width of the smeared particle surface in units nm.
    SLD : float, default about SiO2 in H2O
        Scattering length density of cylinder in nm^-2.
        SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2
    solventSLD : float
        Scattering length density of surrounding solvent in nm^-2.
        D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2
    alpha : float, [float,float], default [0,pi/2]
        Orientation, angle between the cylinder axis and the scattering vector q in units rad.
        0 means parallel, pi/2 is perpendicular
        If alpha =[start,end] is integrated between start,end
        start > 0, end < pi/2
    nalpha : int, default 30
        Number of points in Gauss integration along alpha.

    Returns
    -------
    dataArray
        Columns [q ,Iq ]
         - .cylinderVolume
         - .radius
         - .cylinderLength
         - .alpha
         - .SLD
         - .solventSLD
         - .modelname

    Notes
    -----


    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,5,500)

     p=js.grace()
     for sig in [0.1,0.5,1]:
         fc=js.ff.fuzzyCylinder(q,L=100,radius=5,sigmasurf=sig)
         p[0].plot(fc,le='fuzzy layer sig={0:.1f}'.format(sig))
     cc=js.ff.cylinder(q,L=100,radius=5)
     p.plot(cc,li=[1,1,4],sy=0,le='cylinder')
     p.yaxis(label='I(q)',scale='l',min=1e-4,max=1e2)
     p.xaxis(label='q / nm\S-1',scale='l',min=0.01,max=6)
     p.title('fuzzy cylinder')
     p.legend(x=0.012,y=1)
     #p.save(js.examples.imagepath+'/fuzzyCylinder.jpg')

    .. image:: ../../examples/images/fuzzyCylinder.jpg
     :align: center
     :width: 50 %
     :alt: multiShellCylinder


    References
    ----------
    The models is derived from the fuzzy sphere model.
    Similar is used in for the core in

    .. [1] Lund et al, Soft Matter, 2011, 7, 1491

    """
    if alpha is None:
        alpha = [0, np.pi / 2]
    Q = np.atleast_1d(q)
    dSLD = SLD - solventSLD  # contrast

    def _ff(QQ, r, L, angle, sig):
        # formfactor of a cylinder with orientation angle alpha
        QQ0 = np.r_[0, QQ]
        Pc = dSLD * _fa_cylinder(QQ0, np.r_[r], L, angle)[:, 0] * np.exp(-sig ** 2 * QQ0 ** 2 / 2.) ** 2
        result = dA(np.c_[QQ, Pc[1:] ** 2].T)
        # store the forward scattering
        result.I0 = Pc[0] ** 2
        return result

    # test if alpha is angle or range
    if isinstance(alpha, (list, set, tuple)) and alpha[0] == alpha[1]:
        alpha = alpha[0]

    if isinstance(alpha, numbers.Number):
        # single angle
        result = _ff(Q, radius, L, alpha, sig=sigmasurf)
    else:
        # integrate over range
        alpha[1] = min(alpha[1], np.pi / 2.)
        alpha[0] = max(alpha[0], 0.)
        w = np.c_[0:np.pi / 2:90j, np.sin(np.r_[0:np.pi / 2:90j])].T
        result = formel.parQuadratureFixedGauss(_ff, alpha[0], alpha[1], 'angle', weights=w,
                                                n=nalpha, QQ=Q, r=radius, L=L, sig=sigmasurf)

    result.cylinderVolume = np.pi * radius ** 2 * L
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.radius = radius
    result.cylinderLength = L
    result.alpha = alpha
    result.SLD = SLD
    result.solventSLD = solventSLD
    result.sigmasurf = sigmasurf
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _fa_cylinder(q, r, L, angle):
    """
    cylinder form factor amplitude, save for q=0 and q<0 result is zero

    q : wavevectors
    r : shell thickness , a list or array !!
    L : length of cylinder, L=0 is infinitely long cylinder
    angle : angle between axis and scattering vector q in rad

    q<0 result is zero needed in ellipsoidFilledCylinder

    """
    # deal with possible zero in q
    if isinstance(q, numbers.Number):
        q = np.r_[q]
    result = np.zeros((len(q), len(r)))
    if angle != 0:
        sina = np.sin(angle)
        cosa = np.cos(angle)
    else:
        sina = 1
        cosa = 1
    if L > 0 and r[0] > 0:
        fq0 = 2. * np.pi * r ** 2 * L
        fqq = lambda qq: fq0 * special.j1(qq[:, None] * r * sina) / (qq[:, None] * r * sina) * \
                         np.sinc(qq[:, None] * L / 2. * cosa / np.pi)
    elif r[0] > 0:
        fq0 = 2. * np.pi * r ** 2 * 1
        fqq = lambda qq: fq0 * special.j1(qq[:, None] * r * sina) / (qq[:, None] * r * sina)
    elif L > 0:
        fq0 = 2. * L
        fqq = lambda qq: fq0 * np.sinc(qq[:, None] * L / 2. * cosa / np.pi)
    result[np.where(q > 0)[0], :] = fqq(q[np.where(q > 0)])
    result[np.where(q == 0)[0], :] = fq0 * 0.5
    return result


def _fa_cylindercap(q, r, L, angle, h, n=21):
    # Equ 1 in Kaya & Souza  J. Appl. Cryst. (2004). 37, 508±509  DOI: 10.1107/S0021889804005709
    # integrate by fixed Gaussian at positions t and weights w
    j1 = special.j1
    x, w = formel._cached_p_roots(n)
    x = np.real(x)
    if isinstance(q, numbers.Number):
        q = np.r_[q]
    if angle != 0:
        sina = np.sin(angle)
        cosa = np.cos(angle)
    else:
        sina = 1
        cosa = 1
    R = (h ** 2 + r ** 2) ** 0.5
    lowlimit = -h / R
    uplimit = 1
    t = ((uplimit - lowlimit) * (x[:, None, None] + 1) / 2.0 + lowlimit)  # first axis for x
    result = np.zeros((len(t), len(q), len(r)))
    cap = lambda q: 4 * np.pi * r ** 3 * np.cos(q[:, None] * cosa * (r * t + h + L / 2)) * \
                    (1 - t ** 2) * (j1(q[:, None] * r * sina * (1 - t ** 2) ** 0.5)) / \
                    (q[:, None] * r * sina * (1 - t ** 2) ** 0.5)
    cap0 = 4 * np.pi * r ** 3 * (1 - t ** 2)

    result[:, np.where(q > 0)[0], :] = (uplimit - lowlimit) / 2.0 * cap(q[np.where(q > 0)])
    result[:, np.where(q == 0)[0], :] = (uplimit - lowlimit) / 2.0 * cap0 * 0.5

    # multiply by weight and sum over weights
    return (result * w[:, None, None]).sum(axis=0)


def _fa_capedcylinder(QQ0, r, L, angle, h, dSLDs, ncap):
    # formfactor amplitude of a cylinder with orientation alpha and cap
    # outer integration boundary r
    # L cylinder length, angle orientation
    #  h position of cap
    # dSLDs contrast for multi shells,
    # ncap integration steps for cap
    # the functions _fa_ return arrays for all Q (axis 0) and all shells (axis 1)

    # calc outer cylinders
    Pc = dSLDs * _fa_cylinder(QQ0, r, L, angle)
    if h is not None and np.all(r > 0):
        # calc cap contribution
        Pcap = dSLDs * _fa_cylindercap(QQ0, r, L, angle, h, ncap)
    if len(r) > 1:
        # subtract inner cylinders that shell remains
        #  inner most with r==0 is not subtracted
        Pc[:, 1:] = Pc[:, 1:] - dSLDs[1:] * _fa_cylinder(QQ0, r[:-1], L, angle)
        if h is not None and np.all(r > 0):
            # calc cap contribution
            Pcap[:, 1:] = Pcap[:, 1:] - dSLDs[1:] * _fa_cylindercap(QQ0, r[:-1], L, angle, h, ncap)

    # sum up all cylinder shells with axis=1
    if h is not None and np.all(r > 0):
        # this avoids the infinite thin disc to be added
        if L > 0:
            Pcs = (Pc + Pcap).sum(axis=1)
        else:
            Pcs = Pcap.sum(axis=1)
    else:
        # cylinder without cap
        Pcs = Pc.sum(axis=1)
    # return scattering amplitude
    return Pcs


def _fq_capedcylinder(QQ, r, L, angle, h, dSLDs, ncap):
    # calc scattering amplitude and square it for formfactor
    # include zero for forward scattering
    fa = _fa_capedcylinder(np.r_[0, QQ], r, L, angle, h, dSLDs, ncap)
    result = dA(np.c_[QQ, fa[1:]**2].T)
    # store the forward scattering
    result.I0 = fa[0]**2
    return result


def multiShellCylinder(q, L, shellthickness, shellSLD, solventSLD=0, alpha=None, h=None, nalpha=60, ncap=31):
    r"""
    Multi shell cylinder with caps in solvent averaged over axis orientations.

    Each shell has a constant SLD and may have a cap with same SLD sequence.
    Caps may be globular (barbell) or small (like lenses).
    For zero length L a lens shaped disc or  a double sphere like shape is recovered.

    Parameters
    ----------
    q : array
        Wavevectors, units 1/nm
    L : float
        Length of cylinder, units nm
        L=0 infinite cylinder if h=None.
    shellthickness : list of float or float, all >0
        Thickness of shells in sequence, units nm.
        radii r=cumulativeSum(shellthickness)
    shellSLD : list of float/list
        Scattering length density of shells in nm^-2.
        A shell can be divided in sub shells if instead of a single float a list of floats is given.
        These list values are used as scattering length of equal thickness subshells.
        E.g. [1,2,[3,2,1]] results in the last shell with 3 subshell of equal thickness.
        The sum of subshell thickness is the thickness given in shellthickness. See second example.
        SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2
    solventSLD : float
        Scattering length density of surrounding solvent in nm^-2.
        D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2
    h : float, default=None
        Geometry of the caps with cap radii R=(r**2+h**2)**0.5
        h is distance of cap center with radius R from the flat cylinder cap and r as radii of the cylinder shells.

        - None No caps, flat ends as default.
        - 0 cap radii equal cylinder radii (same shellthickness as cylinder shells)
        - >0 cap radius larger cylinder radii as barbell
        - <0 cap radius smaller cylinder radii as lens caps
    alpha : float, [float,float] , unit rad
        Orientation, angle between the cylinder axis and the scattering vector q.
        0 means parallel, pi/2 is perpendicular
        If alpha =[start,end] is integrated between start,end
        start > 0, end < pi/2
    nalpha : int, default 30
        Number of points in Gauss integration along alpha.
    ncap : int, default=31
        Number of points in Gauss integration for cap.

    Returns
    -------
    dataArray
        Columns [q ,Iq ]
         - .outerCylinderVolume
         - .Radius
         - .cylinderLength
         - .alpha
         - .shellthickness
         - .shellSLD
         - .solventSLD
         - .modelname
         - .contrastprofile
         - .capRadii

    Notes
    -----
    Multishell  cylinders of type:

    .. table::
        :align: left

        ============================== ===============================
        flat cap                       L>0, radii>0, h=None
        lens cap                       L>0, radii>0, h<0
        lens cap, R=r                  L>0, radii>0, h=0
        barbell, globular cap          L>0, radii>0, h>0
        lens, no cylinder              L=0, radii>0, h<0
        barbell, no cylinder           L=0, radii>0, h>0
        infinite flat disc             L=0. h=None
        ============================== ===============================

    .. image:: barbell.png
     :align: center
     :height: 150px
     :alt: Image of barbell

    Compared to SASview this yields a factor 2 less. See :py:func:`~.ff.cylinder`

    Examples
    --------
    Alternating shells with different thickness 0.3 nm h2o and 0.2 nm d2o in vacuum::

     import jscatter as js
     import numpy as np
     x=np.r_[0.0:10:0.01]
     ashell=js.ff.multiShellCylinder(x,20,[0.4,0.6]*5,[-0.56e-4,6.39e-4]*5)
     #plot it
     p=js.grace()
     p.new_graph(xmin=0.24,xmax=0.5,ymin=0.2,ymax=0.5)
     p[0].plot(ashell)
     p[0].yaxis(label='I(q)',scale='l',min=1e-7,max=1)
     p[0].xaxis(label='q / nm\S-1',scale='l',min=0.05,max=10)
     p[1].plot(ashell.contrastprofile,li=1) # a contour of the SLDs
     p[1].subtitle('contrastprofile')
     p[0].title('alternating shells')
     #p.save(js.examples.imagepath+'/multiShellCylinder.jpg')

    .. image:: ../../examples/images/multiShellCylinder.jpg
     :align: center
     :width: 50 %
     :alt: multiShellCylinder

    Double shell with exponential decreasing exterior shell to solvent scattering::

     import jscatter as js
     import numpy as np
     x=np.r_[0.0:10:0.01]
     def doubleexpshells(q,L,d1,d2,e3,sd1,sd2,sol):
        # The third layer will have 9 subshells with combined thickness of e3.
        # The scattering length decays to e**(-3) in last subshell.
        return js.ff.multiShellCylinder(q,L,[d1,d2,e3],[sd1,sd2,((sd2-sol)*np.exp(-np.r_[0:3:9j])+sol)],solventSLD=sol)
     dde=doubleexpshells(x,10,0.5,0.5,3,1e-4,2e-4,0)
     #plot it
     p=js.grace()
     p.multi(2,1)
     p[0].plot(dde)
     p[1].plot(dde.contrastprofile,li=1) # a contour of the SLDs

    Cylinder with cap::

     x=np.r_[0.1:10:0.01]
     p=js.grace()
     p.title('Comparison of dumbbell cylinder with simple models')
     p.subtitle('thin lines correspond to simple models as sphere and dshell sphere')
     p.plot(js.ff.multiShellCylinder(x,0,[10],[1],h=0),sy=[1,0.5,2],le='simple sphere')
     p.plot(js.ff.sphere(x,10),sy=0,li=1)
     p.plot(js.ff.multiShellCylinder(x,0,[2,1],[1,2],h=0),sy=[1,0.5,3],le='double shell sphere')
     p.plot(js.ff.multiShellSphere(x,[2,1],[1,2]),sy=0,li=1)
     p.plot(js.ff.multiShellCylinder(x,10,[3],[20],h=-5),sy=[1,0.5,4],le='thin lens cap cylinder=flat cap cylinder')
     p.plot(js.ff.multiShellCylinder(x,10,[3],[20],h=None),sy=0,li=[1,2,1],le='flat cap cylinder')
     p.plot(js.ff.multiShellCylinder(x,10,[3],[20],h=-0.5),sy=0,li=[3,2,6],le='thick lens cap cylinder')
     p.yaxis(scale='l')
     p.xaxis(scale='l')
     p.legend(x=0.15,y=0.01)

    References
    ----------
    Single cylinder

    .. [1] Guinier, A. and G. Fournet, "Small-Angle Scattering of X-Rays", John Wiley and Sons, New York, (1955)
    .. [2] http://www.ncnr.nist.gov/resources/sansmodels/Cylinder.html

    Double cylinder

    .. [3] Use of viscous shear alignment to study anisotropic micellar structure by small-angle neutron scattering,
           J. B. Hayter and J. Penfold J. Phys. Chem., 88:4589--4593, 1984
    .. [4] http://www.ncnr.nist.gov/resources/sansmodels/CoreShellCylinder.html

    Barbell, cylinder with small end-caps, circular lens

    .. [5] Scattering from cylinders with globular end-caps
           Kaya (2004). J. Appl. Cryst. 37, 223-230]     DOI: 10.1107/S0021889804000020
           Scattering from capped cylinders. Addendum
           H. Kaya and Nicolas-Raphael de Souza
           J. Appl. Cryst. (2004). 37, 508-509  DOI: 10.1107/S0021889804005709

    """
    if alpha is None:
        alpha = [0, np.pi / 2]
    if isinstance(shellSLD, numbers.Number): shellSLD = [shellSLD]
    if isinstance(shellthickness, numbers.Number): shellthickness = [shellthickness]
    if len(shellSLD) != len(shellthickness):
        raise Exception('shellSLD and shellthickness should be of same length but got:%i!=%i'
                        % (len(shellSLD), len(shellthickness)))
    Q = np.atleast_1d(q)
    shelld = []  # list of shellthicknesses
    SLDs = []  # constant scattering length density of inner radius to outer radius of shell
    for i, sld in enumerate(shellSLD):
        if isinstance(sld, numbers.Number):  # a normal constant shell only ffsph will be used
            shelld.append(abs(shellthickness[i]))
            SLDs.append(sld)
        else:  # a shell with lin progress
            shelld.append([abs(shellthickness[i]) / (len(sld) - 1)] * (len(sld) - 1))
            SLDs.append(sld[:-1])
    SLDs = np.hstack(SLDs)
    shelld = np.hstack(shelld)
    radii = np.cumsum(shelld)
    # subtract solvent to have in any case the contrast to the solvent
    dSLDs = SLDs - solventSLD

    # here we do the formfactor integration in _fq_capedcylinder
    # test if alpha is angle or range
    if isinstance(alpha, (list, set, tuple)) and alpha[0] == alpha[1]:
        alpha = alpha[0]
    if isinstance(alpha, numbers.Number):
        # single angle
        result = _fq_capedcylinder(Q, radii, L, alpha, h, dSLDs, ncap)
    else:
        # integrate over range
        alpha[1] = min(alpha[1], np.pi / 2.)
        alpha[0] = max(alpha[0], 0.)
        w = np.c_[0:np.pi / 2:90j, np.sin(np.r_[0:np.pi / 2:90j])].T
        result = formel.parQuadratureFixedGauss(_fq_capedcylinder, alpha[0], alpha[1], 'angle', weights=w,
                                                n=nalpha, QQ=Q, r=radii, L=L, h=h, dSLDs=dSLDs, ncap=ncap)

    result.outerCylinderVolume = np.pi * radii[-1] ** 2 * L
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.Radius = radii[-1]
    result.cylinderLength = L
    result.alpha = alpha
    result.shellthickness = np.abs(shellthickness)
    result.shellSLD = shellSLD
    result.solventSLD = solventSLD
    if h is not None:
        result.capRadii = radii * (1 + h ** 2) ** 0.5
        if h != 0:
            result.capRadii *= np.sign(h)
    contrastprofile = np.c_[np.r_[radii - shelld, radii], np.r_[SLDs, SLDs]].T
    result.contrastprofile = contrastprofile[:,
                             np.repeat(np.arange(len(SLDs)), 2) + np.tile(np.r_[0, len(SLDs)], len(SLDs))]
    result.modelname = inspect.currentframe().f_code.co_name
    return result


#: incomplete Gamma function
_iG = lambda a, x: special.gamma(a) * special.gammainc(a, x)


def gaussianChain(q, Rg, nu=0.5):
    r"""
    General formfactor of a gaussian polymer chain with excluded volume parameter.

    For nu=0.5 this is the Debye model for Gaussian chain in theta solvent.
    nu>0.5 for good solvents,nu<0.5 for bad solvents.
    For absolute scattering see introduction :ref:`formfactor (ff)`.

    Parameters
    ----------
    q : array
        Scattering vector, unit eg  1/A or 1/nm
    Rg : float
        Radius of gyration,  units in 1/unit(q)
    nu : float, default=0.5
        ν is the excluded volume parameter,
        which is related to the Porod exponent d as ν = 1/d and [5/3 <= d <= 3].

    Returns
    -------
    dataArray
        Columns [q,Fq]
         - .radiusOfGyration
         - .nu excluded volume parameter

    Notes
    -----
     - :math:`Rg^2=l^2 N^{2\nu}` with monomer length l and monomer number N.
     - calcs

       .. math:: F(Q) = \frac{1}{\nu U^{\frac{1}{2\nu}}} \gamma_{inc}(\frac{1}{2\nu}, U) -
                        \frac{1}{\nu U^{\frac{1}{\nu}}} \gamma_{inc}(\frac{1}{\nu}, U)

       with :math:`U=(qR_g)^2` and :math:`\gamma_{inc}` as lower incomplete gamma function.
     - The absolute scattering is proportional to :math:`b^2 N^2=b^2 (R_g/l)^{1/\nu}` with monomer number :math:`N`
       and monomer scattering length :math:`b`.
     - From [1]_: "Note that this model describing polymer chains with excluded volume applies only in
       the mass fractal range ([5/3 <= d <= 3]) and does not apply to surface fractals ([3 < d < 4]).
       It does not reproduce the rigid-rod limit (d = 1) because it assumes chain flexibility from the outset,
       nor does it describe semi-flexible chains ([1 < d < 5/3]). "
     - This model should be favoured compared to the Beaucage model as it is not an artificial
       connection between two regimes.


    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.1,8,100)
     p=js.grace()
     for nu in np.r_[0.3:0.61:0.05]:
        iq=js.ff.gaussianChain(q,2,nu)
        p.plot(iq,le='nu= $nu')
     p.yaxis(label='I(q)',scale='l',min=1e-3,max=1)
     p.xaxis(label='q / nm\S-1',scale='l')
     p.legend(x=0.2,y=0.1)
     p.title('Gaussian chains')
     #p.save(js.examples.imagepath+'/gaussianChain.jpg')

    .. image:: ../../examples/images/gaussianChain.jpg
     :align: center
     :width: 50 %
     :alt: gaussianChain

    References
    ----------
    .. [1] Analysis of the Beaucage model
            Boualem Hammouda  J. Appl. Cryst. (2010). 43, 1474–1478
            http://dx.doi.org/10.1107/S0021889810033856
    .. [2] SANS from homogeneous polymer mixtures: A unified overview.
           Hammouda, B. in Polymer Characteristics 87–133 (Springer-Verlag, 1993). doi:10.1007/BFb0025862


    """

    nu2 = nu * 2.
    q = np.atleast_1d(q)
    U = q ** 2 * Rg ** 2 * (nu2 + 1) * (nu2 + 2) / 6.
    gu = lambda x: 1 / (nu * x ** (1. / nu2)) * _iG(1 / nu2, x) - 1 / (nu * x ** (1. / nu)) * _iG(1 / nu, x)
    res = np.piecewise(U, [U == 0], [1, gu])
    result = dA(np.c_[q, res].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.radiusOfGyration = Rg
    result.nu = nu
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def ringPolymer(q, Rg):
    r"""
    General formfactor of a polymer ring in theta solvent.

    For absolute scattering see introduction :ref:`formfactor (ff)`.

    Parameters
    ----------
    q : array
        Scattering vector, unit eg  1/A or 1/nm
    Rg : float
        Radius of gyration,  units in 1/unit(q)

    Returns
    -------
    dataArray
        Columns [q,Fq]
         - .radiusOfGyration

    Notes
    -----
    Equ. 26 from [1]_ (or see equ. 3.5 in [2]_ shows in short form related to the Dawson function)

    .. math:: S(Q) = dawsn(U)/U = \frac{e^{-U^2}}{U} \int_0^U e^{t^2}

    with :math:`U=(q^2R_g^2)^{1/2}/2`

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.1,8,100)
     p=js.grace()
     p.multi(1,2)
     iq=js.ff.ringPolymer(q,5)
     p[0].plot(iq)
     p[0].yaxis(scale='l',label='I(q) / a.u.')
     p[0].xaxis(scale='l',label='q / nm\S-1')
     p[1].plot(iq.X,iq.Y*iq.X**2)
     p[1].yaxis(scale='l',label=[r'I(q)q\S2\N / a.u.',1,'opposite'],ticklabel=['power',0,1,'opposite'],min=1e-2,max=0.2)
     p[1].xaxis(scale='l',label='q / nm\S-1')
     p[1].legend(x=0.2,y=0.5)
     p[1].subtitle('Kratky plot')
     p[0].subtitle('ring polymer')
     #p.save(js.examples.imagepath+'/ringPolymer.jpg')

    .. image:: ../../examples/images/ringPolymer.jpg
     :align: center
     :width: 50 %
     :alt: ringPolymer

    References
    ----------
    .. [1] Some statistical properties of flexible ring polymers
           Edward F. Casassa
           JOURNAL OF POLYMER SCIENCE: PART A, 3, 605-614 (1965)
           https://doi.org/10.1002/pol.1965.100030217
    .. [2] SANS from homogeneous polymer mixtures: A unified overview.
           Hammouda, B. in Polymer Characteristics 87–133 (Springer-Verlag, 1993). doi:10.1007/BFb0025862

    """
    U = q * Rg / 2.
    res = special.dawsn(U) / U
    result = dA(np.c_[q, res].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.radiusOfGyration = Rg
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def wormlikeChain(q, N, a, R=None, SLD=1, solventSLD=0, rtol=0.02):
    r"""
    Scattering of a wormlike chain, which correctly reproduces the rigid-rod and random-coil limits.

    To calculate the scattering of the classical Kratky-Porod model of semiflexible chains we use an analytical solution
    for arbitrary stiffness and length as given by Kholodenko [1]_.
    The transition from infinite thin chain to a cross sectional scattering uses the decoupling approximation and the
    scattering cross section of an infinitly thin (optional multishell)disc.

    Parameters
    ----------
    q : array
        Wavevectors in 1/nm.
    N : float
        Length of the chain in units nm.
        Number of chain segments is N/l=N/(2a). We follow here the notation of [1]_.
    a : float
        Persistence length *a* with Kuhn length l=2a (segment length), units of nm.
    R : float
        Radius in units of nm.
    SLD : float
        Scattering length density segments.
    solventSLD :
        Solvent scattering length density.
    rtol : float
        Maximum relative tolerance in integration.

    Returns
    -------
    dataArray
        Columns [q, Iq]
         - .chainRadius
         - .chainLength
         - .persistenceLength
         - .Rg
         - .volume
         - .contrast
        For R=0 the normalized formfactor is returned.

    Notes
    -----
    We use equation 17 of [1]_ to calculate the normalized formfactor *S(q)* of a semiflexible thin polymer chain as
    it correctly recovers the limit of rigid rod and flexible chain (for details see [1]_).

    .. math:: S_{wc}(q) =& \frac{2}{x}[I_1(x)-\frac{1}{x}I_2(x)]

        with\;       I_n =& \int_0^x z^{n-1}f(z) \;   and \;  x=\frac{3N}{2a}

                     k<=& 3/2a : \; f(z) = \frac{1}{E} \frac{sinh(Ez)}{sinh(z)}

                     k>& 3/2a : \; f(z) = \frac{1}{\overline{E}} \frac{sinh(\overline{E}z)}{sinh(z)}

                    E^2 =& 1-(\frac{2}{3}ak) ;\; \overline{E}^2 = 1-(\frac{2}{3}ak)

    If the contour length is much larger than the cross section :math:`N>>R` then the cross section scattering can be
    separated. Within a decoupling approximation [4]_ we may use an infinitly thin disc formfactor :math:`S_{disc}(q)`
    oriented perpendicular to the chain.
    This can be calculated as homogeneous thin disc (included in using R>0) or as multi shell disc
    using *multiShellDisc* (see third example).

    .. math:: F(q) = S_{wc}(q,R=0,...) N S_{disc}(q,D=0,alpha=\pi/2,...)

    The forward scattering :math:`I_0` for a homogeneous cylinder is :math:`I_0=V^2(SLD-solventSLD)^2`
    with :math:`V=\pi R^2 N`.
    For multishellDisc(..,D=0,alpha=\pi/2,..).I0 the result has to be multiplied by the contour length *N*.

    .Rg is calculated according to equ 20 in [2]_ and similar is found in [3]_ with l=2a.

    .. math:: R_g^2 = \frac{lN}{6}\big( 1-\frac{3l}{2N}+\frac{3l^2}{2N^2}-\frac{3l^3}{4N^3}(1-e^{-2N/l}) \big)

    From [1]_ :
        The Kratky plot (Figure 4 ) is not the most convenient
        way to determine *a* as was pointed out in ref 20. Figure
        5 provides an alternative way of measuring a by plotting
        the experimentally measurable combination Nk2S(k)
        versus a for fixed wavelength k. As Figure 5 indicates,
        this plot is rather insensitive to the chain length N and
        therefore is universal. The numerical analysis of eq 17
        shows that this remains true for as long as k is not too
        small. Taking into account that the excluded-volume
        effects leave S(k) practically unchanged (e.g., see Figures
        2 and 4 of ref 231, the plot of Figure 5 can serve as a useful
        alternative to the Kratky plot which, in addition, does not
        suffer from the polydispersity effects


    Examples
    --------
    ::

     import jscatter as js
     p=js.grace()
     p.multi(2,1)
     p.title('figure 3 (2 scaled) of ref Kholodenko Macromolecules 26, 4179 (1993)',size=1)
     q=js.loglist(0.01,10,100)
     for a in [1,2.5,5,20,50,1000]:
         ff=js.ff.wormlikeChain(q,200,a)
         p[0].plot(ff.X,200*ff.Y*ff.X**2,legend='a=%.4g' %ff.persistenceLength)
         p[1].plot(ff.X,ff.Y,legend='a=%.4g' %ff.persistenceLength)
     p[0].legend()
     p[0].yaxis(label=r'Nk\S2\NS(k)')
     p[1].xaxis(label='k',scale='l')
     p[1].yaxis(label='S(k)',scale='l')
     #p.save(js.examples.imagepath+'/wormlikeChain.jpg')

    .. image:: ../../examples/images/wormlikeChain.jpg
     :align: center
     :width: 50 %
     :alt: wormlikeChain

    ::

     import jscatter as js
     p=js.grace()
     p.multi(2,1)
     p.title('figure 4 of ref Kholodenko Macromolecules 26, 4179 (1993)',size=1)
     # fig 4 seems to be wrong scale in [1]_ as for large N with a=1 fig 2 and 4 should have same plateau.
     a=1
     q=js.loglist(0.01,4./a,100)
     for NN in [1,20,50,150,500]:
         ff=js.ff.wormlikeChain(q,NN,a)
         p[0].plot(ff.X*a,NN*a*ff.Y*ff.X**2,legend='N=%.4g' %ff.chainLength)
         p[1].plot(ff.X,ff.Y,legend='a=%.4g' %ff.persistenceLength)
     p[0].legend()
     p[0].yaxis(label=r'(N/a)(ka)\S2\NS(k)')
     p[0].xaxis(label='ka')
     p[1].xaxis(label='k',scale='l')
     p[1].yaxis(label='S(k)',scale='l')


    Micellar wormlike structure with core shell disc cross section   ::

     import jscatter as js
     import numpy as np
     def thickworm(q, N, a, Rcore, shellD, SLDcore=1, SLDshell=2, solventSLD=0):
        worm = js.ff.wormlikeChain(q, N, a, R=0)
        cross = js.ff.multiShellDisc(q, radialthickness=[Rcore,shellD], shellthickness=[0,0],
                                    shellSLD=[SLDcore,SLDshell], solventSLD=solventSLD, alpha=np.pi/2)
        worm.Y = worm.Y*N*cross.Y
        worm.volume = N*np.pi*(Rcore+shellD)**2
        worm.I0 = cross.I0*N
        return worm

     p=js.grace(1,0.7)
     p.title('Thick wormlike chain with coreshell cross section',size=1.5)
     p.subtitle('persistence length *a*')
     q=js.loglist(0.01,4,200)
     for a in [1,2.5,5,20,50,1000]:
         ff=thickworm(q,N=200,a=a, Rcore=3, shellD=1, SLDcore=0, SLDshell=1)
         p.plot(ff.X,ff.Y,legend='a=%.4g' %ff.persistenceLength)
     p.legend(x=0.03,y=1000)
     p.xaxis(label='q',scale='l',charsize=1.5)
     p.yaxis(label='S(q)',scale='l',charsize=1.5,min=1,max=3e5)
     #p.save(js.examples.imagepath+'/wormlikeChain2.jpg')

    .. image:: ../../examples/images/wormlikeChain2.jpg
     :align: center
     :width: 50 %
     :alt: worm

    References
    ----------
    .. [1] Analytical calculation of the scattering function for polymers of arbitrary
           flexibility using the dirac propagator
           A. L. Kholodenko,
           Macromolecules, 26:4179--4183, 1993
    .. [2] The structure factor of a wormlike chain and the random-phase-approximation solution
           for the spinodal line of a diblock copolymer melt
           Zhang X et. al.
           Soft Matter 10, 5405 (2014), https://doi.org/10.1039/C4SM00374H
    .. [3] Models of Polymer Chains
           Teraoka I. in Polymer Solutions: An Introduction to Physical Properties
           pp: 1-67, New York, John Wiley & Sons, Inc.
           https://doi.org/10.1002/0471224510.ch1

    Decoupling approximation for cross section

    .. [4] Static structure factor of polymerlike micelles:Overall dimension,
           flexibility, and local properties of lecithin reverse micelles in deuterated isooctane
           Götz Jerke, Jan Skov Pedersen, Stefan Ulrich Egelhaaf, and Peter Schurtenberger
           Phys. Rev. E 56, 5772 ; https://doi.org/10.1103/PhysRevE.56.5772

    """
    a2 = 2. * float(a)  # Kuhn length
    q = np.atleast_1d(q)  # row vector
    limit = 100  # limit to avoid exp overflow
    x = 3 * N / a2
    z = np.c_[0:x:1000 * 1j]  # column vector

    EF = np.sqrt(np.sign((a2 * q / 3.)**2 - 1) * ((a2 * q / 3.) ** 2 - 1))
    EFiszero = (EF == 0)
    EF[EFiszero] = 1  # to avoid EF=0

    # fz is [ z , q ] matrix
    def FZ(qq, zz):
        mfz = np.zeros((zz.shape[0], qq.shape[0]))
        # now fill it
        mfz[(0 < zz) & (zz < limit) & (a2 * qq <= 3)] = (
                np.sinh(zz[(0 < zz) & (zz < limit), None] * EF[None, a2 * qq <= 3]) / np.sinh(
            zz[(0 < zz) & (zz < limit), None]) / EF[None, a2 * qq <= 3]).flatten()
        # for to large zz we avoid expz>limit and use sinh(EF*zz)/sinh(zz)=exp(zz*(Ef-1)) for zz>limit
        mfz[(zz >= limit) & (a2 * qq <= 3)] = (
                np.exp(zz[zz >= limit, None] * (EF[None, a2 * qq <= 3] - 1)) / EF[None, a2 * qq <= 3]).flatten()
        mfz[(0 < zz) & (zz < limit) & (a2 * qq > 3)] = (
                np.sin(zz[(0 < zz) & (zz < limit), None] * EF[None, a2 * qq > 3]) / np.sinh(
            zz[(0 < zz) & (zz < limit), None]) / EF[None, a2 * qq > 3]).flatten()
        # mfz[(zz>limit          ) & (a2*qq >3)] = 0    # default is zero
        # for zz=0  limes is  1 in both cases
        mfz[zz[:, 0] == 0, :] = 1
        if np.any(EFiszero):
            # catch fz  when EF is zero and assigned correct value
            mfz[(0 < zz) & (zz < limit) & EFiszero] = (
                    zz[(0 < zz) & (zz < limit)] / np.sinh(zz[(0 < zz) & (zz < limit)]))
        return mfz

    # integrate I1 and I2 from above matrix
    fz = FZ(q, z)
    I1 = scipy.integrate.simps(fz, z, axis=0)
    I2 = scipy.integrate.simps(fz * z, z, axis=0)
    P0 = 2. / x * (I1 - I2 / x)

    while True:
        # adaptive integration to increase accuracy stepwise
        nz = np.c_[0:x:(2 * len(z) - 1) * 1j]
        nfz = np.zeros((nz.shape[0], q.shape[0]))
        nfz[::2, :] = fz
        nfz[1::2, :] = FZ(q, nz[1::2])  # each second is new element
        I1 = scipy.integrate.simps(nfz, nz, axis=0)
        I2 = scipy.integrate.simps(nfz * nz, nz, axis=0)
        nP0 = 2. / x * (I1 - I2 / x)
        if max(abs(nP0 - P0) / abs(nP0)) < rtol:
            P0 = nP0
            break
        else:
            z = nz
            fz = nfz
            P0 = nP0
    # now do the volume and sld
    if R:  # not None or >0
        Pcs = (2 * special.j1(q * R) / q / R) ** 2
        V = np.pi * R * R * N
        sld = SLD - solventSLD
        I0 = V ** 2 * sld ** 2
    else:
        Pcs = 1
        R = 0
        V = 1
        sld = 1
        I0 = 1
    result = dA(np.c_[q, V ** 2 * sld ** 2 * P0 * Pcs].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.chainRadius = R
    result.chainLength = N
    result.I0 = I0
    result.persistenceLength = a
    # in [2]_ a is Kuhn length (here a2)
    result.Rg = np.sqrt(
        (a2 * N / 6.) * (1 - 1.5 * a2 / N + 1.5 * (a2 / N) ** 2 - 0.75 * (a2 / N) ** 3 * (1 - np.exp(-2 * N / a2))))
    result.volume = V
    result.contrast = sld
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _fq_cuboid(q, p, t, a, b, c):
    """scattering of cuboid

    Parameters
    ----------
    q : array wavevector
    p : array angle phi
    t: array angle theta
    a,b,c : float edge length
    """
    pi2 = np.pi * 2
    fa = (np.sinc(q * a * np.sin(t[:, None]) * np.cos(p[:, None]) / pi2) *
          np.sinc(q * b * np.sin(t[:, None]) * np.sin(p[:, None]) / pi2) *
          np.sinc(q * c * np.cos(t[:, None]) / pi2)) ** 2 * np.sin(t[:, None])
    return fa


def cuboid(q, a, b=None, c=None, SLD=1, solventSLD=0, N=30):
    r"""
    Formfactor of rectangular cuboid with different edge lengths.

    Parameters
    ----------
    q : array
        Wavevector in 1/nm
    a,b,c : float, None
        Edge length, for a=b=c its a cube, Units in nm.
        If b=None b=a.
        If c=None c=b.
    SLD : float, default =1
        Scattering length density of cuboid.unit nm^-2
        e.g. SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2 for neutrons
    solventSLD : float, default =0
        Scattering length density of solvent. unit nm^-2
        e.g. D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2 for neutrons
    N : int
        Order for Gaussian integration over both phi and theta.

    Returns
    -------
    dataArray
        Columns [q,Iq]
         - .I0 forward scattering
         - .edges
         - .contrast

    Notes
    -----

    .. math:: I(q)=\rho^2V_{cube}^2 \int_{0}^{2\pi}\int_{0}^{\pi} \lvert sinc(q_xa/2 )
              sinc(q_yb/2) sinc(q_zc/2)\rvert^2 \sin\theta d\theta d\phi

    with :math:`q = (q_x,q_y,q_z) = (q\sin\theta\cos\phi,q\sin\theta\sin\phi,q\cos\theta)`
    and contrast :math:`\rho` [1]_.

    In [1]_ the edge length is only half of it.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=np.r_[0.1:5:0.01]
     p=js.grace()
     p.plot(js.ff.cuboid(q,60,4,6))
     p.plot(js.ff.cuboid(q,10,4,60))
     p.plot(js.ff.cuboid(q,11,11,11),li=1)
     p.yaxis(scale='l',label='I(q)')
     p.xaxis(scale='l',label='q / nm\S-1')
     p.title('cuboid')
     #p.save(js.examples.imagepath+'/cuboid.jpg')

    .. image:: ../../examples/images/cuboid.jpg
     :width: 50 %
     :align: center
     :alt: cuboid


    References
    ----------
    .. [1] Analysis of small-angle scattering data from colloids and polymer solutions:
           modeling and least-squares fitting
           Pedersen, Jan Skov Advances in Colloid and Interface Science 70, 171 (1997)
           http://dx.doi.org/10.1016/S0001-8686(97)00312-6

    """
    if b is None:
        b = a
    if c is None:
        c = b
    sld = SLD - solventSLD
    V = a * b * c
    q = np.atleast_1d(q)

    # integrate by Gauss quadrature rule
    fq = formel.pQFGxD(_fq_cuboid, [0, 0], [np.pi/2, np.pi/2], ['p', 't'], q=q, a=a, b=b, c=c, n=N) * 8 / (4 * np.pi)

    I0 = V ** 2 * sld ** 2

    result = dA(np.c_[q, I0 * fq].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.I0 = I0
    result.edges = [a, b, c]
    result.contrast = sld
    return result


def pearlNecklace(Q, N, Rc=None, l=None, A1=None, A2=None, A3=None, ms=None, mr=None, vmonomer=None,
                  monomerlength=None):
    r"""
    Formfactor of a pearl necklace (freely jointed chain of pearls connected by rods)

    The formfactor is normalized to 1.
    For absolute scattering see introduction :ref:`formfactor (ff)`.

    Parameters
    ----------
    Q : array
        Wavevector in nm.
    Rc : float
        Pearl radius in nm.
    N : float
        Number of pearls (homogeneous spheres).
    l : float
        Physical length of the rods in nm
    A1, A2, A3 : float
        Amplitudes of pearl-pearl, rod-rod and pearl-rod scattering.
        Can be calculated with the number of chemical monomers in a pearl ms and rod mr
        (see below for further information)
        If ms and mr are given A1,A2,A3 are calculated from these.
    ms : float, default None
        Number of chemical monomers in each pearl.
    mr : float, default None
        Number of chemical monomers in rod like strings.
    vmonomer : float
        Monomer specific volume :math:`v_0` in cubic nm.
        Used to calculate Rc as :math:`Rc= (\frac{ms v_03}{4\pi})^{1/3}`.
        Increasing vmonomer compard to the bulk simulates swelling due to solvent inclusion.
    monomerlength : float
        Monomer length a in nm to calculate :math:`l=m_r a`.

    Returns
    -------
    dataArray
        Columns [q, Iq]
         - .pearlRadius
         - .A1 = ms²/(M*mr+N*ms)²
         - .A2 = mr²/(M*mr+N*ms)²
         - .A3 = (mr*ms)/(M*mr+N*ms)²
         - .numberPearls N
         - .numberRods M = (N-1) number of rod like strings
         - .mr
         - .ms
         - .stringLength
         - .numberMonomers : :math:`Nm_s + Mm_r`

    Notes
    -----

    Author: L. S. Fruhner, RB, FZJ Juelich 2016

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,5,300)
     p=js.grace()
     for l in [2,20,50]:
         p.plot(js.ff.pearlNecklace(q, Rc=2, N=5, ms=200-l, mr=l,monomerlength=0.1),le='l=$stringLength mr=$mr')
     p.yaxis(scale='l',label='I(q)',min=0.0001)
     p.xaxis(scale='l',label='q / nm\S-1')
     p.legend(x=0.2,y=0.01)
     p.title('pearl necklace with 5 parls')
     p.subtitle('increasing string length reducing pearls')
     #p.save(js.examples.imagepath+'/pearlNecklace.jpg')

    .. image:: ../../examples/images/pearlNecklace.jpg
     :width: 50 %
     :align: center
     :alt: pearlNecklace



    References
    ----------
    .. [1] Particle scattering factor of pearl necklace chains
           R. Schweins, K. Huber, Macromol. Symp., 211, 25-42, 2004.



    """

    N = np.float(N)  # always float
    M = N - 1
    if isinstance(ms, numbers.Number) and isinstance(mr, numbers.Number):
        A1 = ms ** 2 / (M * mr + N * ms) ** 2
        A2 = mr ** 2 / (M * mr + N * ms) ** 2
        A3 = (mr * ms) / (M * mr + N * ms) ** 2
    if isinstance(monomerlength, numbers.Number) and l is None:
        l = monomerlength * mr
    if isinstance(vmonomer, numbers.Number) and Rc is None:
        Rc = (ms * vmonomer * 3 / 4 / np.pi) ** (1 / 3)

    # distance between centers of neighbouring spheres
    A = l + 2 * Rc
    QA = Q * A
    # sphere form factor
    Y1 = 3 * (np.sin(Q * Rc) - (Q * Rc) * np.cos(Q * Rc)) / (Q * Rc) ** 3
    # S_ss equ 13 in [1]_
    Z1 = 2 * Y1 ** 2 * (N / (1 - np.sinc(QA)) - N / 2 - (1 - np.sinc(QA) ** N) / (1 - np.sinc(QA)) ** 2 * np.sinc(QA))

    # infinitely thin rod equ 16 self term ii
    Y2 = special.sici(Q * l)[0] / (Q * l)
    # rods mixed terms ij
    Y3 = (special.sici(Q * (A - Rc))[0] - special.sici(Q * Rc)[0]) / (Q * l)

    # S_rr equ 15 in [1]_
    Z2 = M * (2 * Y2 - np.sinc(Q * l / 2) ** 2) \
         + 2 * M * Y3 ** 2 / (1 - np.sinc(QA)) \
         - 2 * Y3 ** 2 * (1 - np.sinc(QA) ** M) / (1 - np.sinc(QA)) ** 2

    # S_rs equ 21 in [1]
    Z3 = Y3 * Y1 * 4 * (
            (N - 1) / (1 - np.sinc(QA)) - (1 - np.sinc(QA) ** (N - 1)) / (1 - np.sinc(QA)) ** 2 * np.sinc(QA))

    # add the different contributions
    YY = A1 * Z1 + A2 * Z2 + A3 * Z3
    result = dA(np.c_[Q, YY].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq'
    result.pearlRadius = Rc
    result.A1 = A1
    result.A2 = A2
    result.A3 = A3
    result.numberPearls = N
    result.numberRods = M
    result.mr = mr
    result.ms = ms
    try:
        result.numberMonomers = ms * N + mr * (N - 1)
    except:
        pass
    result.stringLength = l
    return result


def linearPearls(q, N, R, l, pearlSLD, cr, n=1, relError=0, rms=0, ffpolydispersity=0, ncpu=0,
                 smooth=7, shellthickness=0, shellSLD=0, solventSLD=0):
    r"""
    Linear arranged pearls connected by gaussian chains in between them.

    Large pearls are aligned in a line and connected by a polymer chain approximated as Gaussian coils.
    Increasing the number of connecting coils (reducing individual mass) result in an approximated linear connector.
    The model uses cloudscattering.
    The formfactor is normalized to 1. For absolute scattering see introduction :ref:`formfactor (ff)`.

    This model might be used as template to make models with with inhomogeneous pearls like
    hollow spheres or Gaussian coils as pearls just by changing the sphere formfactor and adjusting the geometry.

    Parameters
    ----------
    q : array, ndim= Nx1
         Radial wavevectors in 1/nm
    N : int
        Number of pearls
    R : float
        Radius of uniform pearls in units nm.
    l : float
        Length of connectors in units nm.
        The distance between pearls center of mass is 2(R+shellD)+l
    pearlSLD : float
        Scattering length density in each pearl in units nm^-2.
        The pearl scattering length is volume*SLD (respectively the corresponding value for coreShell pearls)
    cr : float>=0
        Virtual connector radius in units nm determining the connector scattering length.
        Describing the connector volume as a cylinder with scattering length density of the core
        the volume is :math:`V_c = \pi r_{cr}^2l` and the scattering length is F_a(q=0)=V*pearlsSLD.
        The scattering length is distributed to n Gaussian coils. cr=0 means no connector.
    n : int
        Number of Gaussians coils in connector.
        The coils are equal distributed on pearl connecting lines with Rg=l/2/n that coils touch with a distance 2Rg
        and touch the radius of the pearls. Zero means no connector but pearls separated by l.
    shellthickness : float>=0
        Optional a shellthickness :math:`d_{shell}` (units nm) to add an outer shell around the pearl.
        The shellthickness is added to the distance between pearls.
    shellSLD : float
        Optional, scattering length density in each pearl shell in units nm^-2.
    solventSLD : float
        Solvent scattering length density in units nm^-2.
    relError : float
        Determines calculation method.
         - relError>1   Explicit calculation of spherical average with Fibonacci lattice on sphere
                        of 2*relError+1 points. Already 150 gives good results, more is better (see Examples)
         - 0<relError<1 Monte Carlo integration on sphere until changes in successive iterations
                        become smaller than relError.
                        (Monte carlo integration with pseudo random numbers, see sphereAverage).
                        This might take long for too small error.
         - relError=0   The Debye equation is used (no asymmetry factor beta, no rms, no ffpolydispersity).
                        Computation is of order :math:`N^2` opposite to above which is order :math:`N`.
                        For about 1000 particles same computing time,for 500 Debye is 4 times faster than above.
                        If beta, rms or polydispersity is needed use above.
    rms : float, default=0
        Root mean square displacement :math:`\langle u^2 \rangle^{0.5}` of the positions in line as
        random (Gaussian) displacements in nm.
        *!Attention!* Introduction of rms results in noise on the model function if relError is to small.
        This is a result from changing position in each orientation during orientation average. To reduce this noise
        during fitting relError should be high (>2000) and smoothing might be increased.
    ffpolydispersity : float
        Polydispersity of the spheres in relative units.
        See cloudscattering.
    ncpu : int, default 0
        Number of cpus used in the pool for multiprocessing.
        See cloudscattering.
    smooth : int, default 7
        Window size for smoothing (using formel.smooth with window 'flat')
        rms and polydispersity introduce noise on the scattering curve from the explicit calculation of
        the ensemble average. Smoothing (flat window) reduces this noise again.

    Returns
    -------
    dataArray :
        Columns [q,Pq,beta]
         - .I0 :          Forward scattering I0
         - .sumblength :  Scattering length of the linear pearls
         - .formfactoramplitude   : formfactor amplitude of cloudpoints according to type for all q values.
         - .formfactoramplitude_q :  corresponding q values
         - beta only for relErr > 0

    Notes
    -----
    This model is unique to Jscatter as connectors are included (at 2019).
    For linear pearls without connector use [1]_ as reference which is basically the same.
    Random pearls e.g. restricted to a cylinder are described in [2]_.

    .. image:: ../../examples/images/linearPearlsSketch.png
     :width: 70 %
     :align: center
     :alt: linearPearlsSketch

    The  form factor is :math:`P(Q)=< F_a(q) \cdot F_a^*(q) >=< |F(q)|^2 >`
    We calculate the scattering amplitude :math:`F_a(q)` with scattering amplitude :math:`b_i(q)`

    .. math:: F_a(q)= \sum_N b_i(q) e^{i\mathbf{qr_i}}  / \sum_N b_i(q=0)

    Here we use :math:`b_i(q)` of spheres (or coreShell) and Gaussians to describe the pearls and linear connectors.
    Positions are arranged along a line (x axis)  with positions :math:`x_{p=[0..N-1]}=p(2R+2d_{shell}+l)`
    for pearls and coils of radius :math:`r_c=l/(2n)` at positions
     :math:`x_{p=[0..N-1],c=[0..n-1]}=p(2R+l) + R +d_{shell}+ r_c +c 2r_c` .

    The ensemble average :math:`<>` is done as explicit orientational average or using the Debye function.
    The explicit orientational average allows to include rms and polydispersity with random position
    and size changes in each step.

    The scattering length density in a pearl may include swelling of the pearl material by solvent.


    Examples
    --------
    Linear Pearls with position distortion smear out the correlation peak.
    The smeared out low Q range is similar to [3]_ Figure 11.

    Polydispersity reduces the characteristic minimum and fills the characteristic sphere minimum.

    The bumpy low q scattering is due to the random values for rms and polydispersity
    and vanish for larger values of relError as this increases the number of points in the explicit sphericalaverage.
    At the same time computing time increases.
    ::

     import jscatter as js
     q=js.loglist(0.02,5,300)
     p=js.grace(1.2,1)
     for rms in [0.3,1,1.5,2]:
        fq=js.ff.linearPearls(q,N=3,R=2,l=2,pearlSLD=1,cr=0,n=1,relError=200, rms=rms, ffpolydispersity=0)
        p.plot(fq,li=[3,3,-1],sy=0,le=f'rms={rms:.1f}')
     for pp in [0.05,0.1,0.2]:
        fq=js.ff.linearPearls(q,N=3,R=2,l=2,pearlSLD=11,cr=0,n=1,relError=200, rms=rms, ffpolydispersity=pp)
        p.plot(fq,li=[1,3,-1],sy=0,le=f'rms={rms:.0f} polydisp={pp:.2f}')
     p.yaxis(scale='l',label='I(Q)',min=1e-4,max=1.2)
     p.xaxis(scale='l',label='q / nm\S-1',min=0.04,max=7)
     p.legend(x=0.05,y=0.01)
     p.title('linear pearls with position distortion')
     p.subtitle('and polydispersity')
     #p.save(js.examples.imagepath+'/linearPearls2.jpg')

    .. image:: ../../examples/images/linearPearls2.jpg
     :width: 50 %
     :align: center
     :alt: linearPearls2

    Longer or stronger connector fill up the characteristic sphere minimum.
    ::

     import jscatter as js
     q=js.loglist(0.05,5,300)
     p=js.grace(1.5,1)
     for n in [0,0.5,1.3,2]:
         fq=js.ff.linearPearls(q,N=5,R=4,l=5,pearlSLD=100,cr=n,n=1)
         p.plot(fq,li=[1,2,-1],le='cr={0:.1f}'.format(n))
     p.plot(fq.formfactoramplitude_q,fq.formfactoramplitude[0]**2,le='single sphere')
     p.plot(fq.formfactoramplitude_q,fq.formfactoramplitude[1]**2,le='single gaussian')
     p.yaxis(scale='l',label='I(Q)',min=0.00001,max=1.1)
     p.xaxis(scale='l',label='q / nm\S-1',min=0.05,max=6)
     p.legend(x=0.1,y=0.01)
     p.title('linear pearls with gaussian connector')
     #p.save(js.examples.imagepath+'/linearPearls.jpg')

    .. image:: ../../examples/images/linearPearls.jpg
     :width: 50 %
     :align: center
     :alt: linearPearls



    References
    ----------
    For linear pearls without connector

    .. [1] Cascade of Transitions of Polyelectrolytes in Poor Solvents
           A. V. Dobrynin, M. Rubinstein, S. P. Obukhov
           Macromolecules 1996, 29, 2974-2979

    Linear pearls with polydispersity, pearls in cylinder, NO connectors

    .. [2] Form factor of cylindrical superstructures
           Leonardo Chiappisi et al.
           J. Appl. Cryst. (2014). 47, 827–834

    Liao uses Simulation to come to a similar formfactor as found here with connectors, rms and polydispersity.

    .. [2] Counterion-correlation-induced attraction and necklace formation in polyelectrolyte solutions:
           Theory and simulations.
           Liao, Q., Dobrynin, A. V., & Rubinstein, M.
           Macromolecules, 39(5), 1920–1938.(2006). https://doi.org/10.1021/ma052086s

    """
    if cr is None: cr = 0
    if cr <= 0:
        cr = 0
        n = 0
    if l < 0: l = 0
    d = abs(shellthickness)

    # fq of different sized spheres (root and norm is taken in cloudscattering)
    if d > 0 and shellSLD != solventSLD:
        fq = sphereCoreShell(q, Rc=R, Rs=R + d, bc=pearlSLD, bs=shellSLD, solventSLD=solventSLD)[[0, 2]]
    else:
        fq = sphere(q, R, pearlSLD - solventSLD)[[0, 2]]

    M = N - 1  # number connectors
    line = np.zeros((N + M * n, 5))  # N pearls and (N-1)*n gaussians in connectors
    # pearls
    line[:N, 0] = np.r_[0:N] * (2 * R + 2 * d + l)  # position on x axis
    line[:N, 3] = fq.fa0                            # scattering amplitude of pearls
    line[:N, 4] = 1                                 # index formfactor
    # connectors as n Gaussian coils
    if n > 0:
        connectorSL = np.pi * cr ** 2 * l * (pearlSLD - solventSLD)
        crg = l / 2 / n  # coil radius
        for m in range(M):
            line[N + m * n:N + (m + 1) * n, 0] = line[m, 0] + R + d + crg + 2 * crg * np.r_[0:n]
        line[N:, 3] = connectorSL / n
        line[N:, 4] = 2
        fq = fq.addColumn(1, gaussianChain(q, crg).Y**0.5)

    # use cloudscattering
    result = cloudScattering(q, line, relError=relError, formfactoramp=fq,
                             rms=rms, ffpolydispersity=ffpolydispersity, ncpu=ncpu)
    result.setColumnIndex(iey=None)
    result.modelname = inspect.currentframe().f_code.co_name
    result.fulllength = (2 * R + 2 * d + l) + 2 * R + 2 * d

    if smooth > 0:
        # smooth with polydispersity as noise is strong because of sampling
        result.Y = formel.smooth(result, windowlen=int(smooth), window='flat')
    return result


def ellipsoid(q, Ra, Rb, SLD=1, solventSLD=0, alpha=None, tol=1e-6):
    r"""
    Form factor for a simple ellipsoid (ellipsoid of revolution).

    Parameters
    ----------
    q : float
        Scattering vector unit e.g.  1/A or 1/nm  1/Ra
    Ra : float
        Radius rotation axis   units in 1/unit(q)
    Rb : float
        Radius rotated axis    units in 1/unit(q)
    SLD : float, default =1
        Scattering length density of unit nm^-2
        e.g. SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2 for neutrons
    solventSLD : float, default =0
        Scattering length density of solvent. unit nm^-2
        e.g. D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2 for neutrons
    alpha : [float,float] , default [0,90]
        Angle between rotation axis Ra and scattering vector q in unit grad
        Between these angles orientation is averaged
        alpha=0 axis and q are parallel, other orientation is averaged
    tol : float
        relative tolerance for integration between alpha

    Returns
    -------
    dataArray
        Columns [q; Iq; beta ]
         - .RotationAxisRadius
         - .RotatedAxisRadius
         - .EllipsoidVolume
         - .I0         forward scattering q=0
         - beta is asymmetry factor according to [3]_.
           :math:`\beta = |<F(Q)>|^2/<|F(Q)|^2>` with scattering amplitude :math:`F(Q)` and
           form factor :math:`P(Q)=<|F(Q)|^2>`

    Examples
    --------
    Simple ellipsoid in vacuum::

     import jscatter as js
     import numpy as np
     x=np.r_[0.1:10:0.01]
     Rp=6.
     Re=8.
     ashell=js.ff.multiShellEllipsoid(x,Rp,Re,1)
     #plot it
     p=js.grace()
     p.new_graph(xmin=0.24,xmax=0.5,ymin=0.2,ymax=0.5)
     p[1].subtitle('contrastprofile')
     p[0].plot(ashell)
     p[0].yaxis(scale='l',label='I(q)',min=0.01,max=100)
     p[0].xaxis(scale='l',label='q / nm\S-1',min=0.1,max=10)
     p[0].title('ellipsoid')
     p[1].plot(ashell.contrastprofile,li=1) # a contour of the SLDs
     #p.save(js.examples.imagepath+'/ellipsoid.jpg')

    .. image:: ../../examples/images/ellipsoid.jpg
     :width: 50 %
     :align: center
     :alt: ellipsoid


    References
    ----------
    .. [1] Structure Analysis by Small-Angle X-Ray and Neutron Scattering
           Feigin, L. A, and D. I. Svergun, Plenum Press, New York, (1987).
    .. [2] http://www.ncnr.nist.gov/resources/sansmodels/Ellipsoid.html
    .. [3] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).

    """
    if alpha is None:
        alpha = [0, 90]
    result = multiShellEllipsoid(q, Ra, Rb, shellSLD=SLD, solventSLD=solventSLD, alpha=alpha, tol=tol)
    attr = result.attr
    result.EllipsoidVolume = result.outerVolume
    result.RotationAxisRadius = Ra
    result.RotatedAxisRadius = Rb
    result.contrast = result.shellcontrast
    result.angles = alpha
    attr.remove('columnname')
    attr.remove('I0')
    for at in attr:
        delattr(result, at)
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def multiShellEllipsoid(q, poleshells, equatorshells, shellSLD, solventSLD=0, alpha=None, tol=1e-6):
    r"""
    Scattering of multi shell ellipsoidal particle with varying shell thickness at pole and equator.

    Shell thicknesses add up to form complex particles with any combination of axial ratios and shell thickness.
    A const axial ratio means different shell thickness at equator and pole.

    Parameters
    ----------
    q : array
        Wavevectors, unit 1/nm
    equatorshells : list of float
        Thickness of shells starting from inner most for rotated axis Re making the equator. unit nm.
        The absolute values are used.
    poleshells : list of float
        Thickness of shells starting from inner most for rotating axis Rp pointing to pole. unit nm.
        The absolute values are used.
    shellSLD : list of float
        List of scattering length densities of the shells in sequence corresponding to shellthickness. unit nm^-2.
    solventSLD : float, default=0
        Scattering length density of the surrounding solvent. unit nm^-2
    alpha : [float,float], default [0,90]
        Angular range of rotated axis to average over in degree. Default is no preferred orientation.
    tol : float
        Absolute tolerance for above adaptive integration of alpha.

    Returns
    -------
    dataArray
        Columns[q, Iq, beta]
         Iq                    scattering cross section in units nm**2
          - .contrastprofile       as radius and contrast values at edge points of equatorshells
          - .equatorshellthicknes  consecutive shell thickness
          - .poleshellthickness
          - .shellcontrast         contrast of the shells to the solvent
          - .equatorshellradii     outer radius of the shells
          - .poleshellradii
          - .outerVolume           Volume of complete sphere
          - .I0                    forward scattering for Q=0
          - .alpha                 integration range alpha

    Examples
    --------
    Simple ellipsoid in vacuum::

     import jscatter as js
     import numpy as np
     q=np.r_[0.0:10:0.01]
     Rp=2.
     Re=1.
     ashell=js.ff.multiShellEllipsoid(q,Rp,Re,1)
     #plot it
     p=js.grace()
     p.multi(2,1)
     p[0].plot(ashell)
     p[1].plot(ashell.contrastprofile,li=1) # a contour of the SLDs

    Core shell ellipsoid with a spherical core.
    Dependent on shell thickness at pole or equator the shape is oblate or prolate with a spherical core.
    ::

     import jscatter as js
     import numpy as np
     q=np.r_[0.0:10:0.01]
     def coreShellEllipsoid(q,Rcore,Spole,Sequ,bc,bs):
         ellipsoid = js.ff.multiShellEllipsoid(x,[Rcore,Spole],[Rcore,Sequ],[bc,bs])
         return ellipsoid

     p=js.grace()
     p.multi(2,1,vgap=0.25)
     for eq in [0.1,1,2]:
         ell = coreShellEllipsoid(q,2,1,eq,1,2)
         p[0].plot(ell)
         p[1].plot(ell.contrastprofile,li=1) # a contour of the SLDs
     p[0].yaxis(label='I(q)',scale='log')
     p[0].xaxis(label='q / nm\S-1')
     p[1].yaxis(min=0,max=3)
     p[1].xaxis(label='radius / nm')

    Alternating shells with thickness 0.3 nm h2o and 0.2 nm d2o in vacuum::

     import jscatter as js
     import numpy as np
     x=np.r_[0.1:10:0.01]
     shell=np.r_[[0.3,0.2]*3]
     sld=[-0.56e-4,6.39e-4]*3

     # constant axial ratio for all shells but nonconstant shell thickness
     axialratio=2
     ashell=js.ff.multiShellEllipsoid(x,axialratio*shell,shell,sld)

     # shell with constant shellthickness of one component and other const axialratio
     pshell=shell[:]
     pshell[0]=shell[0]*axialratio
     pshell[2]=shell[2]*axialratio
     pshell[4]=shell[4]*axialratio
     bshell=js.ff.multiShellEllipsoid(x,pshell,shell,sld)

     #plot it
     p=js.grace()
     p.new_graph(xmin=0.24,xmax=0.5,ymin=0.2,ymax=0.5)
     p[1].subtitle('contrastprofile')
     p[0].plot(ashell,le='const. axial ratio')
     p[1].plot(ashell.contrastprofile,li=2) # a contour of the SLDs
     p[0].plot(bshell,le='const shell thickness')
     p[1].plot(bshell.contrastprofile,li=2) # a contour of the SLDs
     p[0].yaxis(scale='l',label='I(q)',min=1e-9,max=0.0002)
     p[0].xaxis(scale='l',label='q / nm\S-1')
     p[0].legend(x=0.12,y=1e-5)
     p[0].title('multi shell ellipsoids')
     #p.save(js.examples.imagepath+'/multiShellEllipsoid.jpg')

    .. image:: ../../examples/images/multiShellEllipsoid.jpg
     :width: 50 %
     :align: center
     :alt: multiShellEllipsoid

    Double shell with exponential decreasing exterior shell to solvent scattering::

     import jscatter as js
     import numpy as np
     x=np.r_[0.0:10:0.01]
     def doubleexpshells(q,d1,ax,d2,e3,sd1,sd2,sol):
        shells =[d1   ,d2]+[e3]*9
        shellsp=[d1*ax,d2]+[e3]*9
        sld=[sd1,sd2]+list(((sd2-sol)*np.exp(-np.r_[0:3:9j])))
        return js.ff.multiShellEllipsoid(q,shellsp,shells,sld,solventSLD=sol)
     dde=doubleexpshells(x,0.5,1,0.5,1,1e-4,2e-4,0)
     #plot it
     p=js.grace()
     p.multi(2,1)
     p[0].plot(dde)
     p[1].plot(dde.contrastprofile,li=1) # a countour of the SLDs
     p[0].yaxis(scale='log')

    References
    ----------
    .. [1] Structure Analysis by Small-Angle X-Ray and Neutron Scattering
           Feigin, L. A, and D. I. Svergun, Plenum Press, New York, (1987).
    .. [2] http://www.ncnr.nist.gov/resources/sansmodels/Ellipsoid.html
    .. [3] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).

    """
    if alpha is None:
        alpha = [0, 90]
    if isinstance(shellSLD, numbers.Number): shellSLD = [shellSLD]
    if isinstance(poleshells, numbers.Number): poleshells = [poleshells]
    if isinstance(equatorshells, numbers.Number): equatorshells = [equatorshells]
    if len(shellSLD) != len(equatorshells) or len(equatorshells) != len(poleshells):
        raise Exception(
            'shellSLD and equatorshells should be of same length but got:%i!=%i' % (len(shellSLD), len(equatorshells)))

    requ = np.cumsum(np.abs(equatorshells))  # returns array with absolute values
    rpol = np.cumsum(np.abs(poleshells))
    dSLDs = np.r_[shellSLD] - solventSLD  # subtract solvent to have in any case the contrast to the solvent

    # forward scattering Q=0 -------------
    Vr = 4 / 3. * np.pi * requ ** 2 * rpol
    dslds = Vr * dSLDs
    dslds[:-1] = dslds[:-1] - Vr[:-1] * dSLDs[1:]  # subtract inner shell
    fa0 = dslds.sum()

    # scattering amplitude in general
    def _ellipsoid_ffamp(Q, cosa, Re, Rp):
        axialratio = Rp / Re
        z = lambda q, Re, x: q * Re * np.sqrt(1 + x ** 2 * (axialratio ** 2 - 1))
        f = lambda z: 3 * (np.sin(z) - z * np.cos(z)) / z ** 3
        return f(z(Q, Re, cosa))

    def _ffa(q, cosa, re, rp):
        # avoid zero
        Q = np.where(q == 0, q * 0 + 1e-10, q)
        # scattering amplitude multishell Q and R are column and row vectors
        # outer shell radius
        fa = Vr * dSLDs * _ellipsoid_ffamp(Q[:, None], cosa, re, rp)
        if len(re) > 1:
            # subtract inner radius for multishell, innermost shell has r=0
            fa[:, 1:] = fa[:, 1:] - Vr[:-1] * dSLDs[1:] * _ellipsoid_ffamp(Q[:, None], cosa, re[:-1], rp[:-1])
        # sum over radii and square for intensity
        fa = fa.sum(axis=1)
        # restore zero
        Fa = np.where(q == 0, fa0, fa)
        Fq = Fa ** 2
        # return scattering intensity and scattering amplitude for beta
        return np.c_[Fq, Fa]

    # integration over orientations for all q
    cosalpha = np.cos(np.deg2rad(alpha))
    res = formel.parQuadratureAdaptiveGauss(_ffa, cosalpha[1], cosalpha[0], 'cosa',
                                            tol=tol, miniter=30, q=q, re=requ, rp=rpol)
    # calc beta
    res[1] = res[1] ** 2 / res[0]
    result = dA(np.c_[q, res.T].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq; beta'
    result.equatorshellsthickness = equatorshells
    result.poleshellthickness = poleshells
    result.shellcontrast = shellSLD
    result.equatorshellradii = requ
    result.poleshellradii = rpol
    contrastprofile = np.c_[np.r_[requ - equatorshells, requ], np.r_[shellSLD, shellSLD]].T
    result.contrastprofile = contrastprofile[:,
                             np.repeat(np.arange(len(shellSLD)), 2) + np.tile(np.r_[0, len(shellSLD)], len(shellSLD))]
    result.outerVolume = 4. / 3 * np.pi * max(requ) ** 2 * max(rpol)
    result.I0 = fa0 ** 2
    result.alpha =alpha
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _ellipsoid_ff_amplitude(q, a, Ra, Rb):
    """
    Ellipsoidal form factor amplitude for internal usage only. save for q=0
    q in nm
    a as angle between q and the rotating axis Ra (Rb==Rc)
    Ra,Rb in nm

    If x is an array of len N the output is shape N+1,len(q) with 0 as q and 1:N+1 as result

    Orientationalaverage needs to be done with angle NOT cos(angle)
    """
    Q = np.where(q == 0, q * 0 + 1e-10, q)
    nu = Ra / float(Rb)
    cosa = np.cos(a)
    z = lambda q, Rb, x: q[:, None] * Rb * np.sqrt(1 + x ** 2 * (nu ** 2 - 1))
    f = lambda z: 3 * (np.sin(z) - z * np.cos(z)) / z ** 3
    # include factor from theta integration cos(a)da
    fa = f(z(Q, Rb, cosa)) * cosa
    fa = np.where(q[:, None] == 0, 1, fa)
    return dA(np.c_[q, fa].T)


def ellipsoidFilledCylinder(q=1, R=10, L=0, Ra=1, Rb=2, eta=0.1, SLDcylinder=0.1, SLDellipsoid=1, SLDmatrix=0, alpha=90,
                            epsilon=None, fPY=1, dim=3):
    r"""
    Scattering of a single cylinder filled with ellipsoidal particles .

    A cylinder filled with ellipsoids of revolution with cylinder formfactor and ellipsoid scattering
    as described by Siefker [1]_.
    Ellipsoids have a fluid like distribution and hard core interaction leading to Percus-Yevick
    structure factor between ellipsoids. Ellipsoids can be oriented along cylinder axis.
    If cylinders are in a lattice, the  ellipsoid scattering (column 2) is observed in the diffusive scattering and
    the dominating cylinder contributes only to the bragg peaks as a form factor.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm
    R : float
        Cylinder radius in nm
    L : float
        Length of the cylinder in nm
        If zero infinite length is assumed, but absolute intensity is not valid, only relative intensity.
    Ra : float
        Radius rotation axis   units in nm
    Rb : float
        Radius rotated axis    units in nm
    eta : float
        Volume fraction of ellipsoids in cylinder for use in Percus-Yevick structure factor.
        Radius in PY corresponds to sphere with same Volume as the ellipsoid.
    SLDcylinder : float,default 1
        Scattering length density cylinder material in nm**-2
    SLDellipsoid : float,default 1
        Scattering length density of ellipsoids in cylinder in nm**-2
    SLDmatrix : float
        Scattering length density of the matrix outside the cylinder in nm**-2
    alpha : float, default 90
        Orientation of the cylinder axis to wavevector in degrees
    epsilon : [float,float], default [0,90]
        Orientation range of ellipsoids rotation axis relative to cylinder axis in degrees.
    fPY : float
        Factor between radius of ellipsoids Rv (equivalent volume) and radius used in structure factor Rpy
        Rpy=fPY*(Ra*Rb*Rb)**(1/3)
    dim : 3,1, default 3
        Dimensionality of the Percus-Yevick structure factor
        1 is one dimensional stricture factor, anything else is 3 dimensional (normal PY)

    Returns
    -------
    dataArray
        Columns [q,n*conv(ellipsoids,cylinder)*sf_b + cylinder,
                 n *conv(ellipsoids,cylinder)*sf_b,
                 cylinder, n * ellipsoids,
                 sf, beta_ellipsoids]
         - Each contributing formfactor is given with its absolute contribution
           :math:`V^2contrast^2` (NOT normalized to 1)
         - The observed structurefactor is :math:`sf\_b = S_{\beta}(q)=1+\beta (S(q)-1)`.
         - beta_ellipsoids :math:`=\beta(q)` is the asymmetry factor of Kotlarchyk and Chen [2]_.
         - conv(ellipsoids,cylinder) -> ellipsoid formfactor convoluted with cylinder formfactor
         - .ellipsoidNumberDensity  -> n ellipsoid number density in cylinder volume
         - .cylinderRadius
         - .cylinderLength
         - .cylinderVolume
         - .ellipsoidRa
         - .ellipsoidRb
         - .ellipsoidRg
         - .ellipsoidVolume
         - .ellipsoidVolumefraction
         - .ellipsoidNumberDensity  unit 1/nm**3
         - .alpha orientation range
         - .ellipdoidAxisOrientation

    Examples
    --------
    ::

     import jscatter as js
     p=js.grace()
     q=js.loglist(0.01,5,800)
     ff=js.ff.ellipsoidFilledCylinder(q,L=100,R=5.4,Ra=1.63,Rb=1.63,eta=0.4,alpha=90,epsilon=[0,90],SLDellipsoid=8)
     p.plot(ff.X,ff[2],li=[1,2,-1],sy=0,legend='convolution cylinder x ellipsoids')
     p.plot(ff.X,ff[3],li=[2,2,-1],sy=0,legend='cylinder formfactor')
     p.plot(ff.X,ff[4],li=[1,2,-1],sy=0,legend='ellipsoid formfactor')
     p.plot(ff.X,ff[5],li=[3,2,-1],sy=0,legend='structure factor ellipsoids')
     p.plot(ff.X,ff.Y,sy=[1,0.3,4],legend='conv. ellipsoid + filled cylinder')
     p.legend(x=2,y=1e-1)
     p.yaxis(scale='l',label='I(q)',min=1e-4,max=1e6)
     p.xaxis(scale='n',label='q / nm\S-1')
     p.title('ellipsoid filled cylinder')
     p.subtitle('the convolution cylinder x ellipsoids shows up in diffusive scattering')
     #p.save(js.examples.imagepath+'/ellipsoidFilledCylinder.jpg')

    The measured scattering intensity (blue points) follows the cylinder formfactor but the cylinder minima are limited
    by ellipsoid scattering (black line). Ellipsoid scattering shows a pronounced maximum around 2 1/nm but increases
    at low Q because of the convolution with the cylinder formfactor.

    .. image:: ../../examples/images/ellipsoidFilledCylinder.jpg
     :width: 50 %
     :align: center
     :alt: ellipsoidFilledCylinder

    Angular averaged formfactor ::

     def averageEFC(q,R,L,Ra,Rb,eta,alpha=[alpha0,alpha1],fPY=fPY):
         res=js.dL()
         alphas=np.deg2rad(np.r_[alpha0:alpha1:13j])
         for alpha in alphas:
             ffe=js.ff.ellipsoidFilledCylinder(q,R=R,L=L,Ra=Ra,Rb=Rb,eta=ata,alpha=alpha,)
             res.append(ffe)
         result=res[0].copy()
         result.Y=scipy.integrate.simps(res.Y,alphas)/(alpha1-alpha0)
         return result

    References
    ----------
    .. [1]  Confinement Facilitated Protein Stabilization As Investigated by Small-Angle Neutron Scattering.
            Siefker, J., Biehl, R., Kruteva, M., Feoktystov, A., & Coppens, M. O. (2018)
            Journal of the American Chemical Society, 140(40), 12720–12723. https://doi.org/10.1021/jacs.8b08454
    .. [2] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).

    """
    if epsilon is None:
        epsilon = [0, 90]
    q = np.atleast_1d(q)
    sldc = SLDmatrix - SLDcylinder
    slde = SLDellipsoid - SLDcylinder
    alpha = np.deg2rad(np.r_[alpha])
    epsilon = np.deg2rad(epsilon)
    Ra = abs(Ra)
    Rb = abs(Rb)

    # nu = Ra / float(Rb)
    Vell = 4 * np.pi / 3. * Ra * Rb * Rb
    if L == 0:
        Vcyl = np.pi * R ** 2 * 1
    else:
        Vcyl = np.pi * R ** 2 * L
    # matrix with q and x for later integration
    Rge = (Ra ** 2 + 2 * Rb ** 2) ** 0.5
    # RgL = (R ** 2 / 2. + L ** 2 / 12) ** 0.5
    # catch if really low Q are tried
    lowerlimit = min(0.01 / Rge, min(q) / 5.)
    upperlimit = min(100 / Rge, max(q) * 5.)
    qq = np.r_[0, formel.loglist(lowerlimit, upperlimit, 200)]
    # width dq between Q values for integration;
    dq = qq * 0
    dq[1:] = ((qq[1:] - qq[:-1]) / 2.)
    dq[0] = (qq[1] - qq[0]) / 2.  # above zero
    dq[-1] = qq[-1] - qq[-2]  # assume extend to inf

    # generate ellipsoid orientations
    points = formel.fibonacciLatticePointsOnSphere(1000)
    pp = points[(points[:, 2] > epsilon[0]) & (points[:, 2] < epsilon[1])]
    v = formel.rphitheta2xyz(pp)
    # assume cylinder axis as [0,0,1], rotate the ellipsoid distribution to alpha cylinder axis around [1,0,0]
    RotM = formel.rotationMatrix([1, 0, 0], alpha)
    pxyz = np.dot(RotM, v.T).T
    # points in polar coordinates still with radius 1, theta component is for average formfactor amplitude
    theta = formel.xyz2rphitheta(pxyz)[:, 2]
    # use symmetry of _ellipsoid_ff_amplitude
    theta[theta > np.pi / 2] = np.pi / 2 - theta[theta > np.pi / 2]
    theta[theta < 0] = -theta[theta < 0]
    # get all ff_amplitudes interpolate and get mean
    eangles = np.r_[0:np.pi / 2:45j]
    fee = _ellipsoid_ff_amplitude(qq, eangles, Ra, Rb)[1:].T
    feei = scipy.interpolate.interp1d(eangles, fee)
    femean_qq = feei(theta).mean(axis=1)
    febetamean_qq = (feei(theta) ** 2).mean(axis=1)

    def _sfacylinder(q, R, L, angle):
        """
        single cylinder form factor amplitude for all angle
        q : wavevectors
        r : cylinder radius
        L : length of cylinder, L=0 is infinitely long cylinder
        angle : angle between axis and scattering vector q in rad
        for q<0 we get zero as a feature!!
        """
        # deal with possible zero in q and sin(angle)
        sina = np.sin(angle)
        qsina = q[:, None] * sina
        qsina[:, sina == 0] = q[:, None]
        qsina[q == 0, :] = 1  # catch later
        result = np.zeros_like(qsina)
        if L > 0:
            qcosa = q[:, None] * np.cos(angle)
            fqq = lambda qsina, qcosa: 2 * special.j1(R * qsina) / (R * qsina) * special.j0(L / 2. * qcosa)
            result[q > 0, :] = fqq(qsina[q > 0, :], qcosa[q > 0, :])
            result[q == 0, :] = 1
        else:
            fqq = lambda qsina: 2 * special.j1(R * qsina) / (R * qsina)
            result[q > 0, :] = fqq(qsina[q > 0, :])
            result[q == 0, :] = 1
        return result

    def fc2(q, R, L, angle):
        # formfactor cylinder ; this is squared!!!
        if angle[0] == angle[1]:
            res = _sfacylinder(q, R, L, np.r_[angle[0]]) ** 2
        else:
            pj = (angle[1] - angle[0]) // 0.05
            if pj == 0: pj = 2
            al_angle = np.r_[angle[0]:angle[1]:pj * 1j]
            val = _sfacylinder(q, R, L, al_angle)
            res = np.trapz(val ** 2, al_angle, axis=1)
        return res

    def fefcconv(q, angle):
        # convolution of cylinder and ellipsoid;
        val = [(femean_qq * _sfacylinder(q_ - qq, R, L, np.r_[angle]).T[0] * dq).sum() / dq[qq <= q_].sum()
                                                                              if q_ > 0 else 1 for q_ in qq]
        res = np.interp(q, qq, np.r_[val])
        return res

    # structure factor ellipsoids
    if dim == 1:
        R1dim = (Ra * Rb * Rb) ** (1 / 3.)
        Sq = sf.PercusYevick1D(q, fPY * R1dim, eta=fPY * eta)
        density = eta / (2 * R1dim)  # in unit 1/nm
    else:
        Sq = sf.PercusYevick(q, fPY * (Ra * Rb * Rb) ** (1 / 3.), eta=fPY ** 3 * eta)
        # particle number in cylinder volume
        density = Sq.molarity * constants.Avogadro / 10e24  # unit 1/nm**3
    nV = density * Vcyl
    # contribution form factors
    ffellipsoids = nV * (slde * Vell) ** 2 * np.interp(q, qq, femean_qq ** 2)
    ffellipsoidsbeta = np.interp(q, qq, (femean_qq ** 2 / febetamean_qq))  # ala Kotlarchyk

    ffcylinder = (sldc * Vcyl) ** 2 * fc2(q, R, L, [alpha[0], alpha[0]])[:, 0]
    # convoluted  form factor of ellipsoids
    # and structure factor correction as in Chen, Kotlarchyk
    ffconv = nV * (slde * Vell) ** 2 * fefcconv(q, alpha[0]) ** 2 * (1 + ffellipsoidsbeta * (Sq.Y - 1))

    result = dA(np.c_[q, ffconv + ffcylinder, ffconv, ffcylinder, ffellipsoids, Sq.Y, ffellipsoidsbeta].T)
    result.cylinderRadius = R
    result.cylinderLength = L
    result.cylinderVolume = Vcyl
    result.ellipsoidRa = Ra
    result.ellipsoidRb = Rb
    result.ellipsoidRg = R
    result.ellipsoidVolume = Vell
    result.ellipsoidVolumefraction = eta
    result.ellipsoidNumberDensity = density  # unit 1/nm**3
    result.alpha = np.rad2deg(alpha[0])
    result.ellipdoidAxisOrientation = np.rad2deg(epsilon)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; ellipsoidscylinder; convellicyl; cylinder; ellipsoids; structurefactor; betaellipsoids'
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def teubnerStrey(q, xi, d, eta2=1):
    r"""
    Scattering from space correlation ~sin(2πr/D)exp(-r/ξ)/r e.g. disordered bicontinious microemulsions.

    Phenomenological model for the scattering intensity of a two-component system using the Teubner-Strey model [1]_.
    Often used for  bi-continuous micro-emulsions.

    Parameters
    ----------
    q : array
        Wavevectors
    xi : float
        Correlation length
    d : float
        Characteristic domain size, periodicity.
    eta2 : float, default=1
        Squared mean scattering length density contrast :math:`\eta^2`

    Returns
    -------
    dataArray
        Columns [q, Iq]

    Notes
    -----
    A correlation function :math:`\gamma(r) = \frac{d}{2\pi r}e^{-r/\xi}sin(2\pi r/d)` yields after 3D Fourier transform
    the scattering intensity of form

    .. math:: I(q) = \frac{8\pi\eta^2/\xi}{a_2 + 2bq^2 + q^4}

    with
     - :math:`k = 2 \pi/d`
     - :math:`a_2 = (k^2 + \xi^{-2})^2`
     - :math:`b = k^2 - \xi^{-2}`
     - :math:`q_{max}=((2\pi/d)^2-\xi^{-2})^{1/2}`

    Examples
    --------
    Teubner-Strey with background and a power law for low Q
    ::

     import jscatter as js
     import numpy as np

     def tbpower(q,B,xi,dd,A,beta,bgr):
         # Model Teubner Strey  + power law and background
         tb=js.ff.teubnerStrey(q=q,xi=xi,d=dd)
         # add power law and background
         tb.Y=B*tb.Y+A*q**beta+bgr
         tb.A=A
         tb.bgr=bgr
         tb.beta=beta
         return tb

     q=js.loglist(0.01,5,600)
     p=js.grace()
     data=tbpower(q,1,10,20,0.00,-3,0.)
     p.plot(data,legend='no bgr, no power law')
     data=tbpower(q,1,10,20,0.002,-3,0.1)
     p.plot(data,legend='xi=10')
     data=tbpower(q,1,20,20,0.002,-3,0.1)
     p.plot(data,legend='xi=20')
     p.xaxis(scale='l',label=r'Q / nm\S-1')
     p.yaxis(scale='l',label='I(Q) / a.u.')
     p.legend(x=0.02,y=1)
     p.title('TeubnerStrey model with power law and background')
     #p.save(js.examples.imagepath+'/teubnerStrey.jpg')

    .. image:: ../../examples/images/teubnerStrey.jpg
     :width: 50 %
     :align: center
     :alt: teubnerStrey



    References
    ----------
    .. [1] M. Teubner and R. Strey,
           Origin of the scattering peak in microemulsions,
           J. Chem. Phys., 87:3195, 1987
    .. [2] K. V. Schubert, R. Strey, S. R. Kline, and E. W. Kaler,
           Small angle neutron scattering near lifshitz lines:
           Transition from weakly structured mixtures to microemulsions,
           J. Chem. Phys., 101:5343, 1994

    """
    q = np.atleast_1d(q)
    qq = q * q
    k = 2 * np.pi / d
    a2 = (k ** 2 + xi ** -2) ** 2
    b = k ** 2 - xi ** -2
    Iq = 8 * np.pi * eta2 / xi / (a2 - 2 * b * qq + qq * qq)
    result = dA(np.c_[q, Iq].T)
    result.correlationlength = xi
    result.domainsize = d
    result.SLD2 = eta2
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name

    return result


def superball(q, R, p, SLD=1, solventSLD=0, nGrid=12, returngrid=False):
    r"""
    A superball is a general mathematical shape that can be used to describe rounded cubes, sphere and octahedron's.

    The shape parameter p continuously changes from star, octahedron, sphere to cube.

    Parameters
    ----------
    q : array
        Wavevector in 1/nm
    R : float, None
        2R = edge length
    p : float, 0<p<100
        Parameter that describes shape
         - p=0       empty space
         - p<0.5     concave octahedron's
         - p=0.5     octahedron
         - 0.5<p<1   convex octahedron's
         - p=1       spheres
         - p>1       rounded cubes
         - p->inf    cubes
    SLD : float, default =1
        Scattering length density of cuboid. unit nm^-2
    solventSLD : float, default =0
        Scattering length density of solvent. unit nm^-2
    nGrid : int
        Number of gridpoints in superball volume is ~ nGrid**3.
        The accuracy can be increased increasing the number of grid points dependent on needed q range.
        Orientational average is done with 2(nGrid*4)+1 orientations on Fibonacci lattice.
    returngrid : bool
        Return only grid as lattice object.
        The a visualisation can be done using grid.show()

    Returns
    -------
    dataArray
        Columns [q,Iq, beta]

    Notes
    -----
    The shape is described by

    .. math:: |x|^{2p} + |y|^{2p} + |z|^{2p} \le |R|^{2p}

    which results in a sphere for p=1. The numerical integration is done by a pseudorandom grid of scatterers.

    .. image:: ../../examples/images/superballfig.jpg
     :width: 100 %
     :align: center
     :alt: superballfig

    Examples
    --------
    Visualisation as shown above ::

     import jscatter as js
     import numpy as np
     import matplotlib.pyplot as plt
     from mpl_toolkits.mplot3d import Axes3D
     fig = plt.figure(figsize=[15,3])
     q=np.r_[0:5:0.1]
     R=3
     for i,p in enumerate([0.2,0.5,1,1.3,20],1):
         ax = fig.add_subplot(1,5,i, projection='3d')
         grid=js.ff.superball(q,R,p=p,nGrid=40,returngrid=True)
         grid.filter(lambda xyz: np.linalg.norm(xyz))
         grid.show(fig=fig, ax=ax,atomsize=0.2)
         ax.set_title(f'p={p:.2f}')
     #fig.savefig(js.examples.imagepath+'/superballfig.jpg')



    Compare to extreme cases of sphere (p=1) and cube (p->inf , use here 100)
    to estimate the needed accuracy in your Q range. ::

     import jscatter as js
     import numpy as np
     #
     q=np.r_[0:3.5:0.02]
     R=6
     nGrid=25
     p=js.grace()
     p.multi(2,1)
     p[0].yaxis(scale='l',label='I(q)')
     ss=js.ff.superball(q,R,p=1,nGrid=12)
     p[0].plot(ss,legend='superball p=1 nGrid=12 default')
     ss=js.ff.superball(q,R,p=1,nGrid=25)
     p[0].plot(ss,legend='superball p=1 nGrid=25')
     p[0].plot(js.ff.sphere(q,R),li=1,sy=0,legend='sphere ff')
     p[0].legend(x=2,y=5e5)
     #
     p[1].yaxis(scale='l',label='I(q)')
     p[1].xaxis(scale='n',label='q / nm\S-1')
     cc=js.ff.superball(q,R,p=100)
     p[1].plot(cc,sy=[1,0.3,1],legend='superball p=100 nGrid=12')
     cc=js.ff.superball(q,R,p=100,nGrid=25)
     p[1].plot(cc,sy=[1,0.3,2],legend='superball p=100 nGrid=25')
     p[1].plot(js.ff.cuboid(q,2*R),li=4,sy=0,legend='cuboid')
     p[1].legend(x=2,y=9e5)
     p[0].title('Superball with transition from sphere to cuboid')
     p[0].subtitle('p=1 sphere; p>1 round cube; p>20 cube  ')
     #p.save(js.examples.imagepath+'/superball.jpg')

    .. image:: ../../examples/images/superball.jpg
     :width: 50 %
     :align: center
     :alt: superball

    **Superball scaling** with :math:`q/p^{1/3}` close to sphere shape with p=1.
    Small deviations from sphere (as a kind of long wavelength roughness) cannot be discriminated from polydispersity
    or small ellipsoidality.
    ::

     import jscatter as js
     import numpy as np
     q=np.r_[0:5:0.02]
     R=3

     Fq=js.dL()
     for i,p in enumerate([0.5,0.8,0.9,1,1.115,1.3,2],1):
         fq=js.ff.superball(q,R,p=p,nGrid=20)
         Fq.append(fq)

     pp=js.grace()
     pp.multi(2,1,vgap=0.2)
     for fq in Fq[1:-1]:
         pp[0].plot(fq.X,fq.Y/fq.Y[0],sy=[-1,0.2,-1],le=f'{fq.rounding_p:.2g}')
         pp[1].plot(fq.X*fq.rounding_p**(1/3),fq.Y/fq.Y[0],sy=[-1,0.2,-1],le=f'{fq.rounding_p:.2g}')
     fq=Fq[0]
     pp[0].plot(fq.X,fq.Y/fq.Y[0],sy=0,li=[1,2,-1],le=f'{fq.rounding_p:.2g}')
     pp[1].plot(fq.X*fq.rounding_p**(1/3),fq.Y/fq.Y[0],sy=0,li=[1,2,-1],le=f'{fq.rounding_p:.2g}')
     fq=Fq[-1]
     pp[0].plot(fq.X,fq.Y/fq.Y[0],sy=0,li=[3,2,-1],le=f'{fq.rounding_p:.2g}')
     pp[1].plot(fq.X*fq.rounding_p**(1/3),fq.Y/fq.Y[0],sy=0,li=[3,2,-1],le=f'{fq.rounding_p:.2g}')

     pp[0].legend(x=0.2,y=0.05)
     pp[0].yaxis(label='I(q)',scale='l')
     pp[1].yaxis(label='I(q)',scale='l')
     pp[0].xaxis(label='q / nm')
     pp[1].xaxis(label=r'q/p\S1/3\N')
     pp[0].title('superball scaling')
     pp[0].subtitle('p=0.5 octahedron, p=1 sphere, p>10 cube')
     pp[1].text(r'q scaled by p\S-1/3\nclose to p=1 I(q) scales to similar shape ',x=4,y=0.1)
     pp[0].text('original',x=4,y=0.1)
     #p.save(js.examples.imagepath+'/superballscaling.jpg')

    .. image:: ../../examples/images/superballscaling.jpg
     :width: 50 %
     :align: center
     :alt: superballscaling



    References
    ----------
    .. [1] Periodic lattices of arbitrary nano-objects: modeling and applications for self-assembled systems
           Yager, K.G.; Zhang, Y.; Lu, F.; Gang, O.
           Journal of Applied Crystallography 2014, 47, 118–129. doi: 10.1107/S160057671302832X
    .. [2] http://gisaxs.com/index.php/Form_Factor:Superball

    """
    p2 = abs(2. * min(p, 101.))
    R = abs(R)
    q = np.atleast_1d(q)
    contrast = SLD - solventSLD
    # volume according to Soft Matter, 2012, 8, 8826-8834, DOI: 10.1039/C2SM25813G
    frac = special.gamma(1 + 1 / p2) ** 3 / special.gamma(1 + 3 / p2)
    V = 8 * R ** 3 * frac

    # superball surface radius for a point,
    # a definition of radius in p2 exponent as
    # r = lambda xyz: (np.abs(xyz[:, :3]) ** p2).sum(axis=1) ** (1. / p2)
    # The same is calculated in numpy.linalg.norm(xyz,ord=p2,axis=1) but faster

    # The integration using pseudorandom grid is as fast as 3D GaussIntegration of same quality looking at high Q
    # accuracy (deviation from analytic sphere/cube)
    # pseudorandom grid
    grid = sf.pseudoRandomLattice([2 * R, 2 * R, 2 * R], int(nGrid ** 3 / frac), b=0)
    grid.move([-R, -R, -R])  # move to zero center
    # select according to p2 norm <R
    grid.set_bsel(1, np.linalg.norm(grid.XYZall, ord=p2, axis=1) < R)
    grid.prune(grid.ball > 0)

    if returngrid:
        return grid

    # calc scattering
    result = cloudScattering(q, grid, relError=nGrid * 4)
    result.columnname = 'q; Iq; beta; fa'
    result.Y = result.Y * V ** 2 * contrast ** 2
    result.modelname = inspect.currentframe().f_code.co_name
    result.R = R
    result.Volume = V
    result.rounding_p = p2 / 2.
    result.contrast = contrast
    result.I0 = V ** 2 * contrast ** 2

    return result


def _mVD(Q, kk, N):
    # in the paper N and n are both the same.
    q = Q  # np.float128(Q) # less numeric noise at low Q with float128 but 4 times slower
    K = kk  # np.float128(kk)
    K2 = K * K
    K3 = K2 * K
    K4 = K3 * K
    K5 = K4 * K
    K6 = K5 * K
    K7 = K6 * K
    K8 = K7 * K
    NN = N * N
    NNN = N * N * N
    K2m1 = K2 - 1
    K2p1 = K2 + 1
    KN2 = K ** (N + 2)
    D = (-6. * K2m1 * K2p1 * (K4 + 5 * K2 + 1) * NN + (-6 * K8 - 12 * K6 + 48 * K4 + 48 * K2 + 6) * N + (
            3 * K8 + 36 * K6 + 24 * K4 - 18 * K2 - 3.)) * np.sin(q * (2 * N + 1))
    D += ((3 * K8 - 12 * K6 - 45 * K4 - 24 * K2 - 3) * NN + (6 * K8 - 12 * K6 - 72 * K4 - 48 * K2 - 6) * N + (
            3 * K8 + 18 * K6 - 24 * K4 - 36 * K2 - 3.)) * np.sin(q * (2 * N - 1))
    D += ((3 * K8 + 24 * K6 + 45 * K4 + 12 * K2 - 3) * NN + 6 * K2 * (3 * K2 + 2) * N + 3 * K2 * (
            4 * K4 - K2 - 6.)) * np.sin(q * (2 * N + 3))
    D += (18 * K4 * K2p1 * NN + 6 * K2 * (6 * K4 + 3 * K2 - 2) * N + 3 * K2 * (6 * K4 + K2 - 4.)) * np.sin(
        q * (2 * N - 3))
    D += (-18 * K2 * K2p1 * NN - 6 * K4 * (2 * K2 + 3) * N - 3 * K4) * np.sin(q * (2 * N + 5))
    D += (3 * K4 * NN + 6 * K4 * N + 3 * K4) * np.sin(q * (2 * N - 5))
    D += (-3 * K4 * NN) * np.sin(q * (2 * N + 7))
    D += (6 * K3 * (3 * K4 + 10 * K2 + 5) * NN + 6 * K3 * (3 * K4 + 8 * K2 + 3) * N - 12 * K * K2m1 * (
            K4 + 3 * K2 + 1.)) * np.sin(q * 2 * N)
    D += (K * (-12 * K6 - 12 * K4 + 12 * K2 + 6) * NN - 6 * K * (2 * K2 + 3) * (2 * K4 - 2 * K2 - 1) * N + K * (
            -12 * K6 - 12 * K4 + 36 * K2 + 12.)) * np.sin(q * (2 * N - 2))
    D += (K * (-30 * K4 - 60 * K2 - 18) * NN + K * (-42 * K4 - 72 * K2 - 18) * N + K * (
            -12 * K6 - 36 * K4 + 12 * K2 + 12.)) * np.sin(q * (2 * N + 2))
    D += (-6 * K3 * (2 * K2 + 1) * NN - 6 * K3 * (4 * K2 + 1.) * N - 12 * K5) * np.sin(q * (2 * N - 4))
    D += (-6 * K * (K6 + 2 * K4 - 2 * K2 - 2) * NN + 6 * K3 * (K4 + 4 * K2 + 2.) * N + 12 * K3) * np.sin(
        q * (2 * N + 4))
    D += (6 * K3 * (K2 + 2.) * NN + 6 * K5 * N) * np.sin(q * (2 * N + 6))

    D += (6 * K2m1 * K2p1 * (K4 + 4 * K2 + 1) * NNN + 3 * (K4 - 4 * K2 - 3) * (3 * K4 + 8 * K2 + 1) * NN + (
            3 * K8 - 36 * K6 - 120 * K4 - 60 * K2 - 3) * N + 42 * K2 * (K4 - 4 * K2 + 1.)) * np.sin(q)
    D += (-2 * K2m1 * K2p1 * (K4 - K2 + 1) * NNN + (-3 * K8 + 9 * K6 + 3 * K2 + 3) * NN + (
            -K8 + 7 * K6 + 5 * K2 + 1) * N + 6 * K2 * (-4 * K4 + 11 * K2 - 4.)) * np.sin(3 * q)
    D += (-6 * K2 * K2m1 * K2p1 * NNN - 3 * K2 * (K4 - 8 * K2 - 5) * NN + 3 * K2 * (K4 + 8 * K2 + 3) * N + 6 * K2 * (
            K4 - K2 + 1.)) * np.sin(5 * q)
    D += (-6 * K * K2m1 * (2 * K2 + 1) * (K2 + 2) * NNN + K * (-12 * K6 + 48 * K4 + 102 * K2 + 24) * NN + K * (
            66 * K4 + 84 * K2 + 12) * N + 24 * K3 * K2p1) * np.sin(2 * q)
    D += (6 * K * K2m1 * K2p1 * K2p1 * NNN + 6 * K * K2p1 * (K4 - 5 * K2 - 2) * NN - 6 * K * K2p1 * (
            5 * K2 + 1) * N - 12 * K3 * K2p1) * np.sin(4 * q)
    D += (2 * K3 * K2m1 * NNN - 6 * K3 * NN - 2 * K3 * (K2 + 2.) * N) * np.sin(6 * q)

    D += KN2 * K2m1 * np.sin(q * N + 0) * K * (-72 - 12 * N * (3 * K2 + 4))
    D += KN2 * K2m1 * np.sin(q * (N - 1)) * (12 * (3 * K2 - 2) - 12 * N * (K2 + 2.))
    D += KN2 * K2m1 * np.sin(q * (N + 1)) * (-12 * (2 * K2 - 3) + 12 * N * (4 * K2 + 3.))
    D += KN2 * K2m1 * np.sin(q * (N - 2)) * K * (48 + 6 * N * (4 * K2 + 7.))
    D += KN2 * K2m1 * np.sin(q * (N + 2)) * K * (48 + 12 * N * (2 * K2 + 1.))
    D += KN2 * K2m1 * np.sin(q * (N - 3)) * (-6 * (4 * K2 - 1) - 6 * N * (2 * K2 - 1.))
    D += KN2 * K2m1 * np.sin(q * (N + 3)) * (6 * (K2 - 4) - 6 * N * (7 * K2 + 4.))
    D += KN2 * K2m1 * np.sin(q * (N - 4)) * K * (-12 - 6 * N * (K2 + 2.))
    D += KN2 * K2m1 * np.sin(q * (N + 4)) * K * (-12 - 6 * N * (K2 - 2.))
    D += KN2 * K2m1 * np.sin(q * (N - 5)) * K2 * (6. + 6 * N)
    D += KN2 * K2m1 * np.sin(q * (N + 5)) * (6 + 6 * N * (2 * K2 + 1.))
    D += KN2 * K2m1 * np.sin(q * (N + 6)) * K * (-6. * N)

    return D  # np.float64(D)


def _gauss(x, a, s):
    # Gaussian with normalized to have Integral s
    return np.exp(-0.5 * (x - a) ** 2 / s ** 2) / np.sqrt(2 * np.pi)


def _monomultilayer(q, layer, sld, gwidth, pos, edges, mima):
    # monodisperse multilayer, this is the kernel to calculate multilayer
    #  layer, sld, gwidth, pos, edges are all arrays with corresponding values for all layers
    # mima is [minimum, maximum and max gaussian width] for x estimate

    # array of phases for later einsum over layers j,k in second,third indices, distance of layers
    phase = np.cos(q[:, None, None] * (pos - pos[:, None])) * sld * sld[:, None]
    cphase = np.exp(q[:, None] * pos * 1j) * sld

    # x for contrastprofile
    x = np.r_[mima[0]- mima[2]*3 * 1.2:mima[1] + mima[2]*3 * 1.2:500j]

    # aq are formfactor amplitudes for layers
    aq = np.zeros((q.shape[0], sld.shape[0]))
    contrastprofile=[]

    if edges is not None:
        # box contributions
        aq[:, gwidth <= 0] = np.sinc(q[:, None] * layer / 2. / np.pi) * layer
        contrastprofile.extend([formel.box(x, [a, e]).Y * s
                                for a, e, s in zip(edges[:-1], edges[1:], sld[gwidth <= 0])])

    # gaussian contributions
    aq[:, gwidth > 0] = np.exp(-q[:, None] ** 2 * gwidth[gwidth > 0] ** 2 / 2.) * gwidth[gwidth > 0]
    contrastprofile.extend([_gauss(x, a, e) * s for a, e, s in
                            zip(pos[gwidth > 0], gwidth[gwidth > 0], sld[gwidth > 0])])

    # calc fomfactor, <|F|²> = <F*F.conj> result in this real phase
    Fq = np.einsum('ij,ijk,ik->i', aq, phase, aq)
    # formfactor amplitude fa for later  |<fa²>| with complex phase
    fa = np.einsum('ij,ij->i', aq, cphase)
    result = dA(np.c_[q, Fq].T)
    result.contrastprofile = dA(np.c_[x, np.sum(contrastprofile, axis=0)].T)
    result.fa = fa.real
    return result


def multilayer(q, layerd=None, layerSLD=None, gausspos=None, gaussw=None, gaussSLD=None, ds=0, solventSLD=0):
    r"""
    Form factor of a multilayer with rectangular/Gaussian density profiles perpendicular to the layer.

    To describe smeared interfaces or complex profiles use more layers.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    layerd : list of float
        Thickness of box layers in units nm.
        List gives consecutive layer thickness from center to outside.
    layerSLD : list of float
        Scattering length density of box layers in units 1/nm².
        Total scattering per box layer is (layerSLD[i]*layerd[i])²
    gausspos : list of float
        Centers of gaussians layers in units nm.
    gaussw : list of float
        Width of Gaussian.
    gaussSLD : list of float
        Scattering length density of Gaussians layers in 1/nm².
        Total scattering per Gaussian layer is (gaussSLD[i]*gaussw[i])²
    ds : float, list
        - float
           Gaussian thickness fluctuation (sigma=ds) of central layer in above lamella in nm.
           The thickness of the central layer is varied and all consecutive position are shifted
           (gausspos + layer edges).
        - list, ds[0]='outersld','innersld','inoutsld','centersld', ds[1..n+1]= w[i]
           SLD fluctuations in a layer.
           The factor 0 < f[i]=i/n < 1 determines the SLD of the outer layer occurring with
           a probability w[i] as f[i]*sld.
           E.g. parabolic profile ``ds=['outersld',np.r_[0:1:7j]**2]``
           or upper half ``ds=['outersld',np.r_[0,0,0,0,1,1,1,1]]``

    solventSLD : float, default=0
        Solvent scattering length density in 1/nm².

    Returns
    -------
    dataArray
        Columns [q, Fq, Fa2]
         - Fq :math:`F(q)=<\sum_{ij} F_a(q,i)F_a^*(q,j)>` is multilayer scattering per layer area.
         - Fa2 :math:`Fa2(q)=<\sum_{i} F_a(q,i)>^2` described fluctuations in the multilayer for given *ds*.
           Might be used for stacks of multilayers and similar.
         - To get the scattering intensity of a volume the result needs to be multiplied with the layer area [2]_.
         - .contrastprofile    contrastprofile as contrast to solvent SLD.
         - .profilewidth
         - ....

    Notes
    -----
    The scattering amplitude :math:`F_a` is the Fourier transform of the density profile :math:`\rho(r)`

    .. math:: F_a(q)=\int \rho(r)e^{iqr}dr

    For a rectangular profile [1]_ of thickness :math:`d_i` centered at :math:`a_i` and
    layer scattering length density :math:`\rho_i` we find

    .. math:: F_{a,box}(q)= \rho_i d_i sinc(qd_i/2)e^{iqa_i}

    For a Gaussian profile [2] :math:`\rho(r) = \frac{\rho_i}{\sqrt{2\pi}}e^{-r^2/s_i^2/2}` with width :math:`s_i`
    and same area as the rectangular profile :math:`\rho_is_i = \rho_id_i` we find

    .. math:: F_{a,gauss}(q)= \rho_i s_i e^{-(q^2s_i^2/2)}e^{iqa_i}

    The scattering amplitude for a multi box/gauss profile is :math:`F_a(q)=\sum_i F_a(q,i)`

    The formfactor :math:`F(q)` of this multi layer profile is in average :math:`<>`

    .. math:: F(q)=<\sum_{ij} F_a(q,i)F_a^*(q,j)>

    resulting e.g. for a profile of rectangular boxes in

    .. math:: F_{box}(q)=\sum_{i,j} \rho_i\rho_j d_i d_j sinc(qd_i)sinc(qd_j)cos(q(a_i-a_j))

    To get the 3D orientational average one has 2 options:
     - add a Lorentz correction :math:`q^{-2}` to describe the correct scattering in isotropic average (see [2]_).
       Contributions of multilamellarity resulting in peaky structure at low Q are ignored.
     - Use *multilamellarVesicles* which includes a full structure factor and also size averaging.
       The Lorentz correction is included as the limiting case for high Q.
       Additional the peaky structure at low Q is described as a consequence of the multilamellarity.
       See :ref:`Multilamellar Vesicles` for examples.

    Approximately same minimum for gaussian and box profiles is found for :math:`s_i = d_i/\pi`.
    To get same scattering I(0) the density needs to be scaled :math:`\rho_i\pi`.

    **Restricting parameters for Fitting**
     If the model is used during fits one has to consider dependencies between the parameters
     to restrict the number of free parameters. Symmetry in the layers may be used to restrict
     the parameter space.

    Examples
    --------
    Some symmetric box and gaussian profiles in comparison.
    An exact match is not possible but the differences are visible only in higher order lobes.
    ::

     import jscatter as js
     import numpy as np
     q=np.r_[0.01:5:0.001]
     p=js.grace()
     p.multi(2,1)
     p[0].title('multilayer membranes')
     p[0].text(r'I(0) = (\xS\f{}\si\NSLD[i]*width[i])\S2',x=0.5,y=80)
     p[0].text(r'equal minimum using \n2width\sgauss\N=width\sbox\N 2/\xp', x=0.7, y=25)
     profile=np.r_[2,1,2]
     #
     pf1=js.ff.multilayer(q,layerd=[1,5,1],layerSLD=profile)
     p[0].plot(pf1,sy=[1,0.3,1],le='box')
     p[1].plot(pf1.contrastprofile,li=[1,2,1],sy=0,le='box only')
     #
     # factor between sigma and box width
     f=2 * 3.141/2
     pf2=js.ff.multilayer(q,gausspos=np.r_[0.5,3.5,6.5],gaussSLD=profile*f,gaussw=np.r_[1,5,1]/f)
     p[0].plot(pf2,sy=[2,0.3,2],le='gauss')
     p[1].plot(pf2.contrastprofile,li=[1,2,2],sy=0,le='gauss only')
     #
     pf3=js.ff.multilayer(q,layerd=[1,5,1],layerSLD=[0,1,0],gausspos=np.r_[0.5,6.5],gaussSLD=[2*f,2*f],gaussw=np.r_[1,1]/f)
     p[0].plot(pf3,sy=[3,0.3,3],le='gauss-box-gauss')
     p[1].plot(pf3.contrastprofile,li=[1,2,3],sy=0,le='gauss-box-gauss')

     pf3=js.ff.multilayer(q,layerd=[1,5,1],layerSLD=[0,1,0],gausspos=np.r_[0.5,6.5],gaussSLD=[2*f,2*f],gaussw=np.r_[1,1]/f,ds=0.8)
     p[0].plot(pf3,sy=0,li=[1,2,4],le='gauss-box-gauss with fluctuations')
     p[1].plot(pf3.contrastprofile,li=[1,2,4],sy=0,le='gauss-box-gauss')

     p[0].yaxis(scale='n',min=0.001,max=90,label='I(Q)',charsize=1)#,ticklabel=['power',0,1]
     p[0].xaxis(label='',charsize=1)
     p[1].yaxis(label='contrast profile ()')
     p[0].xaxis(label='position / nm')
     p[1].xaxis(label='Q / nm\S-1')
     p[0].legend(x=2.5,y=70)
     #p.save(js.examples.imagepath+'/multilayer.jpg')

    .. image:: ../../examples/images/multilayer.jpg
     :width: 50 %
     :align: center
     :alt: multilayer membrane

    **How to use in a fit model**
    Due to the large number of possible models (e.g. 9 Gaussians with each 3 parameters), smearing and more
    one has to define what seems to be important and use symmetries to reduce the parameter space.

    Complex profiles with tens of layers are possible and may be defined like this: ::

     # 5 layer box model
     def box5(q,d1,d2,d3,s1,s2):
        # symmetric model with 5 layers, d1 central, d3 outer
        # outer layers have half the scattering length density of d2
        result=js.ff.multilayer(q,layerd=[d3,d2,d1,d2,d3],layerSLD=[s2/2,s2,s1,s2,s2/2],solventSLD=0)
        return result

    **A model of Gaussians**
    We describe a symmetric bilayer with a center Gaussian and 2 Gaussians at each side to describe the head groups.
    ::

     # define symmetric 3 gaussian model according to positions p_i of the Gaussian centers.
     def gauss3(q,p1,p2,s1,s2,s0,w1,w2,w0):
         # define your model
         p0=0
         pos = np.r_[-p2,-p1,p0,p1,p2]  # symmetric positions
         result=js.ff.multilayer(q,gausspos=pos,gaussSLD=[s2,s1,s0,s1,s2],gaussw=[w2,w1,w0,w1,w2],solventSLD=0)
         return result

    References
    ----------
    Multi box profile
     .. [1] Modelling X-ray or neutron scattering spectra of lyotropic lamellar phases :
            interplay between form and structure factors
            F. Nallet, R. Laversanne, D. Roux  Journal de Physique II, EDP Sciences, 1993, 3 (4), pp.487-502
            https://hal.archives-ouvertes.fr/jpa-00247849/document

    Gaussian profile
     .. [2] X-ray scattering from unilamellar lipid vesicles
            Brzustowicz and Brunger, J. Appl. Cryst. (2005). 38, 126–131
     .. [3] Structural information from multilamellar liposomes at full hydration:
            Full q-range fitting with high quality X-ray data.
            Pabst, G., Rappolt, M., Amenitsch, H. & Laggner, P.
            Phys. Rev. E - Stat. Physics, Plasmas, Fluids, Relat. Interdiscip. Top. 62, 4000–4009 (2000).

    """
    if isinstance(layerd, numbers.Number) and layerd >0:
        layerd = [layerd]
    if isinstance(layerSLD, numbers.Number): layerSLD = [layerSLD]
    if isinstance(gausspos, numbers.Number): gausspos = [gausspos]
    if isinstance(gaussw, numbers.Number) and gaussw>0:
        gaussw = [gaussw]
    if isinstance(gaussSLD, numbers.Number): gaussSLD = [gaussSLD]

    if layerSLD is not None:
        layerSLD = np.atleast_1d(layerSLD) - solventSLD  # contrast
        layer = np.abs(np.atleast_1d(layerd[:len(layerSLD)]))
        # layers center positions additive from zero
        edges = np.r_[0, np.cumsum(layer)]
        if len(layerd)>len(layerSLD) and layerd[-1][0] == 'c':
            # 'centered', center layers around zero
            edges = edges - edges[-1] / 2.
        layerpos = edges[:-1] + np.diff(edges) / 2  # pos is centers of layers
    else:
        layerpos = []
        layerSLD = []
        edges = []
        layer = []
    if gaussSLD is not None:
        gausspos = np.atleast_1d(gausspos)
        gaussSLD = np.atleast_1d(gaussSLD) - solventSLD  # contrast
        gaussw = np.abs(np.atleast_1d(gaussw))
    else:
        gausspos = []
        gaussSLD = []
        gaussw = []

    pos = np.r_[layerpos, gausspos]
    sld = np.r_[layerSLD, gaussSLD]
    # gwidth <0 will select box layers
    gwidth = np.r_[[-1]*len(layerSLD), gaussw]
    # min max, width  estimate profile
    mima = [min(np.r_[edges, pos]), max(np.r_[edges, pos]), np.max(np.r_[gwidth, 0.])]
    center = (np.min(pos) + np.max(pos)) / 2

    if isinstance(ds, numbers.Number) and ds > 0:
        # fluctuations in central layer, integrate over normal distribution with width ds
        ns=23  # odd number of points in gaussian
        x, w = formel.gauss(np.r_[-2 * ds:2 * ds:ns*1j], 0, ds).array
        # calc fq for all x
        fq=dL()
        for dx in x/2:
            dpos = pos + np.where(pos > center, dx, -dx)
            dedges = edges + np.where(edges > center, dx, -dx)
            dlayer = np.diff(dedges)
            fq.append(_monomultilayer(q=q, layer=dlayer, sld=sld, gwidth=gwidth, pos=dpos, edges=dedges, mima=mima))

        # average fq with weights
        Fq = (fq.Y.array * w[:, None]).sum(axis=0) / w.sum()
        Fa2 = ((fq.fa.array * w[:, None]).sum(axis=0) / w.sum())**2
        contrastprofile = fq[int((ns-1)/2)].contrastprofile
        # average contrastprofile
        contrastprofile.Y = (fq.contrastprofile.array[:, 1, :] * w[:, None]).sum(axis=0) / w.sum()
    elif isinstance(ds, (list, tuple)) and ds[0] in ['outersld', 'innersld', 'inoutsld', 'centersld']:
        # indices to change
        dil={'outersld': pos>=pos.max(),
             'innersld': pos<=pos.min(),
             'inoutsld': (pos>=pos.max()) | (pos<=pos.min()),
             'centersld': pos == np.sort(pos)[int(len(pos)/2)]}

        fq=dL()
        dsld = np.copy(sld)
        w = np.squeeze(ds[1:])  # weights
        for dx in np.r_[0:1:len(w)*1j]:
            dsld[dil[ds[0]]] = dx * sld[dil[ds[0]]]
            fq.append(_monomultilayer(q=q, layer=layer, sld=dsld, gwidth=gwidth, pos=pos, edges=edges, mima=mima))

        # average fq with weights
        Fq = (fq.Y.array * w[:, None]).sum(axis=0) / w.sum()
        Fa2 = ((fq.fa.array * w[:, None]).sum(axis=0) / w.sum())**2
        contrastprofile = fq[0].contrastprofile
        # average contrastprofile
        contrastprofile.Y = (fq.contrastprofile.array[:, 1, :] * w[:, None]).sum(axis=0) / w.sum()

    else:
        # single monodispers
        fq = _monomultilayer(q=q, layer=layer, sld=sld, gwidth=gwidth, pos=pos, edges=edges, mima=mima)
        Fq = fq.Y
        Fa2 = np.zeros_like(q)  # no diffuse scattering for monodispers multilayer
        contrastprofile = fq.contrastprofile

    result = dA(np.c_[q, Fq, Fa2].T)
    result.modelname = inspect.currentframe().f_code.co_name
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Fq; Fa2'
    result.contrastprofile = contrastprofile
    result.thicknessfluctuation = ds
    result.solventSLD = solventSLD
    result.layerthickness = layerd
    result.layerSLD = layerSLD
    result.layerpos = layerpos
    result.gausspos = gausspos
    result.gaussSLD = gaussSLD
    result.gausswidth = gaussw
    result.profilewidth = (mima[1]+mima[2]) - (mima[0]-mima[2])
    return result


def _mVSzero(q, N):
    S = 0.5 + 3. / (4 * N * (N + 0.5) * (N + 1)) * (
            np.cos(2 * q * (N + 1)) * ((N + 1) ** 2 - (N + 1) / (np.sin(q) ** 2)) +
            np.sin(2 * q * (N + 1)) / np.tan(q) * (-(N + 1) ** 2 + 1 / (2 * np.sin(q) ** 2)))
    return S / N ** 2 / q ** 2


def _mVSone(q, N):
    S = 3. / (N ** 3 * (N + 0.5) * (N + 1)) * (-0.5 * np.cos(q * (N + 0.5)) * (N + 0.5) +
                                               0.25 * np.sin(q * (N + 0.5)) / np.tan(q / 2.)) ** 2
    return S / (q * np.sin(q / 2)) ** 2


def _mVS(Q, R, displace, N):
    q = Q * R / N
    if N == 1:
        # a single shell ; see Frielinghaus below equ. 5
        return np.sinc(Q * R / np.pi) ** 2
    if displace == 0:
        return _mVSone(q, N)
    # for N > 1
    Sq = np.ones_like(Q)
    K = _fa_sphere(Q * displace)

    # booleans to decide which solution
    limit = 1e-3
    kzerolimit = limit * 0.5 * (6 * N ** 5 + 15 * N ** 4 + 10 * N ** 3 - N) / (6. * N ** 5 - 10 * N ** 3 + 4 * N)
    konelimit = limit * (420. / 36 * (4. * N ** 6 + 12 * N ** 5 + 13 * N ** 4 + 6 * N ** 3 + N ** 2) /
                         (10. * N ** 7 + 36. * N ** 6 + 21. * N ** 5 - 35 * N ** 4 - 35 * N ** 3 + 4 * N))
    kone = K > 1 - konelimit
    try:
        # above minimum Q with K <kzerolimit always use the kzero solution to get smooth solution
        Qmin = np.min(Q[K < kzerolimit])
    except ValueError:
        # This happens when kzerolimit is not in Q range and kzero should be always False
        Qmin = np.max(Q) + 1
    kzero = Q > Qmin
    kk = ~(kzero | kone)
    # cases as described in Frielinghaus equ 12 and 13 and full solution (kk)
    S0 = _mVSzero(q, N)
    Sq[kzero] = S0[kzero]
    Sq[kone] = _mVSone(q[kone], N)
    qkk = q[kk]
    D = _mVD(qkk, K[kk], N)
    divisor = (-48. * np.sin(qkk) ** 3 * (K[kk] ** 2 + 1 - 2 * K[kk] * np.cos(qkk)) ** 4 * qkk ** 2)
    sq = D * 3. / (N ** 3 * (N + 0.5) * (N + 1)) / divisor
    # for some values divisor and D become both small (machine precision) introducing errors
    # these are approximated by _mVSzero which has minima at the same positions
    qsing = (np.abs(D) < 1e-7) & (np.abs(divisor) < 1e-7) & (S0[kk] < 1e-4)
    sq[qsing] = _mVSzero(qkk[qsing], N)

    Sq[kk] = sq
    return Sq  # ,_mVD( q, K,N),(-48.*np.sin(q)**3 * (K**2 + 1 - 2*K * np.cos(q))**4 * q**2),_mVSone(q,N)


def _discrete_gaussian_kernel(mean, sig, Nmax):
    # generates a truncated discrete gaussian distribution with integrated probabilities in the interval's
    if sig < 0.4:
        # some default values for a single shell
        return [mean], [1], mean, 0
    if Nmax == 0:
        b = 10  # 10 sigma is large enough and >5*sig
    else:
        b = (Nmax - mean) / sig
    nn = np.floor(np.r_[mean - 5 * sig:mean + 5 * sig])
    nn = nn[nn > 0]
    cdf = scipy.stats.truncnorm.cdf(np.r_[nn - 0.5, nn[-1] + 0.5], a=(0.5 - mean) / sig, b=b, loc=mean, scale=sig)
    m, v = scipy.stats.truncnorm.stats(a=(0.5 - mean) / sig, b=10, loc=mean, scale=sig, moments='mv')
    pdf = np.diff(cdf)
    take = pdf > 0.005
    return nn[take], pdf[take] / np.sum(pdf[take]), m, v ** 0.5


def multilamellarVesicles(Q, R, N, phi, displace=0, dR=0, dN=0, nGauss=100, **kwargs):
    r"""
    Scattering intensity of a multilamellar vesicle with random displacements of the inner vesicles [1]_.

    The result contains the full scattering, the structure factor of the lamella and a multilayer formfactor of the
    lamella layer structure. Other layer structures as mentioned in [2].
    Multilayer formfactor is described in :py:func:`~.formfactor.multilayer`.

    Parameters
    ----------
    Q : float
        Wavevector in 1/nm.
    R : float
        Outer radius of the Vesicle in units nm.
    dR : float
        Width of outer radius distribution in units nm.
    displace : float
        Displacements of the vesicle centers in units nm.
        This describes the displacement steps in a random walk of the centers.
        displace=0 it is concentric, all have same center. displace< R/N.
    N : int
        Number of lamella.
    dN : int, default=0
        Width of distribution for number of lamella. (dN< 0.4 is single N)
        A zero truncated normal distribution is used with N>0 and N<R/displace.
        Check .Ndistribution and .Nweight = Nweight for the resulting distribution.
    phi : float
        Volume fraction :math:`\phi` of layers inside of vesicle.
    nGauss : int, default 100
        Number of Gaussian quadrature points in integration over dR distribution.
    Lamella formfactor parameters (see multilayer) :
    layerd : list of float
        Thickness of box layers in units nm.
        List gives consecutive layer thickness from center to outside.
    layerSLD : list of float
        Scattering length density of box layers in units 1/nm².
        Total scattering per box layer is layerSLD[i]*layerd[i]
    gausspos : list of float
        Centers of gaussians layers in units nm.
    gaussw : list of float
        Width of Gaussian.
    gaussSLD : list of float
        Scattering length density of Gaussians layers in 1/nm².
        Total scattering per Gaussian layer is gaussSLD[i]*gaussw[i]
    ds : float
        Gaussian thickness fluctuation (sigma=ds) of central layer in above lamella in nm.
        The thickness of the central layer is varied and all consecutive position are shifted (gausspos + layer edges).
    solventSLD : float, default=0
        Solvent scattering length density in 1/nm².

    Returns
    -------
    dataArray
        Columns [q,I(q),S(q),F(q)]
         - I(q)=S(q)F(q)  scattering intensity
         - S(q) multilamellar vesicle structure factor
         - F(q) lamella formfactor
         - .columnname='q;Iq;Sq;Fq'
         - .outerShellVolume
         - .Ndistribution
         - .Nweight
         - .displace
         - .phi
         - .layerthickness
         - .SLD
         - .solventSLD
         - .shellfluctuations=ds
         - .preFactor=phi*Voutershell**2
        Multilayer attributes (see multilayer)
         - .contrastprofile ....

    Notes
    -----
    The left shows a concentric lamellar structure.
    The right shows the random path of the consecutive centers of the spheres.
    See :ref:`Multilamellar Vesicles` for resulting scattering curves.

    .. image:: MultiLamellarVesicles.png
     :align: center
     :height: 200px
     :alt: Image of MultiLamellarVesicles


    The function returns I(Q) as (see [1]_ equ. 17 )

    .. math:: I(Q)=\phi V_{outershell} S(Q) F(Q)

    with the multishell structure factor :math:`S(Q)` as described in [1]_.
    For a single layer we have the formfactor F(Q)

    .. math:: F(Q)= ( \sum_i \rho_i d_i sinc( Q d_i) )^2

    with :math:`\rho_i` as scattering length density and thickness :math:`d_i`.
    For a complex multilayer we find (see :py:func:`multilayer`)

    .. math:: F(Q)= \sum_{i,j} \rho_i\rho_j d_i d_j sinc(qd_i)sinc(qd_j)cos(q(a_i-a_j))

    with :math:`a_i` as positions of the layers.

    - The amphiphile concentration phi
      is roughly given by phi = d/a, with d being the bilayer thickness
      and a being the spacing of the shells. The spacing of the
      shells is given by the scattering vector of the first correlation
      peak, i.e., a = 2pi/Q. Once the MLVs leave considerable
      space between each other then phi < d/a holds. This condition
      coincides with the assumption of dilution of the Guinier law. (from [1]_)
    - Structure factor part is normalized that :math:`S(0)=\sum_{j=1}^N (j/N)^2`
    - To use a different shell form factor the structure factor is given explicitly.
    - Comparing a unilamellar vesicle (N=1) with multiShellSphere shows that
      R is located in the center of the shell::

        import jscatter as js
        import numpy as np
        Q=js.loglist(0.0001,5,1000)#np.r_[0.01:5:0.01]
        ffmV=js.ff.multilamellarVesicles
        p=js.grace()
        p.multi(1,2)
        # comparison single layer
        mV=ffmV(Q=Q, R=100., displace=0, dR=0,N=1,dN=0, phi=1,layerd=6, layerSLD=1e-4)
        p[0].plot(mV)
        p[0].plot(js.ff.multiShellSphere(Q,[97,6],[0,1e-4]),li=[1,1,3],sy=0)
        # triple layer
        mV1=ffmV(Q=Q, R=100., displace=0, dR=0,N=1,dN=0, phi=1,layerd=[1,4,1], layerSLD=[0.07e-3,0.6e-3,0.07e-3])
        p[1].plot(mV1,sy=[1,0.5,2])
        p[1].plot(js.ff.multiShellSphere(Q,[97,1,4,1],[0,0.07e-3,0.6e-3,0.07e-3]),li=[1,1,4],sy=0)
        p[1].yaxis(label='S(Q)',scale='l',min=1e-10,max=1e6,ticklabel=['power',0])
        p[0].yaxis(label='S(Q)',scale='l',min=1e-10,max=1e6,ticklabel=['power',0])
        p[1].xaxis(label='Q / nm\S-1',scale='l',min=1e-3,max=5,ticklabel=['power',0])
        p[0].xaxis(label='Q / nm\S-1',scale='l',min=1e-3,max=5,ticklabel=['power',0])

    Examples
    --------
    See :ref:`Multilamellar Vesicles`

    Scattering length densities and sizes roughly for DPPC from
     Kučerka et al. Biophysical Journal. 95,2356 (2008)
     https://doi.org/10.1529/biophysj.108.132662
    The SAX scattering is close to matching resulting in low scattering at low Q.
    The specific structure depends on the lipid composition and layer thickness.
    Kučerka uses a multi (n>6) Gauss profile where we use here approximate values in a simple 3 layer box profile
    to show the main characteristics.

    ::

     import jscatter as js
     import numpy as np

     ffmV=js.ff.multilamellarVesicles
     Q=js.loglist(0.02,8,500)
     dd=1.5
     dR=5
     nG=100
     R=50
     N=3
     ds=0.05
     st=[0.75,2.8,0.75]
     p=js.grace(1,1)
     p.title('Lipid bilayer in SAXS/SANS')

     # SAXS
     sld=np.r_[420,290,420]*js.formel.felectron  # unit e/nm³*fe
     sSLD=335*js.formel.felectron  # H2O unit e/nm³*fe
     saxm=ffmV(Q=Q, R=R, displace=dd, dR=dR,N=N,dN=0, phi=0.2,layerd=st, layerSLD=sld,solventSLD=sSLD,nGauss=nG,ds=ds)
     p.plot(saxm,sy=[1,0.3,1],le='SAXS multilamellar')
     saxu=ffmV(Q=Q, R=R, displace=0, dR=dR,N=1,dN=0, phi=0.2,layerd=st, layerSLD=sld,solventSLD=sSLD,nGauss=100,ds=ds)
     p.plot(saxu,sy=0,li=[1,2,4],le='SAXS unilamellar')

     # SANS
     sld=[4e-4,-.5e-4,4e-4]  # unit 1/nm²
     sSLD = 6.335e-4 # D2O
     sanm=ffmV(Q=Q, R=R, displace=dd, dR=dR,N=N,dN=0, phi=0.2,layerd=st, layerSLD=sld,solventSLD=sSLD,nGauss=nG,ds=ds)
     p.plot( sanm,sy=[1,0.3,2],le='SANS multilamellar')
     sanu=ffmV(Q=Q, R=R, displace=0, dR=dR,N=1,dN=0, phi=0.2,layerd=st, layerSLD=sld,solventSLD=sSLD,nGauss=100,ds=ds)
     p.plot(sanu,sy=0,li=[1,2,3],le='SANS unilamellar')
     #
     p.legend(x=1.3,y=1)
     p.subtitle(f'R=50 nm, N={N}, layerthickness={st} nm, dR=5')
     p.yaxis(label='S(Q)',scale='l',min=1e-6,max=1e4,ticklabel=['power',0])
     p.xaxis(label='Q / nm\S-1',scale='l',min=2e-2,max=20,ticklabel=['power',0])

     # contrastprofile
     p.new_graph( xmin=0.6,xmax=0.95,ymin=0.7,ymax=0.88)
     p[1].plot(saxu.contrastprofile,li=[1,4,1],sy=0)
     p[1].plot(sanu.contrastprofile,li=[1,4,2],sy=0)
     p[1].xaxis(label='multiayerprofile')
     p[1].yaxis(label='contrast')
     #p.save(js.examples.imagepath+'/multilamellarVesicles.jpg')

    .. image:: ../../examples/images/multilamellarVesicles.jpg
     :width: 70 %
     :align: center
     :alt: multilamellarVesicles


    References
    ----------
    .. [1] Small-angle scattering model for multilamellar vesicles
           H. Frielinghaus Physical Review E 76, 051603 (2007)
    .. [2] Small-Angle Scattering from Homogenous and Heterogeneous Lipid Bilayers
           N. Kučerka Advances in Planar Lipid Bilayers and Liposomes 12, 201-235 (2010)
    """

    layerd = kwargs.get('layerd', None)
    gaussw = kwargs.get('gaussw', None)

    # shell formfactor
    if phi == 0 or (layerd in [None, 0] and gaussw in [None, 0]):
        # if no good layer parameters are given => no formfactor
        Soutershell = 1
        phi = 1
        Fq = dA(np.c_[Q, np.ones_like(Q)].T)
        Fq.contrastprofile=None
        shellmax = 0
    else:
        Fq= multilayer(q=Q, **kwargs)
        Soutershell = 4 * np.pi * R ** 2  # outer shell surface
        shellmax = Fq.profilewidth

    if N * (displace + shellmax) > R:
        warnings.warn("--->> Warning: layers dont fit inside!!! N=%.3g displace=%.3g R=%.3g" % (N, displace, R))

    # get discrete distribution over N with width dN
    # for small dN this is a single N and N>0
    Nmax = R / displace if displace != 0 else 0
    Ndistrib, Nweight, Nmean, Nsigma = _discrete_gaussian_kernel(N, dN, Nmax)
    if len(Ndistrib) == 0:
        warnings.warn("--->> Warning: layers dont fit inside!!!")
        return -1

    # structure factor
    # define sum over N distribution
    SqR = lambda RR: np.c_[[Nw * _mVS(Q, RR, displace, NN) for NN, Nw in zip(Ndistrib, Nweight)]].sum(axis=0)

    # integrate over dR
    # Sq = np.c_[[Nw * _mVS(Q, R, displace, NN) for NN, Nw in zip(Ndistrib, Nweight)]].sum(axis=0)
    if dR == 0:
        Sq = np.c_[[Nw * _mVS(Q, R, displace, NN) for NN, Nw in zip(Ndistrib, Nweight)]].sum(axis=0)
    else:
        # fixed Gaussian integral over +-3dR
        weight = formel.gauss(np.r_[R - 3 * dR:R + 3 * dR:37j], R, dR).array
        Sq = formel.pQFG(SqR, R - 3 * dR, R + 3 * dR, 'RR', n=nGauss, weights=weight)

    # layer thickness is included in Fq
    result = dA(np.c_[Q, phi * Soutershell ** 2 * Fq.Y * Sq, Sq, Fq.Y].T)
    # result = dA(np.c_[Q, Sq].T)
    result.outerShellVolume = Soutershell * shellmax
    result.Ndistribution = Ndistrib
    result.Nweight = Nweight
    result.displace = displace
    result.phi = phi
    result.preFactor = phi * result.outerShellVolume ** 2
    result.contrastprofile = Fq.contrastprofile
    result.setattr(Fq)
    result.modelname = inspect.currentframe().f_code.co_name
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq; Sq; Fq'
    return result


def decoratedCoreShell(q, Rcore, Rdrop, Ndrop, Hdrop, coreSLD, shellthickness=None, shellSLD=None, dropSLD=None,
                       solventSLD=0, typ='drop', distribution='fibonacci', ndrop=5, relError=100, show=False):
    r"""
    Scattering of a sphere or core shell particle decorated with droplets or disc-like particles.

    The model described a core shell particle decorated with drops or discs.
     - Drops may be added only at the outer surface extending the volume or extending into the inner volume.
     - Discs are only located in the shell describing e.g. liposomes with patches of different lipids or proteins.
     - Using a zero shellthickness drops decorate a sphere like the raspberry model for pickering emulsions.
     - For zero core the disc describes cones.
     - The model might be used to describe a sphere with surface roughness.

    The model uses cloudscattering and the source can be used as a template for more specific models as e.g.
    a bilayer membrane considering head and tail layers or decorated discs larger than the outer shell.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    Rcore : float
        Core radius in nm.
    shellthickness : float
        Thickness of the shell in units nm.
        Might be zero.
    Rdrop : float
        Radius of small drops or discs decorating the shell in units nm.
    Ndrop : int
        Number of drops on shell.
    Hdrop : float
        Center of mass position of drops relative to Rcore+shellthickness. Not used for discs.
    coreSLD,shellSLD,dropSLD : float
        Scattering length of core, shell or drops in unit nm^-2.
    solventSLD : float
        Solvent scattering length density in unit nm^-2.
    typ : 'drop','cutdrop','disc'
        Type of the drops
         - 'drop' extending to inside, drop volume has SLD dropSLD
         - 'cutdrop' the drop is cut at the outer shell and the shell has always shellSLD.
         - 'disc' a disc is cut from the shell and has dropSLD.
    distribution : 'fibonacci','quasirandom'
        Distribution of drops as :
         - 'fibonacci' A Fibonacci lattice on the sphere with Ndrop points.
                       For even Ndrop the point [0,0,1] is removed
         - 'quasirandom' quasirandom distribution of Ndrop drops on sphere surface.
                         The distribution is always the same if repeated several times.
    ndrop : int
        Number of points in grid on length Rdrop. Determines resolution of the droplets.
        Large ndrop increase the calculation time by ndrop**3.
        To small give wrong scattering length contributions in shell and core.
    relError : float
        Determines calculation method.
        See :py:func:`~.formfactor.cloudScattering`
    show : bool
        Show a 3D image using matplotlib.

    Returns
    -------
    dataArray :
        Columns [q, Fq, Fq coreshell]
         - attributes from call
         - .dropSurfaceFraction :math:`=N_{drop}R_{drop}^2/(4(R_{core} + shellthickness + H_{drop})^2)`


    Notes
    -----
    The models uses cloudscattering with multi component particle distribution.
     - At the center is a multiShellSphere with core and shell located.
     - At the positions of droplets/disc a grid of small particles describe the respective shape as disc or drop.
     - According to the 'typ' each particle gets a respective scattering length to
       result in the correct scattering length density including the overlap with the central core-shell particle.
     - cloudscattering is used to calculate the respective scattering including all cross terms.
     - If drops overlap the overlap volume is only counted once.
       For large Ndrop the drop layer might be full, check *.dropSurfaceFraction*. In this case the disc represents
       the shell, while the drops represent still some surface roughness.
       The Rdrop is explicitly not limited to allow this.


    As described in cloudscattering for high q a bragg peak will appear showing the particle bragg peaks.
    This is far outside the respective SAS scattering. The validity of this model is comparable to
    :ref:`A nano cube build of different lattices`.
    For higher q the ndrop resolution parameter needs to be increased.


    Examples
    --------
    Comparing the models with arbitrary values. ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     drop = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=1, shellthickness=1, shellSLD=2,dropSLD=5,show=0,typ='drop')
     cutdrop = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=1, shellthickness=1, shellSLD=2,dropSLD=5,show=0,typ='cutdrop')
     disc = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=1, shellthickness=1, shellSLD=2,dropSLD=5,show=0,typ='disc')
     p=js.grace()
     p.plot(drop,li=1,le='drop')
     p.plot(disc,li=1,le='disc')
     p.plot(cutdrop,li=1,le='cutdrop')
     p.plot(drop.X,drop._cs_fq,li=1,sy=0,le='coreshell')
     p.yaxis(scale='l',min=1e4,max=1e10)
     p.xaxis(scale='l')
     p.legend(x=0.02,y=1e6)


    Comparing the coreshell with the drop decorated version
    ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     drop = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=0, shellthickness=1, shellSLD=2,dropSLD=0.5,show=0,typ='drop')
     fig = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=0, shellthickness=1, shellSLD=2,dropSLD=0.5,show=1,typ='drop')
     bb=fig.axes[0].get_position()
     fig.axes[0].set_title('raspberry: drops on core shell')
     fig.axes[0].set_position(bb.shrunk(0.5,0.9))
     ax1=fig.add_axes([0.58,0.1,0.4,0.85])
     ax1.plot(drop.X,drop.Y, label='coreshell with drops')
     ax1.plot(drop.X,drop._cs_fq,linestyle='--', label='core shell')
     ax1.set_yscale('log')
     ax1.set_xscale('log')
     ax1.legend()
     fig.set_size_inches(8,4)
     #fig.savefig(js.examples.imagepath+'/raspberry.jpg')

    .. image:: ../../examples/images/raspberry.jpg
     :width: 70 %
     :align: center
     :alt: cuboid


    Comparing the coreshell with the disc decorated version
    ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     drop = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=0, shellthickness=1, shellSLD=2,dropSLD=0.5,show=0,typ='disc')
     fig = js.ff.decoratedCoreShell(q=q,Rcore=20, Rdrop=4, Ndrop=20, Hdrop=0,
                     coreSLD=0, shellthickness=1, shellSLD=2,dropSLD=0.5,show=1,typ='disc')
     bb=fig.axes[0].get_position()
     fig.axes[0].set_title('liposome with patches')
     fig.axes[0].set_position(bb.shrunk(0.5,0.9))
     ax1=fig.add_axes([0.58,0.1,0.4,0.85])
     ax1.plot(drop.X,drop.Y, label='liposome with patches')
     ax1.plot(drop.X,drop._cs_fq,'--', label='core shell')
     ax1.set_yscale('log')
     ax1.set_xscale('log')
     ax1.legend()
     fig.set_size_inches(8,4)
     #fig.savefig(js.examples.imagepath+'/coreshellwithdisc.jpg')

    .. image:: ../../examples/images/coreshellwithdisc.jpg
     :width: 70 %
     :align: center
     :alt: cuboid


    """
    # use contrasts
    coreSLD -= solventSLD
    if shellSLD is None:
        shellSLD = 0
    else:
        shellSLD -= solventSLD
    if dropSLD is None:
        dropSLD = 0
    else:
        dropSLD -= solventSLD

    if shellthickness is None: shellthickness = 0

    # fa of coreshell and particles
    # this might be extended to complicated multishellSpheres using multiShellSphere
    if shellthickness == 0 or shellSLD == 0:
        fa = sphere(q, Rcore, coreSLD)[[0, 2]]
    elif Rcore == 0:
        fa = sphere(q, shellthickness, shellSLD)[[0, 2]]
    else:
        fa = multiShellSphere(q, [Rcore, shellthickness], [coreSLD, shellSLD], solventSLD=0)[[0, 2]]
    fa = fa.addColumn(1, 1)  # constant fa for points

    # a hcp grid for the droplets
    dnn = Rdrop / ndrop  # resolution for droplets
    size = (Rcore + shellthickness + Hdrop + Rdrop * 2) / dnn  # overall size
    grid = sf.hcpLattice(ab=dnn, size=size)
    grid.set_b(0)  # set all b to zero

    # center of mass of droplets
    if distribution[0] == 'f':
        NN = int(Ndrop / 2)
        points = formel.fibonacciLatticePointsOnSphere(NN=NN, r=Rcore + shellthickness + Hdrop)
        if points.shape[0] > Ndrop:
            points = np.delete(points, int(NN / 2), 0)
        pointsxyz = formel.rphitheta2xyz(points)
    elif distribution[0] == 'q':
        points = formel.randomPointsOnSphere(NN=int(Ndrop), r=Rcore + shellthickness + Hdrop)
        pointsxyz = formel.rphitheta2xyz(points)

    # generate droplet grids
    V = grid.unitCellVolume
    if typ == 'drop':
        # all drop volume has SDL of drop
        for point in pointsxyz:
            grid.inSphere(Rdrop, center=point, b=dropSLD * V)
        grid.prune(grid._points[:, 3] > 0)  # prune all except spheres
        # correct overlap not to count it twice in core and shell
        grid.inSphere(Rcore + shellthickness, b=(dropSLD - shellSLD) * V)
        grid.inSphere(Rcore, b=(dropSLD - coreSLD) * V)
        grid.prune(grid._points[:, 3] > 0)  # prune all except spheres
    elif typ == 'cutdrop':
        # the drop is just an extension of core and shell to the outside
        for point in pointsxyz:
            grid.inSphere(Rdrop, center=point, b=1)
        grid.prune(grid._points[:, 3] > 0)  # prune all except spheres
        # set b to zero
        grid.inSphere(Rcore + shellthickness, b=0)
        # grid.inSphere(Rcore, b=0)
        grid.prune(grid._points[:, 3] > 0)  # prune all except spheres
        grid.set_b(dropSLD * V)
    elif typ == 'disc':
        # disc cuts in shell
        for point in pointsxyz:
            grid.inCylinder(v=point, R=Rdrop, a=[0, 0, 0], length=np.Inf, b=1)
        grid.prune(grid._points[:, 3] > 0)  # prune all except cylinders/cone
        grid.inSphere(Rcore + shellthickness, b=0, invert=True)
        grid.inSphere(Rcore, b=0, invert=False)
        grid.prune(grid._points[:, 3] > 0)
        grid.set_b((dropSLD - shellSLD) * V)
    if show:
        fig = grid.show()
        # add two transparent spheres
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        # Plot the surface
        fig.axes[0].plot_surface(x * Rcore, y * Rcore, z * Rcore,
                                 color='red', alpha=0.8)
        fig.axes[0].plot_surface(x * (Rcore + shellthickness), y * (Rcore + shellthickness),
                                 z * (Rcore + shellthickness),
                                 color='grey', alpha=0.2)
        return fig

    # complete the grid adding coreshell formfactor at center with respective scattering amplitude
    points = np.vstack([np.c_[grid.array, np.ones(grid.numberOfAtoms()) * 2], [0, 0, 0, fa.fa0, 1]])
    res = cloudScattering(q, points, relError=relError, formfactoramp=fa, ncpu=0)
    result = res.addColumn(1, fa[1]**2)
    result[1] = result[1] * result.I0
    result.columnname += '; cs_fq'
    result.setColumnIndex(iey=None)
    result.modelname = inspect.currentframe().f_code.co_name
    del result.rms
    del result.ffpolydispersity
    result.Rcore = Rcore
    result.Ndrops = Ndrop
    result.Rdrop = Rdrop
    result.Hdrop = Hdrop
    result.coreSLD = coreSLD
    result.shellthickness = shellthickness
    result.shellSLD = shellSLD
    result.dropSLD = dropSLD
    result.solventSLD = solventSLD
    result.dropSurfaceFraction = Ndrop * Rdrop ** 2 / (4 * (Rcore + shellthickness + Hdrop) ** 2)
    result.typ = typ
    result.distribution = distribution

    return result


def inhomogeneousSphere(q, Rcore, Rdrop, Ddrops, coreSLD, dropSLD=None, solventSLD=0, rms=0,
                        typ='drop', distribution='quasirandom', relError=100, show=False, **kwargs):
    r"""
    Scattering of a core shell sphere filled with droplets of different types.

    The model described spherical particle filled with particles as drops or coils.
    Drops are added in the internal volume extending outside if radius is large enough.

    The model uses cloudscattering and the source can be used as a template for more specific models.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    Rcore : float
        Core radius in nm.
    Rdrop : float
        Radius of small drops in units nm.
    Ddrops : int
        Average distance between drops in nm.
    shellthickness : float
        Optional a shellthickness (units nm) to add an outer shell around the core with scattering length shellSLD.
    coreSLD,dropSLD,shellSLD: float
        Scattering length of core and drops (optional shell) in unit nm^-2.
    solventSLD : float
        Solvent scattering length density in unit nm^-2.
    typ : string = ('drop', 'coil', 'gauss') + 'core' or/and 'shell'
        Type of the drops and were to place them. See cloudscattering for types. If the string contains 'core', 'shell'
        the drops are placed in one or both of core and shell.
         - 'drop' sphere with dropSLD
         - 'coil' gaussian coils. Coil scattering length is :math:`F_a(q=0) = dropSLD*4/3pi Rdrop**3`
                  with formfactor amplitude of Gaussian chain.
         - 'gauss' Gaussian function :math:`b_i(q)=b V exp(-\pi V^{2/3}q^2)` with :math:`V = 4\pi/3 R_{drop}^3` .
                  According to [1]_ the atomic scattering amplitude can be represented by gaussians
                  with the volume representing the displaced volume (e.g using the Van der Waals radius)
    distribution : 'random','quasirandom','fcc'
        Distribution of drops as :
         - 'random' random points. Difficult for fits as the configuration changes with each call.
         - 'quasirandom' quasirandom distribution of drops in sphere.
                         The distribution is always the same if repeated several times.
                         quasirandom is a bit more homogeneous than random with less overlap of drops.
         - 'fcc' a fcc lattice
    rms : float, default=0
        Root mean square displacement :math:`\langle u^2\rangle ^{0.5}` of the positions in cloud as
        random (Gaussian) displacements in nm.
        Displacement u is random for each orientation in sphere scattering.
    relError : float
        Determines calculation method.
        See :py:func:`~.formfactor.cloudScattering`
    show : bool
        Show a 3D image using matplotlib.

    Returns
    -------
    dataArray :
        Columns [q, Fq, Fq coreshell]
         - attributes from call
         - .Ndrop number of drops in sphere
         - .dropVolumeFraction :math:`=N_{drop}R_{drop}^3/R_{core}^3`

    Notes
    -----
    The models uses cloudscattering with multi component particle distribution.
     - At the center is a large sphere located.
     - At the positions of droplets inside of the large sphere additional small spheres
       or gaussian coils are positioned.
     - cloudscattering is used to calculate the respective scattering including all cross terms.
     - If drops overlap the overlap volume is counted double assuming an area of higher density.
       Drop volume can extend to the outside of the large sphere.
       The Rdrop is explicitly not limited to allow this.

    Examples
    --------
    Comparing sphere and filled sphere.
    The inhomogeneous filling filled up the characteristic sphere minima.
    Gaussian coil filling also removes the high q minima from small filling spheres.
    ::

     import jscatter as js
     q=js.loglist(0.03,5,300)
     fig = js.ff.inhomogeneousSphere(q=q,Rcore=20, Rdrop=5, Ddrops=11, coreSLD=0.001, dropSLD=2.5,show=1)
     bb=fig.axes[0].get_position()
     fig.axes[0].set_title('inhomogeneous filled sphere \nwith volume fraction 0.4')
     fig.axes[0].set_position(bb.shrunk(0.5,0.9))
     ax1=fig.add_axes([0.58,0.1,0.4,0.85])
     R=2;D=2*R*1.1
     drop = js.ff.inhomogeneousSphere(q=q,Rcore=20, Rdrop=R, Ddrops=D, coreSLD=0.1, dropSLD=1.5)
     ax1.plot(drop.X,drop.Y, label='sphere with drops')
     ax1.plot(drop.X,drop._sphere_fq,'--', label='sphere homogeneous')
     drop1 = js.ff.inhomogeneousSphere(q=q,Rcore=20, Rdrop=R, Ddrops=D, rms=0.6, coreSLD=0.1, dropSLD=1.5)
     ax1.plot(drop1.X,drop1.Y, label='sphere with drops rms=0.6')
     drop2 = js.ff.inhomogeneousSphere(q=q,Rcore=20, Rdrop=R, Ddrops=D, rms=4, coreSLD=0.1, dropSLD=1.5)
     ax1.plot(drop2.X,drop2.Y, label='sphere with drops rms=4')
     drop3 = js.ff.inhomogeneousSphere(q=q,Rcore=20, Rdrop=R, Ddrops=D, rms=4, coreSLD=0.1, dropSLD=1.5, typ='coil')
     ax1.plot(drop3.X,drop3.Y, label='sphere with polymer coil drops rms=4')
     ax1.set_yscale('log')
     ax1.set_xscale('log')
     ax1.legend()
     fig.set_size_inches(8,4)
     #fig.savefig(js.examples.imagepath+'/filledSphere.jpg')

    .. image:: ../../examples/images/filledSphere.jpg
     :width: 70 %
     :align: center
     :alt: filledSphere

    References
    ----------
    .. [1] An improved method for calculating the contribution of solvent to
           the X-ray diffraction pattern of biological molecules
           Fraser R MacRae T Suzuki E IUCr Journal of Applied Crystallography 1978 vol: 11 (6) pp: 693-694

    """
    # use contrasts
    coreSLD -= solventSLD
    dropSLD -= solventSLD
    shellthickness = kwargs.pop('shellthickness', 0)
    shellSLD = kwargs.pop('shellSLD', 0)
    shellSLD -= solventSLD

    # fa of different sized spheres (norm is taken in cloudscattering)
    if shellthickness > 0 and shellSLD != 0:
        fa = sphereCoreShell(q, Rc=Rcore, Rs=Rcore + shellthickness, bc=coreSLD,
                             bs=shellSLD, solventSLD=solventSLD)[[0, 2]]
    else:
        fa = sphere(q, Rcore, coreSLD)[[0, 2]]

    # drop volume
    V = 4 / 3 * np.pi * Rdrop ** 3
    # drop formfactor amplitudes
    if 'coil' in typ:
        fa = fa.addColumn(1, _fa_coil(q*Rdrop))
    elif 'gauss' in typ:
        fa = fa.addColumn(1, np.exp(-q ** 2 * V ** (2 / 3.) * np.pi))
    else:
        # default sphere
        fa = fa.addColumn(1, _fa_sphere(q* Rdrop))

    # determine inner and outer radii for drop location

    if 'shell' in typ and 'core' in typ and shellthickness>0:
        Ri=0
        Ro=Rcore + shellthickness
    elif 'shell' in typ and 'core' not in typ and shellthickness>0:
        Ri=Rcore
        Ro=Rcore + shellthickness
    elif 'shell' not in typ and 'core' in typ and shellthickness>0:
        Ri = 0
        Ro = Rcore
    else:
        # only in core
        Ri = 0
        Ro = Rcore
        typ = typ + 'core'

    # a grid for the droplets
    if distribution[:1] == 'fcc'[:1]:
        size = Ro / Ddrops * 1.2
        grid = sf.fccLattice(abc=Ddrops * 2 ** 0.5, size=size, b=0)
        grid.inSphere(Ro, center=[0, 0, 0], b=1)
        if Ri>0:
            grid.inSphere(Ri, center=[0, 0, 0], b=0)
    elif distribution[:1] == 'random'[:1]:
        nOP = int((2 * Ro) ** 3 / Ddrops ** 3)
        grid = sf.randomLattice(size=[Ro * 2, Ro * 2, Ro * 2], numberOfPoints=nOP, b=0, seed=137)
        grid.move([-Ro, -Ro, -Ro])
        grid.inSphere(Ro, center=[0, 0, 0], b=1)
        if Ri>0:
            grid.inSphere(Ri, center=[0, 0, 0], b=0)
    else:
        nOP = int((2 * Ro) ** 3 / Ddrops ** 3)
        grid = sf.pseudoRandomLattice(size=[Ro * 2, Ro * 2, Ro * 2], numberOfPoints=nOP, b=0, seed=137)
        grid.move([-Ro, -Ro, -Ro])
        grid.inSphere(Ro, center=[0, 0, 0], b=1)
        if Ri>0:
            grid.inSphere(Ri, center=[0, 0, 0], b=0)
    grid.prune(~np.isclose(grid._points[:, 3], 0))  # prune all except spheres
    # set drop SLD according to position
    if shellthickness > 0:
        grid.set_b((dropSLD - shellSLD) * V)  # set all
    grid.inSphere(Rcore, center=[0, 0, 0], b=(dropSLD - coreSLD) * V)  # set core

    if show:
        fig = grid.show()
        # add transparent spheres
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        # Plot the sphere surface
        fig.axes[0].plot_surface(x * Rcore,
                                 y * Rcore,
                                 z * Rcore, color='grey', alpha=0.2)
        if shellthickness > 0 and shellSLD != 0:
            fig.axes[0].plot_surface(x * (Rcore + shellthickness),
                                     y * (Rcore + shellthickness),
                                     z * (Rcore + shellthickness), color='grey', alpha=0.1)
        return fig

    # complete the grid adding coreshell formfactor at center with respective scattering amplitude
    points = np.vstack([np.c_[grid.array, np.ones(grid.numberOfAtoms()) * 2], [0, 0, 0, fa.fa0, 1]])
    res = cloudScattering(q, points, relError=relError, formfactoramp=fa, rms=rms, ncpu=0)
    result = res.addColumn(1, fa[1]**2)
    result[1] = result[1] * result.I0
    result.columnname += '; sphere_fq'
    result.setColumnIndex(iey=None)
    result.modelname = inspect.currentframe().f_code.co_name
    del result.rms
    del result.ffpolydispersity
    result.Rcore = Rcore
    result.Ndrops = grid.numberOfAtoms()
    result.Rdrop = Rdrop
    result.coreSLD = coreSLD + solventSLD
    result.dropSLD = dropSLD + solventSLD
    result.solventSLD = solventSLD
    result.shellSLD = shellSLD + solventSLD
    result.shellthickness = shellthickness
    result.dropVolumeFraction = result.Ndrops * Rdrop ** 3 / Rcore ** 3
    result.typ = typ
    result.distribution = distribution

    return result


def _makeDropsInCylinder(Rcore, L, Rdrop, Ddrops, h, dropSLD, coreSLD,  distribution):
    # a grid for the droplets inside of cylinder with caps for h!=None
    # assume cylinder axis along Z axis center in origin
    V = 4 / 3 * np.pi * Rdrop ** 3
    if h is not None:
        rcap=(Rcore**2+h**2)**0.5
    else:
        rcap=0 # no cap
    rmax = max(rcap, Rcore)
    # generate large enough drop grid
    if distribution[:1] == 'fcc'[:1]:
        sizeL = (2*(rmax)+L/2) / Ddrops * 2
        sizeR = rmax / Ddrops * 2
        grid = sf.fccLattice(abc=Ddrops * 2 ** 0.5, size=[sizeR, sizeR, sizeL], b=0)
        distribution = 'fcc'
    elif distribution[:1] == 'random'[:1]:
        nOP = int((L+4*rmax)*2*rmax*2*rmax / Ddrops ** 3)
        grid = sf.randomLattice(size=[rmax * 2, rmax * 2, (L+4*rmax)], numberOfPoints=nOP, b=0, seed=137)
        grid.move([-rmax, -rmax, -(L/2+2*rmax)])
        distribution = 'random'
    else:
        nOP = int((L+4*rmax)*2*rmax*2*rmax / Ddrops ** 3)
        grid = sf.pseudoRandomLattice(size=[rmax * 2, rmax * 2, (L+4*rmax)], numberOfPoints=nOP, b=0, seed=137)
        grid.move([-rmax, -rmax, -(L/2+2*rmax)])
        distribution = 'quasirandom'
    # generate drop grid inside of cylinder+caps
    grid.planeSide([0, 0, 1], [0, 0, L/2], 1)
    p1=grid.ball!=0
    grid.set_b(0)
    grid.incylinder(a=[0, 0, -L/2], v=[0, 0, 1], R=Rcore, length=np.Inf)
    cy=grid.ball!=0
    grid.set_b(0)
    if h is not None:
        grid.inSphere(rcap, center=[0, 0, L/2+h], b=1)
        s1=grid.ball!=0
        grid.set_b(0)
        grid.inSphere(rcap, center=[0, 0, -(L/2+h)], b=1)
        s2=grid.ball!=0
        grid.set_b(0)
        grid.planeSide([0, 0, -1], [0, 0, -L/2], 1)
        p2=grid.ball!=0
        grid.set_b(0)
        grid.set_bsel((dropSLD - coreSLD) * V, (s1 & p1) | (s2 &p2) |(cy & ~p1))
    else:
        grid.set_bsel((dropSLD - coreSLD) * V, (cy & ~p1))
    # prune grid
    grid.prune(~np.isclose(grid._points[:, 3], 0))
    return grid


def _fq_inhomCyl(Q, radii, L, angle, h, dSLDs, fa, rms, Rcore, Rdrop, Ddrops, dropSLD, coreSLD,  distribution,
                 ncap=31, nconf=37):
    # formfactoramp cylinder+cap
    fac = _fa_capedcylinder(Q, radii, L, angle, h, dSLDs, ncap)
    if distribution[:1] == 'fcc'[:1]:
        # create grid of drops inside of core
        grid = _makeDropsInCylinder(Rcore, L, Rdrop, Ddrops, h, dropSLD, coreSLD,  distribution)
        # average drop scattering amplitude [2]
        iff = np.ones(grid.b.shape[0], dtype=int)
        # points on unit sphere with angle to average (for some speedup)
        qrpt = np.c_[np.ones(nconf), 0:2 * np.pi:2 * np.pi / nconf, np.ones(nconf) * angle]
        # drops return [q,fq,fa]
        fadrops = fscatter.cloud.average_ffqrpt(Q, r=grid.XYZ, blength=grid.b, iff=iff, formfactor=fa,
                                                rms=rms, ffpolydispersity=0, points=qrpt)[:, 2]
        return (fadrops + fac) ** 2, fac ** 2, fadrops ** 2
    else:
        # average over some independent grids
        # points on unit sphere with angle to average (for some speedup)
        nphi = 5
        qrpt = np.c_[np.ones(nphi), 0:2 * np.pi:2 * np.pi / nphi, np.ones(nphi) * angle]
        fadrops = []
        for i in np.r_[:nconf]:
            grid = _makeDropsInCylinder(Rcore, L, Rdrop, Ddrops, h, dropSLD, coreSLD,  distribution)
            iff = np.ones(grid.b.shape[0], dtype=int)
            # drops return [q,fq,fa]
            fadrops.append(fscatter.cloud.average_ffqrpt(Q, r=grid.XYZ, blength=grid.b, iff=iff, formfactor=fa,
                                                    rms=rms, ffpolydispersity=0, points=qrpt)[:, 2])
        fadrops = np.mean(fadrops, axis=0)
        return (fadrops + fac) ** 2, fac ** 2, fadrops ** 2


def inhomogeneousCylinder(q, Rcore, L, Rdrop, Ddrops, coreSLD, dropSLD=None, solventSLD=0, rms=0,
                        typ='drop', distribution='quasirandom', h=0, nconf=34, show=False, **kwargs):
    r"""
    Scattering of a caped cylinder filled with droplets.

    The model described caped cylinder particle filled with drops.
    Drops are added only in the core volume (drop center < Rcore) extending outside if radius is large enough.

    The model uses cloudscattering and the source can be used as a template for more specific models.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    Rcore : float
        Core radius in nm.
    L : float
        Cylinder length in units nm.
    Rdrop : float
        Radius of small drops in units nm.
    Ddrops : int
        Average distance between drops in nm.
    h : float, default=None
        Geometry of the caps with cap radii :math:`R_i=(r_i^2+h^2)^{0.5}`. See multiShellCylinder.
        h is distance of cap center with radius R from the flat cylinder cap and r as radii of the cylinder shells.

        - None: No caps, flat ends as default.
        - 0: cap radii equal cylinder radii (same shellthickness as cylinder shells)
        - >0: cap radius larger cylinder radii as barbell
        - <0: cap radius smaller cylinder radii as lens caps
    shellthickness : float
        Optional a shellthickness (units nm) to add an outer shell around the core with scattering length shellSLD.
    coreSLD,dropSLD,shellSLD: float
        Scattering length of core and drops (optional shell) in unit 1/nm².
    solventSLD : float
        Solvent scattering length density in unit 1/nm².
    typ : 'gauss', 'coil', default='drop'
        Type of the drops
         - 'drop'  sphere with dropSLD. Drop scattering length is dropSLD*4/3pi Rdrop**3 .
         - 'coil'  polymer coils. Coil scattering length is dropSLD*4/3pi Rdrop**3 .
         - 'gauss' Gaussian function :math:`b_i(q)=b V exp(-\pi V^{2/3}q^2)` with :math:`V = 4\pi/3 R_{drop}^3` .
                   According to [1]_ the atomic scattering amplitude can be represented by gaussians
                   with the volume representing the displaced volume (e.g using the Van der Waals radius)
    distribution : 'random','fcc', default='quasirandom'
        Distribution of drops as :
         - 'random' random points. difficult for fitting as the configuration chnages for each call.
         - 'quasirandom' quasirandom distribution of drops in sphere.
                         The distribution is always the same if repeated several times.
                         quasirandom is a bit more homogeneous than random with less overlap of drops.
         - 'fcc' a fcc lattice.
    rms : float, default=0
        Root mean square displacement :math:`\langleu^2\rangle^{0.5} of the positions in cloud as
        random (Gaussian) displacements in nm.
        Displacement u is random for each orientation in sphere scattering.
    nconf : int, default=34
        Determines how many configurations are averaged.
        For 'fcc' it determines the number of angular orientations, a lower number is already sufficient.
        For others it is the number of independent configurations, each averaged over 5 angular orientations.
    show : bool
        Show a 3D image of a configuration using matplotlib.
        This returns a figure handle.

    Returns
    -------
    dataArray :
        Columns [q; fq; fq_cyl; fq_drops']
         - attributes from call
         - .Ndrop number of drops in caped cylinder
         - .dropVolumeFraction :math:`=N_{drop}V_{drop}/V_{caped cylinder}`

    Notes
    -----
     - The scattering amplitude :math:`F_{a,cyl}(q,\alpha)` of a caped cylinder is calculated
       (see multiShellCylinder for a reference).
     - At the positions of drops inside of the caped cylinder core additional drops are positioned
       with respective scattering amplitudes :math:`F_{a,drop}(q)` according to *typ*.
     - Positions are distributed as 'fcc', 'random' or 'quasirandom'.
     - The combined scattering amplitude is
       :math:`F_a(q,\alpha) =  F_{a,cyl}(q,\alpha) + \sum_i e^{iqr_i}F_{a,drop}`
       and
       :math:`F(q) = \int F_a(q,\alpha)F^*_a(q,\alpha) d\alpha`
     - If drops overlap the overlap volume is counted double assuming an area of higher density.
       Drop volume can extend to the outside of the large sphere.
       Rdrop is explicitly not limited to allow this.

    Examples
    --------
    Comparing sphere and filled sphere.
    The inhomogeneous filling filled up the characteristic sphere minima.
    Gaussian coil filling also removes the high q minima from small filling spheres.
    ::

     import jscatter as js
     q=js.loglist(0.01,5,300)
     drop=-1
     fig = js.ff.inhomogeneousCylinder(q=q,Rcore=10,L=50, Rdrop=2.4,h=0, Ddrops=6,coreSLD=1,dropSLD=drop,show=1,typ='coil',distribution='fcc')
     bb=fig.axes[0].get_position()
     fig.axes[0].set_title('inhomogeneous filled cylinder \nwith volume fraction 0.53')
     fig.axes[0].set_position(bb.shrunk(0.5,0.9))
     ax1=fig.add_axes([0.58,0.1,0.4,0.85])
     ihC= js.ff.inhomogeneousCylinder(q=q,Rcore=10,L=50, Rdrop=2.4,h=0, Ddrops=6,coreSLD=1,dropSLD=drop,show=0,typ='coil',distribution='fcc')
     ax1.plot(ihC.X,ihC.Y,label='doped cylinder')
     ax1.plot(ihC.X,ihC._fq_cyl,label='homogeneous cylinder')
     ax1.plot(ihC.X,ihC._fq_drops,label='only drops')
     ax1.set_yscale('log')
     ax1.set_xscale('log')
     ax1.legend()
     fig.set_size_inches(8,4)
     #fig.savefig(js.examples.imagepath+'/filledCylinder.jpg')

    .. image:: ../../examples/images/filledCylinder.jpg
     :width: 70 %
     :align: center
     :alt: filledSphere

    """
    nalpha = kwargs.pop('nalpha', 57)
    # use contrasts
    coreSLD -= solventSLD
    dropSLD -= solventSLD
    shellthickness = kwargs.pop('shellthickness', 0)
    shellSLD = kwargs.pop('shellSLD', 0)
    shellSLD -= solventSLD

    # prepare radii and dSLDs for shellcylinder
    if shellthickness > 0 and shellSLD != 0:
        radii=np.r_[Rcore, Rcore + shellthickness]
        dSLDs = np.r_[coreSLD, shellSLD]
    else:
        radii=np.r_[Rcore]
        dSLDs = np.r_[coreSLD]

    # define drops fa
    if 'coil' in typ:
        fa = np.c_[q, _fa_coil(q*Rdrop)].T
    elif 'gauss' in typ:
        V = 4*np.pi/3 * Rdrop**3
        fa = np.c_[q, np.exp(-q ** 2 * V ** (2 / 3.) * np.pi)].T
    else:
        # default sphere
        fa = np.c_[q, _fa_sphere(q*Rdrop)].T
        typ='drop'

    if h is not None:
        rcap = (Rcore ** 2 + h ** 2) ** 0.5
    else:
        rcap = 0  # no cap

    # on for later usage
    grid = _makeDropsInCylinder(Rcore, L, Rdrop, Ddrops, h, dropSLD, coreSLD, distribution)
    if show:
        # make grid and show it with drops
        fig = grid.show()
        # add transparent cylinder and cap
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        z1 = np.linspace(-L / 2, L / 2, 100)
        uc, zc = np.meshgrid(u, z1)
        xc = np.cos(uc)
        yc = np.sin(uc)
        # plot cylinder
        fig.axes[0].plot_surface(xc * Rcore,
                                 yc * Rcore,
                                 zc , color='grey', alpha=0.2)
        if h is not None:
            # Plot the sphere surface
            fig.axes[0].plot_surface(x * rcap,
                                     y * rcap,
                                     z * rcap+L/2+h, color='grey', alpha=0.2)
            fig.axes[0].plot_surface(x * rcap,
                                     y * rcap,
                                     z * rcap-L/2-h, color='grey', alpha=0.2)

        if shellthickness > 0 and shellSLD != 0:
            fig.axes[0].plot_surface(x * (Rcore + shellthickness),
                                     y * (Rcore + shellthickness),
                                     z * (Rcore + shellthickness)+L/2+h, color='grey', alpha=0.1)
            fig.axes[0].plot_surface(x * (Rcore + shellthickness),
                                     y * (Rcore + shellthickness),
                                     z * (Rcore + shellthickness)-L/2-h, color='grey', alpha=0.1)
        return fig

    # sin(alpha) weight for volume integration
    a = np.r_[0:np.pi / 2:90j]
    w = np.c_[a, np.sin(a)].T
    # Gauss integration over angle alpha with weight = sin(a)*da
    Sq = formel.parQuadratureFixedGauss(_fq_inhomCyl, 0, np.pi / 2., 'angle', weights=w, n=nalpha, ncpu=0,
                                Q=q, radii=radii, L=L, h=h, dSLDs=dSLDs, fa=fa, rms=rms,
                                Rcore=Rcore, Rdrop=Rdrop, Ddrops=Ddrops, dropSLD=dropSLD, coreSLD=coreSLD,
                                distribution=distribution, nconf=nconf)

    result = dA(np.c_[q, Sq].T)
    result.columnname = 'q; fq; fq_cyl; fq_drops'
    result.setColumnIndex(iey=None)
    result.modelname = inspect.currentframe().f_code.co_name
    result.Rcore = Rcore
    result.L = L
    result.coreVolume = np.pi*Rcore**2*L
    if h is not None:
        # add cap volume
        result.coreVolume += 2* np.pi*h**2/3*(3*rcap-h)
    result.shellthickness = shellthickness
    result.Ndrops = grid.numberOfAtoms()
    result.Rdrop = Rdrop
    result.coreSLD = coreSLD + solventSLD
    result.dropSLD = dropSLD + solventSLD
    result.solventSLD = solventSLD
    result.shellSLD = shellSLD + solventSLD
    result.shellthickness = shellthickness
    result.dropVolumeFraction = result.Ndrops * 4/3*np.pi*Rdrop ** 3 / result.coreVolume
    result.typ = typ
    result.distribution = distribution

    return result


def _fq_prism(points, Q, R, H):
    """
    Equal sided prism width edge length R of height H

    The height is along Z-axis. The prism rectangular basis is parallel to XZ-plane,
    the triangular plane is parallel to XY-plane. See [1]_ SI *The form factor of a prism*.

    Parameters
    ----------
    points : 3xN array
        q directionn on unit sphere
    Q 1xM array
        Q values
    R : float
        2R is edge length
    H : float
        Prism height in Z direction

    Returns
    -------
        array

    References
    ----------
    .. [1] DNA-Nanoparticle Superlattices Formed From Anisotropic Building Blocks
          Jones et al
          Nature Materials 9, 913–917 (2010), doi: 10.1038/nmat2870

    """
    qx, qy, qz = points.T[:, :, None] * Q[None, None, :]
    sq3 = np.sqrt(3)
    fa_prism = 2*sq3*np.exp(-1j*qy*R/sq3)*H / (qx*(qx**2-3*qy**2)) * \
    (qx*np.exp(1j*qy*R*sq3) - qx*np.cos(qx*R) - 1j*sq3*qy*np.sin(qx*R)) * \
    np.sinc(qz*H/2)

    return np.real(fa_prism * np.conj(fa_prism))


def prism(q, R, H, SLD=1, solventSLD=0, relError=300):
    r"""
    Formfactor of prism (equilateral triangle) .

    Parameters
    ----------
    q : array 3xN
    R : float
        Edge length of equilateral triangle in units nm.
    H : float
        Height in units nm
    SLD : float, default =1
        Scattering length density unit nm^-2
        e.g. SiO2 = 4.186*1e-6 A^-2 = 4.186*1e-4 nm^-2 for neutrons
    solventSLD : float, default =0
        Scattering length density of solvent. unit nm^-2
        e.g. D2O = 6.335*1e-6 A^-2 = 6.335*1e-4 nm^-2 for neutrons
    relError : float, default 300
        Determines how points on sphere are selected for integration
         - >=1  Fibonacci Lattice with relError*2+1 points (min 15 points)
         - 0<1 Pseudo random points on sphere (see randomPointsOnSphere).
               Stops if relative improvement in mean is less than relError (uses steps of 20*ncpu new points).
               Final error is (stddev of N points) /sqrt(N) as for Monte Carlo methods.
               even if it is not a correct 1-sigma error in this case.

    Returns
    -------
    dataArray [q, fq]

    Notes
    -----
    With contrast :math:`\rho` and wavevector :math:`q=[q_x,q_y,q_z]` the scattering amplitude :math:`F_a(q)` is

    .. math:: F_a(q_x,q_y,q_z) = \rho \frac{2 \sqrt{3} e^{-iq_yR/ \sqrt{3}} H} {q_x (q_x^2-3q_y^2)} \
              (q_x e^{i q_yR\sqrt{3}} - q_xcos(q_xR) - i\sqrt{3} q_ysin(q_xR))  sinc(q_zH/2)

    and :math:`F(q)=<F_a(q)F^*_a(q)>=<|F_a(q)|^2>`

    Examples
    --------
    ::

     import jscatter as js
     q = js.loglist(0.1,5,100)
     p = js.grace()
     fq = js.ff.prism(q,3,3)
     p.plot(fq.X,fq.Y/fq.I0)
     p.yaxis(scale='log')

    References
    ----------
    .. [1] DNA-Nanoparticle Superlattices Formed From Anisotropic Building Blocks
          Jones et al
          Nature Materials 9, 913–917 (2010), doi: 10.1038/nmat2870

    """
    V = np.sqrt(3)*R*R*H
    sld = SLD - solventSLD
    I0 = V*V*sld*sld
    fq, err = formel.sphereAverage(function=_fq_prism, Q=q, R=R, H=H, passPoints=True, relError=relError).reshape(2, -1)

    result = dA(np.c_[q, sld**2 * fq].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.I0 = I0
    result.height = H
    result.edge = R
    result.volume = V
    result.contrast = sld
    return result


def ornsteinZernike(q, xi, I0=1):
    r"""
    Lorenz function, Ornstein Zernike model of critical systems.

    The models is also used to describe diffuse scattering.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm
    xi : float
        Correlation length
    I0 : float
        scale


    Returns
    -------
        dataArray [q, Iq]

    Notes
    -----
    A spatial correlation of the form

    .. math:: \rho(r)_{OZ}= \frac{\rho_0}{r}e^{-\frac{r}{\xi}}

    results in the scattering intensity

    .. math:: I(q) = \frac{I_0}{1+q^2\xi^2}

    A detailed explanation is found in [2]_.

    References
    ----------
    .. [1] Accidental deviations of density and opalescence at the critical point of a single substance.
           Ornstein, L., & Zernike, F. (1914).
           Proc. Akad. Sci.(Amsterdam), 17(September), 793–806.
           Retrieved from http://www.dwc.knaw.nl/DL/publications/PU00012727.pdf

    .. [2] Correlation functions and the critical region of simple fluids.
           Fisher, M. E. (1964).
           Journal of Mathematical Physics, 5(7), 944–962. https://doi.org/10.1063/1.1704197

    .. [3] Origin of the scattering peak in microemulsions
           Teubner, M.; Strey, R.
           Chem. Phys. 1987, 87 (5), 3195–3200 DOI: 10.1063/1.453006

    """
    result = dA(np.c_[q, I0/(1+q**2*xi**2)].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.xi = xi
    return result

def DAB(q, xi, I0=1):
    r"""
    DAB model for two-phase systems with sharp interface leading to Porod scattering at large q.

    Debye-Anderson-Brumberger (DAB) model or Debye–Buche function.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm
    xi : float
        Correlation length in units nm.
    I0 : float
        scale

    Returns
    -------
        dataArray [q, Iq]

    Notes
    -----

    .. math:: I(q) = \frac{I_0}{(1+q^2\xi^2)^2}

    From [3]_ about gels and inhomogenities and usage of DAB.
    DAB is used to describe the inhomogenities:

     "Inhomogeneities in polymer gels are more pronounced after swelling.
     Regions of greater cross-linking density swell considerably more than regions of lower cross-linking density.
     The difference grows with increased swelling, and the denser regions of higher cross-linking density can influence
     the scattering pattern. The static inhomogeneities are not exclusively due to a distribution of cross-links but
     could be topological in nature or due to the connectivity of the network.
     This effect was first illustrated by Bastide and Leibler. To account for both the and the spatial distribution
     of inhomogeneities, the gel structure function has been described as having two contributions, thermal fluctuations
     from gel strands and the static spatial distribution of inhomogeneities.
     The phenomenon was later expanded upon by Panyukov and Rabin for poly-electrolyte gels.
     The simplified version of the structure factor for an inhomogeneous network"
    With first term as DAB and second as OrnsteinZernike model:

    .. math:: I(q) = \frac{I_{0,DAB}}{(1+q^2\xi_{DAB}^2)^2} + \frac{I_{0,OZ}}{1+q^2\xi_{OZ}^2}


    References
    ----------
    .. [1] Scattering by an Inhomogeneous Solid. II. The Correlation Function and Its Application
           Debye, P., Anderson, R., Brumberger, H.,J. Appl. Phys. 28 (6), 679 (1957).

    .. [2] Scattering by an Inhomogeneous Solid
           Debye, P., Bueche, A. M., J. Appl. Phys. 20, 518 (1949)

    .. [3] Scattering methods for determining structure and dynamics of polymer gels
            Morozov et al., J. Appl. Phys.129, 071101 (2021);doi: 10.1063/5.003341


    """
    result = dA(np.c_[q, I0/(1+q**2*xi**2)**2].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.xi = xi
    return result


def polymerCorLength(q, xi, m, I0=1):
    r"""
    Polymer scattering switching from collapsed over theta solvent to good solvent including chain overlap.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm
    xi : float
        Correlation length
    m : float
        Porod exponent describing high q power law.
        m is related to Flory excluded volume exponent 𝜈 as m=1/𝜈
        m=2 is Lorentz function (Ornstein-Zernike critical system)
    I0 : float
        scale


    Returns
    -------
        dataArray [q, Iq]

    Notes
    -----
    According to [1]_ the polymer scattering in solution can be described by the correlation length xi using:

    .. math:: I(q) = \frac{I_0}{1+(q\xi)^m} \ with \ m=1/\nu

    - For collapsed chain  𝜈=1/3 ; m=3
    - For theta solvent  𝜈=1/2 ; m=2
    - For good solvent  𝜈=3/5 ; m=5/3

    For Rg one finds :math:`R_g^2 = \frac{b^2N^{2\nu}}{(2\nu+1)(2\nu+2)}`.
    For details see [1]_ and [2]_.


    References
    ----------
    .. [1] Insight Into Chain Dimensions in PEO/Water Solutions
           B. HAMMOUDA, D. L. Ho,
           Journal of Polymer Science, Part B: Polymer Physics, 45(16), 2196–2200. https://doi.org/10.1002/polb.21221
    .. [2] Insight into Clustering in Poly(ethylene oxide) Solutions
           B. Hammouda,* D. L. Ho, and S. Kline, Macromolecules 2004, 37, 6932-6937, doi: 10.1021/ma049623d

    """
    result = dA(np.c_[q, I0/(1+(q*xi)**m)].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Iq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.xi = xi
    return result



