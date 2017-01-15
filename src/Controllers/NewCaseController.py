from PyQt5.Qt import QLineEdit  # For type annotation only, speeds up development in PyCharm.

from ViewController import ViewController


class NewCaseController(ViewController.Dialog):
    """
    A simple dialog that asks a user to fill in three fields.
    Naively assumes that the user has filled all fields, if they haven't the program will crash on certain actions
        later on during execution.
    """
    case_reference_field = None  # type: QLineEdit
    lab_reference_field = None  # type: QLineEdit
    investigator_field = None  # type: QLineEdit

    def __init__(self):
        """
        Initiates with the given dialog UI file.
        """
        super().__init__("newcase.ui")
