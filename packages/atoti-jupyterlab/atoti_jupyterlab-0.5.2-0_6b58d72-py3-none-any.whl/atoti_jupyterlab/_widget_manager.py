from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Union
from uuid import uuid4

from atoti._ipython_utils import running_in_ipython
from atoti.experimental.distributed.session import DistributedSession
from atoti.query.session import QuerySession
from atoti.session import Session

from ._version import VERSION

if TYPE_CHECKING:
    from ipykernel.ipkernel import IPythonKernel


# Keep in sync with widgetCommTargetName in WidgetComm.ts.
_WIDGET_COMM_TARGET_NAME = "atoti-widget"

# Keep in sync with widgetMimeType in widgetMimeType.ts.
_WIDGET_MIME_TYPE = f"application/vnd.atoti.widget.v{VERSION.split('.')[0]}+json"

_Session = Union[Session, DistributedSession, QuerySession]


@dataclass(frozen=True)
class Cell:
    """Hold some details about the notebook cell currently being executed."""

    has_built_widget: bool
    id: str


class WidgetManager:
    """Manage Jupyter comms and keep track of the widget state coming from kernel requests."""

    _cell: Optional[Cell] = None
    _running_in_supported_kernel: bool = False

    def __init__(self):
        """Create the manager."""
        if not running_in_ipython():
            return

        from IPython import get_ipython

        ipython = get_ipython()

        if not hasattr(ipython, "kernel") or not hasattr(
            ipython.kernel, "comm_manager"
        ):
            # When run from IPython or another less elaborated environment
            # than JupyterLab, these attributes might be missing.
            # In that case, there is no need to register anything.
            return

        self._running_in_supported_kernel = True

        kernel = ipython.kernel

        self._wrap_execute_request_handler_to_extract_widget_details(kernel)

    def display_widget(self, session: _Session, name: Optional[str]):
        """Display the output that will lead the atoti JupyterLab extension to show a widget."""
        if not self._running_in_supported_kernel:
            print(
                "atoti widgets can only be shown in JupyterLab with the atoti JupyterLab extension enabled."
            )
            return

        from ipykernel.comm import Comm
        from IPython.display import publish_display_data

        publish_display_data(
            {
                _WIDGET_MIME_TYPE: {
                    "name": name,
                    "session": session.name,
                },
                "text/plain": f"""Open the notebook in JupyterLab with the atoti extension installed and enabled to {"see" if self._cell and self._cell.has_built_widget else "start editing"} this widget.""",
            }
        )

        if self._cell is None:
            return

        widget_id = str(uuid4())

        Comm(
            _WIDGET_COMM_TARGET_NAME,  # type: ignore
            data={
                "cellId": self._cell.id,
                "session": {
                    "headers": session._generate_auth_headers(),  # pylint: disable=protected-access
                    "isQuerySession": isinstance(session, QuerySession),
                    "port": session.port,
                    "url": session.url.rstrip("/"),
                },
                "widgetId": widget_id,
            },
        ).close()

        if not isinstance(session, Session):
            return

        session._java_api.block_until_widget_loaded(  # pylint: disable=protected-access
            widget_id
        )

    def _wrap_execute_request_handler_to_extract_widget_details(
        self, kernel: IPythonKernel  # type: ignore
    ):
        original_handler = kernel.shell_handlers["execute_request"]

        def execute_request(stream: Any, ident: Any, parent: Any) -> Any:
            metadata = parent["metadata"]
            cell_id = metadata.get("cellId")
            self._cell = (
                Cell(bool(metadata.get("atoti", {}).get("state")), cell_id)
                if cell_id is not None
                else None
            )

            return original_handler(stream, ident, parent)

        kernel.shell_handlers["execute_request"] = execute_request


def visualize(self: _Session, name: Optional[str] = None):  # noqa: D417
    """Display an atoti widget to explore the session interactively.

    Note:
        This method requires the :mod:`atoti-jupyterlab <atoti_jupyterlab>` plugin.

    The widget state will be stored in the cell metadata.
    This state should not have to be edited but, if desired, it can be found in JupyterLab by opening the "Notebook tools" sidebar and expanding the the "Advanced Tools" section.

    Args:
        name: The name to give to the widget.
    """
    self._widget_manager.display_widget(self, name)  # type: ignore  # pylint: disable=protected-access
