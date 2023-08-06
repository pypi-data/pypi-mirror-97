"""Module that contains classes to create multiple choice tasks"""
import json

from taskreview.task import Task
from taskreview.widgets.choice_widgets import ChoiceWidgets


class MultipleChoiceTask(Task):
    """
    A class to represent a single choice task

    ...

    Attributes
    ----------
    mc_widgets : ChoiceWidgets
        class that contains widgets for single choice tasks
    options : Dictonary
        options that will be displayed by widget


    Methods
    -------
    interpret_solution_from_database(solution)
        Returns the solution from database as list
    check_solution(button)
        Checks the solution when the check button is clicked
    prepare_evaluation()
        Evaluates the task
    display_mc_buttons()
        Displays the multiple choice buttons
    """

    def __init__(self, db_conn, task_row):
        super().__init__(db_conn, task_row)
        self.options = json.loads(self.additional_info)
        self.mc_widgets = ChoiceWidgets(self.options, False)

    def interpret_solution_from_database(self, solution):
        """Changes the solution string from the database to correct data type

        Parameters
        ----------
        solution : string
            Includes the correct options for mc task

        Returns
        ----------
        List
            correct options
        """
        solution_list = json.loads(solution)
        if isinstance(solution_list, list):
            return solution_list
        else:
            return list(str(solution_list))

    def check_solution(self, button):
        """Checks if the solution the user chose is correct

        Parameters
        ----------
        button : Button
            Button that has been clicked to execute this method
        """

        correct_options = [self.options[key] for key in self.solution]

        if self.mc_widgets.get_selected_options() == correct_options:
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
        self.display_mc_buttons()
        self.display_buttons()

    def display_mc_buttons(self):
        """Makes it possible to evaluate the task by displaying the buttons
        """
        self.mc_widgets.display_multiple_choice_buttons()
