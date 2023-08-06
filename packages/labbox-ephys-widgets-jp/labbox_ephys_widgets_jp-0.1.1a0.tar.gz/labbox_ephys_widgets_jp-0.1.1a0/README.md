labbox-ephys-widgets-jp
===============================

Labbox-ephys jupyter widgets

Installation
------------

To install use pip:

    $ pip install labbox_ephys_widgets_jp

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/flatironinstitute/labbox-ephys-widgets-jp.git
    $ cd labbox-ephys-widgets-jp
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix labbox_ephys_widgets_jp
    $ jupyter nbextension enable --py --sys-prefix labbox_ephys_widgets_jp

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite labbox_ephys_widgets_jp

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
