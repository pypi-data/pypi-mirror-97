"""Module that contains classes to single choice tasks"""
import json

from taskreview.widgets.choice_widgets import ChoiceWidgets
from taskreview.task import Task


class SingleChoiceTask(Task):
    """
    A class to represent a single choice task

    ...

    Attributes
    ----------
    single_choice_widgets : ChoiceWidgets
        class that contains widgets for single choice tasks
    options : Dictonary
        options that will be displayed by widget


    Methods
    -------
    interpret_solution_from_database(solution)
        Returns the solution from database as string
    check_solution(button)
        Checks the solution when the check button is clicked
    prepare_evaluation()
        Evaluates the task
    display_sc_buttons()
        Displays the single choice buttons
    """

    def __init__(self, db_conn, task_row):
        super().__init__(db_conn, task_row)
        self.options = json.loads(self.additional_info)
        self.sc_widgets = ChoiceWidgets(self.options)

    def interpret_solution_from_database(self, solution):
        """Changes the solution string from the database to correct data type

        Parameters
        ----------
        solution : string
            Includes the correct options for sc task

        Returns
        ----------
        String
            correct options
        """
        return str(solution)

    def check_solution(self, button):
        """Checks if the solution the user chose is correct

        Parameters
        ----------
        button : Button
            Button that has been clicked to execute this method
        """
        selected_widget_index = self.sc_widgets.sc_btns.value
        selected_solution_index = list(self.options.keys())[
            selected_widget_index]

        if selected_solution_index == self.solution:

            self.is_task_answered_correctly = True
            self.display_img_correct()
            self.display_disabled_buttons()
        else:
            self.display_text(self.txt_incorrect_answer)

            # increment counter of tries
            self.cnt_false_answers.increment()

    def prepare_evaluation(self, solution):
        """Makes it possible to evaluate the task by displaying the buttons
        """
        self.display_sc_buttons()
        self.display_buttons()

    def display_sc_buttons(self):
        """Displays the single choice, check and tipp buttons
        """
        self.sc_widgets.display_single_choice_buttons()
