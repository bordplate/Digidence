from Models.Event import Event
from Models.Evidence import Evidence

import pickle

class Case(object):
    """

    """
    case_reference = None  # type: str
    lab_reference = None  # type: str
    investigator = None  # type: str

    events = []  # type: [Event]
    physical_evidence = []  # type: [Evidence]

    save_location = None  # type: str

    def event_to_html(self, event: Event) -> str:
        """
        Returns HTML representation of an event.
        :param event: Event to turn into HTML
        :return: HTML string
        """
        template_file = open("Views/event_record.html", "r")
        template = template_file.read()

        template = template.replace("${CaseRef}", self.case_reference)
        template = template.replace("${ItemUUID}", event.device)
        template = template.replace("${StartDate}", event.start_time)
        template = template.replace("${Comments}", event.comments)
        template = template.replace("${StopDate}", event.stop_time)
        template = template.replace("${InvestigatorName}", self.investigator)

        return template

    def evidence_to_html(self, evidence: Evidence) -> str:
        """
        Returns HTML representation of some evidence.
        Basically takes an HTML template and replaces keywords with actual content.
        :param evidence: Evidence to turn into HTML
        :return: HTML string
        """
        template_file = open("Views/evidence_record.html", "r")
        template = template_file.read()

        template = template.replace("${CaseRef}", self.case_reference)
        template = template.replace("${LabRef}", self.lab_reference)
        template = template.replace("${ItemUUID}", evidence.unique_identifier)
        template = template.replace("${SeizedDate}", evidence.seized_date)
        template = template.replace("${AdditionalInfo}", evidence.additional_information)
        template = template.replace("${DeviceDesc}", evidence.description)
        template = template.replace("${InvestigatorName}", self.investigator)

        return template

    def save_to_disk(self):
        """
        Will save to disk if `save_location` is set
        :return: None
        """
        if self.save_location is None:
            return  # Can't save if we don't know where to

        with open(self.save_location, 'wb') as dump_file:
            pickle.dump(self, dump_file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def open_from_disk(location: str):  # Can not type annotate return value because of recursion in classes...
        """
        Opens a case from a location and returns that.
        Naively assumes that the location is readable and writable.
            The location should come from a file picker anyway, and those files will exist 99.99% of the time.
        :param location: Location on disk
        :return: Returns a Case or None if something bad has happened.
        """
        file = open(location, "rb")
        try:
            return pickle.load(file)
        except TypeError:
            return None
        except pickle.UnpicklingError:
            print("Lid stuck too hard, ask someone for help.")
            return None
        except EOFError as error:
            print("Could not parse file for unpickling. Unexpected end of file.")
            return None
