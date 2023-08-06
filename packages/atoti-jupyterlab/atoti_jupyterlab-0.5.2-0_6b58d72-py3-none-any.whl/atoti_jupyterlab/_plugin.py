from pathlib import Path
from typing import Optional

from atoti._plugins import Plugin
from atoti.experimental.distributed.session import DistributedSession
from atoti.query.session import QuerySession
from atoti.session import Session

from ._widget_manager import WidgetManager, visualize


class JupyterLabPlugin(Plugin):
    """JupyterLab plugin."""

    _widget_manager: WidgetManager = WidgetManager()

    def static_init(self):
        """Init to be called only once."""
        Session.visualize = visualize  # type: ignore
        DistributedSession.visualize = visualize  # type: ignore
        QuerySession.visualize = visualize  # type: ignore

    def get_jar_path(self) -> Optional[Path]:
        """Return the path to the JAR."""
        return None

    def init_session(self, session: Session):
        """Initialize the session."""
        session._widget_manager = self._widget_manager  # type: ignore # pylint: disable=protected-access

    def init_query_session(self, query_session: QuerySession):
        """Iniialize the query session."""
        query_session._widget_manager = self._widget_manager  # type: ignore # pylint: disable=protected-access
