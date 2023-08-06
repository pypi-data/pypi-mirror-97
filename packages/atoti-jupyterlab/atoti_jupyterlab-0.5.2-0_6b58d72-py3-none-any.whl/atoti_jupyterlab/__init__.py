"""Plugin to interactively visualize atoti sessions in JupyterLab.

This package is required to use :meth:`atoti.session.Session.visualize` and :meth:`atoti.query.session.QuerySession.visualize`.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[jupyterlab]

  * .. code-block:: bash

      conda install atoti-jupyterlab
"""

import json
from pathlib import Path
from typing import Collection, Mapping

from ._version import VERSION as __version__

_SOURCE_DIRECTORY = Path(__file__).parent

_LABEXTENSION_FOLDER = "labextension"

_PACKAGE_DATA = json.loads(
    (_SOURCE_DIRECTORY / _LABEXTENSION_FOLDER / "package.json").read_text()
)


def _jupyter_labextension_paths() -> Collection[Mapping[str, str]]:
    """Return the paths used by JupyterLab to load the extension assets."""
    return [{"src": _LABEXTENSION_FOLDER, "dest": _PACKAGE_DATA["name"]}]
