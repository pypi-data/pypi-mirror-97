***********************************
About pyGDM-UI
***********************************

pyGDM-UI is a pyqt based, pure python graphical user interface to pyGDM2. It provides the most common functionalities of pyGDM2 for rapid simulations and testing.


Requirements
================================

    - **python** (tested with 3.5+, `link python <https://www.python.org/>`_)
    - **pyGDM2** (v1.1+, `link pyGDM2 <https://wiechapeter.gitlab.io/pyGDM2-doc/>`_)
    - **pyqt5** (`link pyqt5 <https://pypi.org/project/PyQt5/>`_)
    - **matplotlib** (`link matplotlib <https://matplotlib.org/>`_)
    - **mayavi** (`link mayavi <http://docs.enthought.com/mayavi/mayavi/mlab.html>`_)

Installation
=============================================

via pip
-------------------------------

Install from pypi repository via

.. code-block:: bash
    
    $ pip install pygdmUI

install mayavi
++++++++++++++++++++++++

linux: Works easiest if you use the package manager of your distribution. For example under ubuntu:

.. code-block:: bash
    
    $ sudo apt install mayavi2

windows: Tested with mayavi of the anaconda python distribution. In the anaconda terminal, install via

.. code-block:: bash
    
    $ conda install mayavi

See also: https://docs.enthought.com/mayavi/mayavi/installation.html for more detailed instructions on how to install mayavi.

Manual installation
-------------------------------

Download the latest code from `gitlab <https://gitlab.com/wiechapeter/pygdm-ui>`_ or clone the git repository:

.. code-block:: bash
    
    $ git clone https://gitlab.com/wiechapeter/pygdm-ui.git
    $ cd pygdm-ui
    $ python setup.py install --user

    

Run pyGDM-UI
=============================================

In the terminal:

.. code-block:: bash
    
    $ python3 -m pygdmUI.main

    


Author
=========================

   - P\. R. Wiecha



