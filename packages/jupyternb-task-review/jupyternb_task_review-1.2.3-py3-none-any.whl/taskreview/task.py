"""Module that contains a class to create a task."""

from abc import ABCMeta, abstractmethod

from taskreview.widgets.task_evaluation_widgets import TaskEvaluationWidgets
from taskreview.counter import Counter


class Task(metaclass=ABCMeta):
    """
    A class used to represent a task

    ...

    Attributes
    ----------
    widgets : TaskEvaluationWidgets
        class that contains widgets for task evaluation
    solution : object
        solution of the task
    additional_info : str
        solution that should be displayed when the solution button is hit
        or options of sc/ mc tasks
    tipp : str
        tipp that helps the user to edit the task
    txt_incorrect_answer : str
        text that is shown when the user solution was wrong
    user_solution : object
        solution that the user created for a task
    cnt_false_answers : Counter
        counter that counts the false answers of a user for a task
    is_task_answered_correctly : Boolean
        displays if a user has already edited the task correctly
    db: Database
        Database connection to get information about tasks


    Methods
    -------
    print_solution(button)
        Prints the solution when the solution button is clicked
    print_tipp(button)
        Prints the tipp when the tipp button is clicked
    display_buttons()
        Displays the check and tipp button
    display_colution_btn():
        Displays the check, tipp and solution button
    display_img_correct():
        Displays the check image
    display_text(text):
        Displays the given text
    check_solution():
        Abstract method to check the user solution
    calculate_scored_points()
        Abstract method to calculate points
    """

    def __init__(self, db_conn, task_row):
        self.db_conn = db_conn
        # id of task
        self.task_id = task_row['taskID']

        # init buttons for evaluation of task
        self.widgets = TaskEvaluationWidgets()
        self.widgets.create_tipp_button(self.print_tipp)
        self.widgets.create_check_button(self.check_solution)
        self.widgets.create_solution_button(self.print_solution)

        # information about task
        self.solution = self.interpret_solution_from_database(
            task_row['solutionForReview'])
        self.additional_info = task_row['additionalInformation']
        self.tipp = task_row['tipp']

        # text for incorrect answers
        self.txt_incorrect_answer = 'Leider nicht korrekt. \
            Bitte versuche es erneut.'

        # user specific information
        self.user_solution = None
        self.cnt_false_answers = Counter()
        self.is_task_answered_correctly = False
        self.solution_printed = False

    ###########################
    ### methods for buttons ###
    ###########################

    def print_solution(self, button):
        """Prints the solution of a task as text/ code

        Parameters
        -------
        button : Button
            Button that has been clicked to execute this method

        """
        self.solution_printed = True
        self.widgets.display_html_in_output_field(self.additional_info)

    def print_tipp(self, button):
        """Prints the tipp of a task

        Parameters
        -------
        button : Button
            Button that has been clicked to execute this method

        """

        self.widgets.display_html_in_output_field(self.tipp)

    ################################
    ### display buttons for task ###
    ################################

    def display_buttons(self):
        """Displays the buttons needed for task evaluation
        """

        if not self.tipp:
            self.widgets.display_check_btn()
        else:
            self.widgets.display_check_and_tipp_btn()

        if self.is_task_answered_correctly:
            self.display_img_correct()

    def display_solution_btn(self):
        """Adds a solution button next to the check and tipp button
        """

        if not self.tipp:
            self.widgets.display_check_and_solution_button()
        else:
            self.widgets.display_check_tipp_and_solution_button()

    def display_disabled_buttons(self):
        """Displays the disabled check (and tipp) buttons
        """

        self.widgets.display_disabled_check_and_tipp_button()

    ###############################
    ### display task evaluation ###
    ###############################

    def display_img_correct(self):
        """Displays the check image
        """

        self.widgets.display_check_img()

    def display_text(self, text):
        """Displays the given text

        Parameters
        -------
        text : str
            Text that should be displayed

        """

        self.widgets.display_html_in_output_field(text)

    def calculate_scored_points(self, solution_btn_available=False):
        """Calculate the points that were scored in a task

        Returns
        -------
        scored_points : int
            normalized points that were scored in the task

        """
        scored_points = 0

        if self.is_task_answered_correctly:
            scored_points += 1
            if self.cnt_false_answers.get_value() < 3:
                scored_points += 1
            if solution_btn_available:
                if not self.solution_printed:
                    scored_points += 1
                return scored_points / 3
        return scored_points / 2

    #######################
    ### abstract method ###
    #######################

    @abstractmethod
    def check_solution(self, button):
        """Checks if the solution of the user is correct

        Parameters
        -------
        button : Button
            Button that has been clicked to execute this method

        """

    @abstractmethod
    def prepare_evaluation(self, solution):
        """Makes it possible to evaluate the task by displaying the buttons.
        Shows user solution as spark dataframe.

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            Dataframe that the user submitted
        """

    @abstractmethod
    def interpret_solution_from_database(self, solution):
        """Changes the solution string from the database to correct data type
        depending on the task type

        Parameters
        ----------
        solution : string
            Solution of task
        """
