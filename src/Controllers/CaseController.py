from PyQt5.Qt import *

from ViewController import ViewController

from Models.Case import Case
from Models.Event import Event
from Models.Evidence import Evidence


class CaseController(ViewController):
    """
    Main project view controller for managing the current case.
    """
    case = None  # type: Case

    # Define used UI elements that are imported from the UI-file.
    events_list = None  # type: QListView
    physical_evidence_list = None  # type: QListView

    start_time_field = None  # type: QDateTimeEdit
    stop_time_field = None  # type: QDateTimeEdit
    seized_date_field = None  # type: QDateTimeEdit

    comments_field = None  # type: QTextEdit
    additional_information_field = None  # type: QTextEdit

    add_event_button = None  # type: QPushButton
    add_physical_button = None  # type: QPushButton

    unique_identifier_field = None  # type: QLineEdit
    device_description_field = None  # type: QLineEdit

    # Models used for populating events and physical evidence lists
    events_list_model = None  # type: QStandardItemModel
    physical_evidence_list_model = None  # type: QStandardItemModel

    def __init__(self, case):
        """
        Initiates a case view controller with a given case.
        :param case: Case must be provided.
        """
        super().__init__("case.ui")

        self.case = case

        self.setWindowTitle("Case: " + self.case.case_reference)

        # Configure UI elements
        self.setup_callbacks()
        self.setup_lists()
        self.add_menu_bar_items()
        self.load_case_into_tables()

    # Configuration functions ----------------------------------------------------------------------------------------

    def setup_callbacks(self):
        """
        Configures the pushable buttons in the view.
        :return: None
        """
        self.add_event_button.clicked.connect(self.clicked_add_event)
        self.add_physical_button.clicked.connect(self.clicked_add_physical_evidence)

        self.physical_evidence_list.clicked.connect(self.selected_physical_evidence)

    def setup_lists(self):
        """
        Configures the lists for events and physical evidence.
        :return: None
        """
        self.events_list_model = QStandardItemModel()
        self.events_list.setModel(self.events_list_model)

        self.physical_evidence_list_model = QStandardItemModel()
        self.physical_evidence_list.setModel(self.physical_evidence_list_model)

    def add_menu_bar_items(self):
        """
        Adds all menubar items for this window.
        :return: None
        """
        self.menuBar = QMenuBar(self)
        fileMenu = self.menuBar.addMenu('File')

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)

        exitAction = QAction("Quit", self)  # Qt uses Mac's standard function for this, so only effective on Win/Linux
        exitAction.triggered.connect(quit)

        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        printMenu = self.menuBar.addMenu('Print')

        printAllAction = QAction("Print all", self)
        printAllAction.setShortcut("Ctrl+P")
        printAllAction.triggered.connect(self.print_all)

        printEventAction = QAction("Print selected event", self)
        printEventAction.setShortcut("Ctrl+E")
        printEventAction.triggered.connect(self.print_event)

        printPhysicalAction = QAction("Print selected evidence", self)
        printPhysicalAction.setShortcut("Shift+Ctrl+P")
        printPhysicalAction.triggered.connect(self.print_evidence)

        printMenu.addAction(printAllAction)
        printMenu.addAction(printEventAction)
        printMenu.addAction(printPhysicalAction)

    def load_case_into_tables(self):
        """
        Loads all relevant case information into tables.
        :return: None
        """
        for event in self.case.events:
            self.add_event(event.start_time, event.stop_time, event.comments, event.device)

        for evidence in self.case.physical_evidence:
            self.add_physical_evidence(evidence.seized_date, evidence.description,
                                       evidence.additional_information, evidence.unique_identifier)

    # End configuration functions ------------------------------------------------------------------------------------

    def clicked_add_event(self):
        """
        Callback for when the add-button in the events-tab of the UI has been clicked.
        :return: None
        """
        if self.start_time_field.text() == "" or self.stop_time_field.text() == "" or \
                        self.comments_field.toPlainText() == "":
            return self.prompt_user_to_fill_all_fields()

        # Create and add event to case and then add to list of events
        event = self.add_event(self.start_time_field.text(), self.stop_time_field.text(),
                               self.comments_field.toPlainText(), self.selected_physical_item())

        # Add event to case instance.
        self.case.events += [event]

        self.clear_fields()

    def clicked_add_physical_evidence(self):
        """
        Callback for when the add-button in the physical evidence-tab of the UI has been clicked.
        :return: None
        """
        # Perform to check that no fields are empty
        if self.additional_information_field.toPlainText() == "" or self.seized_date_field.text() == "" or \
                self.device_description_field.text() == "" or self.unique_identifier_field.text() == "":
            return self.prompt_user_to_fill_all_fields()

        evidence = self.add_physical_evidence(self.seized_date_field.text(),
                                              self.device_description_field.text(),
                                              self.additional_information_field.toPlainText(),
                                              self.unique_identifier_field.text())

        # Add evidence to our case instance.
        self.case.physical_evidence += [evidence]

        self.clear_fields()  # User probably don't want to add same stuff twice, so clear the fields.

    def add_event(self, start_time: str, stop_time: str, comments: str, device: str) -> Event:
        """
        Adds an event to the UI list of events.
        :param start_time: What date/time the user started working on this event.
        :param stop_time: Date/time user stopped working.
        :param comments: What the user has done during this time.
        :param device: Which device the user worked on.
        :return: Event object created
        """
        event = Event()
        event.start_time = start_time
        event.stop_time = stop_time
        event.comments = comments
        event.device = device

        # Add to UI list
        item = QStandardItem(event.comments)
        item.setEditable(False)
        self.events_list_model.appendRow([item])

        return event

    def add_physical_evidence(self, seized_date: str, device_description: str, additional_information: str,
                              unique_identifier: str) -> Evidence:
        """
        Adds a physical evidence (device) to the UI list of evidence.
        Also returns back an evidence instance that can be used by whoever called this function.
        :param seized_date: Date the evidence has been seized
        :param device_description: A short description about the evidence.
        :param additional_information: Additional information about the evidence
        :param unique_identifier: A unique identifier
        :return: Evidence object created
        """
        evidence = Evidence()
        evidence.seized_date = seized_date
        evidence.description = device_description
        evidence.additional_information = additional_information
        evidence.unique_identifier = unique_identifier

        item = QStandardItem(evidence.unique_identifier + "\n" + evidence.description)
        item.setEditable(False)
        self.physical_evidence_list_model.appendRow([item])

        return evidence

    def selected_physical_item(self) -> str:
        """
        Returns the unique identifier of the currently selected item in the physical evidence-list
        :return: Unique identifier of the currently selected item.
        """
        selected_index = self.physical_evidence_list.selectedIndexes()[0]  # Just support selecting one item at a time
        return self.case.physical_evidence[selected_index.row()].unique_identifier

    def selected_physical_evidence(self):
        """
        Gets notified when an item in the physical evidence-list is selected and enables the event-add-button.
        :return: None
        """
        self.add_event_button.setDisabled(False)

    def clear_fields(self):
        """
        Clears the fields in the event and evidence logging tabs.
        We let the date/time fields stay the way they were.
        :return: None
        """
        self.comments_field.setText("")
        self.unique_identifier_field.setText("")
        self.additional_information_field.setText("")

    def save(self):
        """
        Saves the project to a location
        :return: None
        """
        if self.case.save_location is None:
            save_dialog = QFileDialog()
            save_dialog.setAcceptMode(QFileDialog.AcceptSave)
            save_dialog.setNameFilter(self.tr("Case file (*.digicase)"))
            save_dialog.setDefaultSuffix(".digicase")
            save_dialog.setFileMode(QFileDialog.AnyFile)

            save_location = save_dialog.getSaveFileName(filter=".digicase")
            if save_location[0] != "":
                self.case.save_location = save_location[0] + save_location[1]  # Location and append filetype
            else:
                return

        self.case.save_to_disk()


    def print_all(self):
        """
        Presents the user with a print-dialog.
        :return: None
        """
        print_dialog = QPrintDialog()

        if print_dialog.exec_() == 0:
            return  # User pressed cancel.

        printer = print_dialog.printer()

        if printer is None:  # User obviously don't want to print after all.
            return

        # Starting and ending a painter will enable us to print mulitple pages in one document.
        # The printer will start printing when painter.end() is called.
        painter = QPainter()
        painter.begin(printer)

        for event in self.case.events:
            self.print(printer, self.case.event_to_html(event), painter)

            printer.newPage()

        first = True
        for evidence in self.case.physical_evidence:
            # Stops us from having an empty page at the end of the document
            if first:
                first = False
            else:
                printer.newPage()

            self.print(printer, self.case.evidence_to_html(evidence), painter)

        painter.end()

    def print_event(self):
        """
        Presents the user with a dialog to print the currently selected event, if any.
        :return: None
        """
        indexes = self.events_list.selectedIndexes()
        if len(indexes) <= 0:
            return  # Bail out, user hasn't selected anything in the list

        # Only one item can be selected at a time anyway, so we just default to index 0
        selected_index = indexes[0].row()

        print_dialog = QPrintDialog()
        if print_dialog.exec_() == 0:
            return  # User pressed cancel.

        printer = print_dialog.printer()

        self.print(printer, self.case.event_to_html(self.case.events[selected_index]))

    def print_evidence(self):
        """
        Presents the user with a dialog to print the currently selected physical evidence.
        :return: None
        """
        indexes = self.physical_evidence_list.selectedIndexes()
        if len(indexes) <= 0:
            return  # Bail out, user hasn't selected anything in the list

        print_dialog = QPrintDialog()
        if print_dialog.exec_() == 0:
            return  # User pressed cancel.

        printer = print_dialog.printer()

        # Only one item can be selected at a time anyway, so we just default to index 0
        selected_index = indexes[0].row()

        self.print(printer, self.case.event_to_html(self.case.events[selected_index]))

    @staticmethod
    def print(printer: QPrinter, html: str, painter=None):
        """
        Prints the given html either directly to the printer or through a painter object.
        :param printer: Printer object to be used for printing.
        :param html: HTML to print
        :param painter: Optional painter, used for printing multiple pages
        :return: None
        """
        document = QTextDocument()  # This text document holds HTML template the records.
        document.setTextWidth(printer.pageRect().width())  # When using painter, this makes document conform to size.

        document.setHtml(html)

        # Tried to add some margin when using a painter, but didn't work

        if painter is None:
            document.print(printer)
        else:
            document.drawContents(painter)

        document.deleteLater()  # Marks document as up-for-grabs by garbage collector.

    @staticmethod
    def prompt_user_to_fill_all_fields():
        """
        Prompts the user to fill out all fields.
        :return: None
        """
        prompt = QMessageBox()
        prompt.setIcon(QMessageBox.Warning)
        prompt.setText("You must fill out all the fields!")
        prompt.exec_()
