.. klink-demo documentation master file, created by
   sphinx-quickstart on Tue Jul  1 13:40:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

klink - A Simple Sphinx Theme
=============================

Klink is a simple sphinx theme. It is heavily inspired by `jrnl's theme
<https://github.com/maebert/jrnl>`__. 

Options
-------

Here are the theme options. They should be added to the html_theme_options in
your **conf.py** file.

    * **github**
      The github address of the project. The format is name/project
      (pmorissette/klink).
    * **logo**
      The logo file. Assumed to be in _static. Default is logo.png. The logo
      should be 150x150.
    * **analytics_id**
      Your Google Analytics id (usually starts with UA-...)

Python Code
-----------

Here is a quick example on how you would insert a IPython Notebook. Everything
you see below this paragraph is actually a Notebook that was converted to
a .rst file for inclusion in this document. Klink's convert_notebooks() does the conversion.  All
you have to do is include the .rst file. It will have the same name as the
notebook.

.. include:: intro.rst

.. toctree::
    :hidden: 
    :maxdepth: 2

    Overview <index>
    Installation Guide <install>
    API <klink>
