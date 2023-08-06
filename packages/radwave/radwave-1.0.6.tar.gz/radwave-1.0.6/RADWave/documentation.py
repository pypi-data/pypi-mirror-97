"""
Copyright 2020 Tristan Salles

RADWave is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later
version.

RadWave is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RADWave.  If not, see <http://www.gnu.org/licenses/>.
"""

import pkg_resources as _pkg_resources
from distutils import dir_util as _dir_util


def install_documentation(path="./RADWave-Notebooks"):
    """Install the example notebooks for RADWave in the given location
    WARNING: If the path exists, the Notebook files will be written into the
    path and will overwrite any existing files with which they collide. The
    default path ("./RADWave-Notebooks") is chosen to make collision less
    problematic. The documentation for RADWave is in the form of jupyter
    notebooks.
    """

    # Question - overwrite or not ? shutils fails if directory exists.

    Notebooks_Path = _pkg_resources.resource_filename('RADWave', 'Notebooks')

    _dir_util.copy_tree(Notebooks_Path, path, preserve_mode=1,
                        preserve_times=1, preserve_symlinks=1,
                        update=0, verbose=1, dry_run=0)
