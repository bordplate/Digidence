from PyQt5.Qt import QFileDialog, QMessageBox

from ViewController import ViewController

from Models.Case import Case

from Controllers.CaseController import CaseController
from Controllers.NewCaseController import NewCaseController


class WelcomeController(ViewController):
    """
    The first view the user is greeted with.
    Gives the user the chance to open an existing case or start a new one.

    Supposed to show recently opened cases as well, but never got that far.
    """

    def __init__(self):
        """
        Open the design from a UI-file and connect the buttons to local functions.
        """
        super().__init__("welcome.ui")

        # Connect our two buttons for opening a project or starting a new one.
        self.new_case_button.clicked.connect(self.start_new_case)
        self.open_case_button.clicked.connect(self.open_case)

    def start_new_case(self):
        """
        Opens a dialog asking for case information and then opens case project window.
        :return: None
        """
        dialog = NewCaseController()
        clicked_ok = dialog.exec_()

        if clicked_ok:
            # Initiate a whole new case and feed it to a CaseController
            case = Case()
            case.case_reference = dialog.case_reference_field.text()
            case.lab_reference = dialog.lab_reference_field.text()
            case.investigator = dialog.investigator_field.text()

            case_controller = CaseController(case)

            self.open_window(case_controller)

    def open_case(self):
        """
        Gives the user a file dialog to find their existing project and opens that.
        :return: None
        """
        open_dialog = QFileDialog()

        user_location = open_dialog.getOpenFileName()[0]  # Index 0 because user can't pick more than one file.
        if user_location == '':
            return  # User most likely pressed cancel.

        case = Case.open_from_disk(user_location)

        if case is None:  # Something bad must have happened. Tell the user that the file is corrupt. Or invalid.
            alert = QMessageBox()
            alert.setText("Corrupt case file or invalid file type.")
            alert.setIcon(QMessageBox.Critical)

            alert.exec_()

            return
        else:
            # Successfully open a case!
            case_controller = CaseController(case)

            self.open_window(case_controller)
