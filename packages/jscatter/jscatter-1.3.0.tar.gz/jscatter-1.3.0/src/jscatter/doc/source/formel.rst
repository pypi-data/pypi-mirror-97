formel
======

.. automodule:: jscatter.formel
    :noindex:

Functions
---------
.. autosummary::
   loglist
   gauss
   lorentz
   voigt
   lognorm
   box
   Ea
   boseDistribution
   schulzDistribution

Quadrature
----------
.. autosummary::
   parQuadratureSimpson
   parQuadratureFixedGauss
   parQuadratureFixedGaussxD
   parQuadratureAdaptiveGauss
   parQuadratureAdaptiveClenshawCurtis
   parAdaptiveCubature
   sphereAverage
   psphereAverage
   convolve

Distribution of parameters
--------------------------
Experimental data might be influenced by multimodal parameters (like multiple sizes)
or by one or several parameters distributed around a mean value.

.. autosummary::
    parDistributedAverage
    multiParDistributedAverage
    scatteringFromSizeDistribution

Centrifugation
--------------
.. autosummary::
   sedimentationCoefficient
   sedimentationProfile
   sedimentationProfileFaxen                                                                                                                                     

NMR
---
.. autosummary::
   DrotfromT12
   T1overT2
   
Material Data
-------------
.. autosummary::   
   scatteringLengthDensityCalc
   waterdensity
   bufferviscosity
   dielectricConstant
   watercompressibility
   cstar
   molarity
   viscosity
   Dtrans
   Drot

other Stuff
-----------
.. autosummary::
   memoize
   xyz2rphitheta
   rphitheta2xyz
   rotationMatrix
   fibonacciLatticePointsOnSphere
   randomPointsOnSphere
   randomPointsInCube
   qEwaldSphere
   smooth
   imageHash

Constants and Tables
--------------------
.. autosummary::
    eijk
    felectron
    Elements

-----

.. automodule:: jscatter.formel
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: jscatter.formel.imageHash
    :members:
    :undoc-members:
    :show-inheritance:


   
   