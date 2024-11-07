from core.editor import Editor
from core.options import OptionsBuilder
from core.handlers.reactangle_handler import RectangleHandler
from core.handlers.connector_handler import ConnectorHandler
from core.handlers.selection_handler import SelectionHandler


def init_editor() -> Editor:
    options = OptionsBuilder()
    options.set_handlers(
        [
            SelectionHandler("selection-handler"),
            RectangleHandler("rectangle-handler"),
            ConnectorHandler("connector-handler"),
        ]
    )
    options.set_default_handler_id("rectangle-handler")

    return Editor(options.build())