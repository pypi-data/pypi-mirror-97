import os

from distutils import dir_util

from seeq.base import system

from .. import _common


def copy(folder=None, *, overwrite=False, advanced=False):
    """
    Copies the SPy Documentation (Jupyter Notebooks) to a particular folder. This is typically used when the seeq
    module is installed via PyPI.

    This function should be called again with overwrite=True if the seeq module is updated.

    Parameters
    ----------
    folder : str
        The folder to receive the documentation. By default it will be copied to a 'SPy Documentation' folder in the
        current working directory.

    overwrite : bool
        If True, any existing files in the specified folder will be deleted before the documentation is copied in.

    advanced : bool
        If True, documentation for advanced functions like workbook manipulation are included.
    """
    _common.validate_argument_types([
        (folder, 'folder', str),
        (overwrite, 'overwrite', bool),
        (advanced, 'advanced', bool)
    ])

    if not folder:
        folder = os.path.join(os.getcwd(), 'SPy Documentation')

    folder = system.cleanse_path(folder)

    if os.path.exists(folder):
        if not overwrite:
            raise RuntimeError('The "%s" folder already exists. If you would like to overwrite it, supply the '
                               'overwrite=True parameter. Make sure you don\'t have any of your own work in that '
                               'folder!' % folder)

        dir_util.remove_tree(folder)

    library_doc_folder = system.cleanse_path(os.path.join(os.path.dirname(__file__), 'Documentation'))

    dir_util.copy_tree(library_doc_folder, folder)

    if not advanced:
        os.remove(os.path.join(folder, 'spy.workbooks.ipynb'))
        os.remove(os.path.join(folder, 'Advanced Reports and Dashboards.ipynb'))

    print('Copied SPy library documentation to "%s"' % folder)
