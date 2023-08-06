**The aim of Jscatter is treatment of experimental data and models**:




* Reading and analyzing experimental data with associated attributes as temperature, wavevector, comment, ....
* Multidimensional fitting taking attributes into account.
* Providing useful models for **neutron and X-ray scattering** as form factors, structure factors
  and dynamic models (quasi elastic neutron scattering) and other topics.
* Simplified plotting with paper ready quality (preferred in xmgrace).
* Easy model building for non programmers.
* Python scripts to document data evaluation and modelling.

.. |citation| image:: https://img.shields.io/badge/DOI-10.1371%2Fjournal.pone.0218789-blue
            :target: https://doi.org/10.1371/journal.pone.0218789

.. |binder| image:: https://img.shields.io/badge/launch-jscatter-F5A252.svg?logo=data:image/png;base64,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
            :alt: link to mybinder
            :target: https://mybinder.org/v2/gl/biehl%2Fjscatter/master?filepath=src%2Fjscatter%2Fexamples%2Fnotebooks

.. |install| image:: https://img.shields.io/pypi/v/jscatter?labelColor=black?logoColor=blue   :alt: PyPI
    :target: https://pypi.org/project/jscatter/

.. |license| image:: https://img.shields.io/badge/license-GPLv3-orange
            :target: https://www.gnu.org/licenses/gpl-3.0.en.html

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/jscatter?color=orange   :alt: PyPI - Python Version
            :target: https://pypi.org/project/jscatter/

.. |docs| image:: https://img.shields.io/readthedocs/jscatter?color=orange
            :alt: Read the Docs
            :target: https://jscatter.readthedocs.io/en/latest/

.. |beginners| image:: https://img.shields.io/badge/Beginners-Guide-orange
            :alt: Beginners Guide
            :target: https://jscatter.readthedocs.io/en/latest/BeginnersGuide.html


|binder| |citation| |install| |license| |pyversion| |docs| |beginners|

.. image:: http://jscatter.readthedocs.io/en/latest/_images/Jscatter.jpeg
    :align: right
    :alt: Jscatter Logo


**Main concept**

- Link data from experiment, analytical model or simulation with attributes as .temperature, .wavevector, .pressure,...
- Methods for fitting, filter, merging,... using the attributes by name.
- Provide an extensible library with common theories/models for fitting of physical models.
- Allowing evaluation even of hundreds of datasets using scripts.

**1  Data organisation**

 Multiple measurements are stored in a *dataList* (subclass of list) of *dataArray*.
 dataArray is a subclass of **numpy** ndarray but with attributes and more.
 Full numpy ndarray functionality is preserved.
 Special attributes are .X,.Y, .eY...- for convenience and easy reading.
 Thus dataList represents e.g. a temperature series (as dataList) with measurements (dataArray) as list elements.

**2  Read/Write data**

 The intention is to read everything in the file to use it later and not ignore it as in numpy.loadtxt.
 Multiple measurement files can be read at once and then filtered according to attributes to get subsets.

 An ASCII file may consist of multiple sets of data with optional attributes or comments.
 Data are a matrix of values in a file. Attribute lines have a name in front.
 Everything else is a comment.

 Even complex ASCII files can be read with a few changes given as options.
 The ASCII file is still human readable and can be edited.
 Attributes can be generated from content of the comments (attributes which are text and not numbers).

**3  Fitting**

 Multidimensional attribute dependent fitting
 (least square Levenberg-Marquardt, differential evolution, .... from scipy.optimize).
 Attributes are used automatically as fixed fit parameters but can be overwritten.
 See dataList.fit for detailed description.

**4  Plotting**

 We use an adaption of xmgrace for 2D plots (a wrapper; see GracePlot) as it allows
 interactive publication ready output in high quality for 2D plots.
 The plot is stored as ASCII (.agr file) with original data and not as non-editable image as png or jpg.
 This allows a later change of the plot layout without recalculation, because data are stored as data and not as image.
 Imagine the boss/reviewer asking for a change of colors/symbol size.
 Nevertheless a small `matplotlib <https://matplotlib.org/>`_ interface is there and matplotlib can be used as it is (e.g. for 3D plots).

**5  Models**

 A set of models/theories is included see module e.g. formel, form factor and structure factor.
 User defined models can be used (e.g. as lambda function) just within a script or in interactive session of (i)python.
 By intention the user should write own models (to include e.g. a background, instrument resolution, ...) or to add different contributions.
 Contribution by new models is welcome. Please give a publication as reference as in the provided models.


 **some special functions**::

  formel.scatteringLengthDensityCalc -> electron density, coh and inc neutron scattering length, mass
  formel.sedimentationProfile        -> approximate solution to the Lamm equation of sedimenting particles
  formel.waterdensity                -> temperature dependent density of water (H2O/D2O) with inorganic substances
  structurefactor.RMSA               -> rescaled MSA structure factor for dilute charged colloidal dispersions
  structurefactor.hydrodynamicFunct  -> hydrodynamic function from hydrodynamic pair interaction
  formfactor.multiShellSphere        -> formfactor of multi shell spherical particles
  formfactor.multiShellCylinder      -> formfactor of multi shell cylinder particles
  formfactor.orientedCloudScattering -> 2D scattering of an oriented cloud of scatterers
  dynamic.finiteZimm                 -> Zimm model with internal friction -> intermediate scattering function
  dynamic.diffusionHarmonicPotential -> diffusion in harmonic potential-> intermediate scattering function
  sas.smear                          -> smearing enabling simultaneous fits of differently smeared SANS/SAXS data
  sas.desmear                        -> desmearing according to the Lake algorithm for the above
  sas.waterXrayScattering            -> absolute scattering of water with components (salt, buffer)

**6  Examples & Documentation**

 A number of examples how to use Jscatter is provided and can be run from Jscatter.
 Documentation located at `<http://jscatter.readthedocs.io>`_.
 The html documentation can be opened in browser (for dev versions) ::

  import jscatter as js
  js.showDoc()                     # open html documentation
  js.examples.showExampleList()    # show list of examples
  js.examples.runExample(1)        # run example by number of filename
  js.examples.showExample(1)       # show example source code


 A short example how to use Jscatter::


    import jscatter as js

    i5=js.dL(js.examples.datapath+'/iqt_1hho.dat')     # read the data (16 sets) with attributes
    # define a model for the fit
    diffusion=lambda A,D,t,wavevector,elastic=0:A*np.exp(-wavevector**2*D*t)+elastic

    # do the fit
    i5.fit(model=diffusion,                     # the fit function
           freepar={'D':[0.08],'A':0.98},       # start parameters, "[]" -> independent fit
           fixpar={'elastic':0.0},              # fixed parameters
           mapNames={'t':'X','wavevector':'q'}) # map names from the model to names from the data

    p=js.grace(1.2,0.8)                         # open a plot
    p.plot(i5,symbol=[-1,0.4,-1],legend='Q=$q') # plot with Q values in legend
    p.plot(i5.lastfit,symbol=0,line=[1,1,-1])   # plot fit as lines
    p.save('test.agr')



** Released under the GPLv3 **

