Klink - A Sphinx Theme
======================

Sphinx is a **simple** and **clean** theme for creating `Sphinx docs
<http://sphinx-doc.org/>`__. It is heavily inspired by the beautiful `jrnl's theme
<https://github.com/maebert/jrnl>`__. It also supports embedding `IPython
Notebooks <http://ipython.org/notebook.html>`__ which can be mighty useful.

Installation
------------

Assuming you have pip installed:

.. code:: bash

    $ pip install klink

That's it.

Usage
-----

In your docs' **conf.py** file, add the following:

.. code:: python

    import klink

    html_theme = 'klink'
    html_theme_path [klink.get_html_theme_path()]
    html_theme_options = {
        'github': 'yourname/yourrepo',
        'analytics_id': 'UA-your-number-here',
        'logo': 'logo.png'
    }

Klink also comes with a useful helper function that allows you to integrate an
IPython Notebook into a .rst file. It basically converts the Notebook to .rst
and copies the static data (images, etc) to your _static dir. 

If you have IPython Notebooks that you would like to integrate, use the
following code to your **conf.py**:

.. code:: python

    klink.convert_notebooks()

Once the conversion is done, you will have a .rst file with the same name as
each one of your notebooks.

*Note: place your notebooks in your docs' source dir.*

Now all you have to do is use the **include** command to insert them into your
docs.

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
