from PyQt5.Qt import *
from PyQt5.uic import *


class ViewController(QWidget):
    def __init__(self, view_name: str):
        """
        Initiates a view controller with given UI-file as view.
        :param view_name: Name of the view to open.
        """
        super().__init__()

        loadUi("Views/" + view_name, self)

    def open_window(self, window, close_self=True):
        """
        Opens a new a window.
        :param window: Window should be of type ViewController.
        :param close_self: Whether or not to close the window that opens the new window.
        :return: None
        """
        window.show()

        # Python's GC will -1 the reference count of `window` at the end of this function.
        # The line underneath makes sure the retain count for the window is +1'd and will keep the retain count at
        #   1 when the function has finished.
        window.window = window.window  # Hack to stop Python's garbage collector from throwing stones at the window.

        if close_self:
            self.close()

    class Dialog(QDialog):
        def __init__(self, view_name: str):
            super().__init__()

            loadUi("Views/" + view_name, self)
