"""Module that contains a class to create a learning module instance
to create tasks inside a Jupyter Notebook"""
import json

from taskreview.task_database import TaskDatabase
from taskreview.tasks.pandas_dataframe_task import PandasDataframeTask
from taskreview.tasks.spark_dataframe_task import SparkDataframeTask
from taskreview.tasks.single_choice_task import SingleChoiceTask
from taskreview.tasks.multiple_choice_task import MultipleChoiceTask
from taskreview.widgets.task_evaluation_widgets import TaskEvaluationWidgets


class LearningModule:
    """
    A class used to represent a learning module

    ...

    Attributes
    ----------
    task_db: Database-File
        Database file representing exercises of each learning module
    db: Database
        Database object on which actions can be performed
    num_correct_answered: Counter
        counter that counts the correct answers
    taskList: list
        list that is used to collect all tasks of a learning module


    Methods
    -------
    show_task(task_id, solution)
        Creates a task based on task_id and database
    calculate_scored_points()
        Gets the calculated score
    get_score()
        Returns the overall score
    get_task_evaluation_string()
        Returns the points for each task
    """

    def __init__(self, task_db):
        self.database = TaskDatabase(task_db)
        self.scored_points = 0
        self.task_dict = {}
        self.score = 0
        self.task_options = {'DFP': PandasDataframeTask,
                             'DFS': SparkDataframeTask,
                             'SC': SingleChoiceTask,
                             'MC': MultipleChoiceTask,
                             }

        self.widgets = TaskEvaluationWidgets()
        self.task_points_dict = {}

    def show_task(self, task_id, solution=None):
        """Creates a task based on the task_id and all the associated
        informations from the database

        Parameters
        -------
        task_id : int
            id of the task that should be created
        solution : object
            solution that may be submitted by the user
        """
        task_row = self.database.fetch_task(task_id)

        try:
            if task_row['taskID'] in self.task_dict:
                self.task_dict[task_id].prepare_evaluation(solution)
            else:
                task_type = self.task_options[task_row['taskType']]
                task = task_type(self.database, task_row)
                task.prepare_evaluation(solution)
                self.task_dict[task_id] = task

        except TypeError as err:
            print(str(err) + '\nZu dieser Task-ID existiert keine Aufgabe.')
            return
        except KeyError as err:
            print(str(err) +
                  '\nFür diese Aufgabe wurde kein Task-Type hinterlegt.')
            return

    def calculate_scored_points(self):
        """Calculates the score in the learning module
        (Can be carried out at any point in the learning module)

        Returns
        -------
        int
            calculated score
        """
        self.scored_points = 0

        for task in self.task_dict.values():
            task_points = 0
            if isinstance(task, (SingleChoiceTask, MultipleChoiceTask)):
                task_points = task.calculate_scored_points()
            else:
                task_points = task.calculate_scored_points(
                    solution_btn_available=True)
            self.scored_points += task_points
            self.task_points_dict['Aufgabe ' + str(task.task_id)] = \
                str(int(task_points*100)) + ' %'

    ####################
    ### Submit score ###
    ####################

    def get_score(self):
        """Returns the overall score so that it can be transmitted to the
        learning platform
        """
        self.calculate_scored_points()
        percentage_scored_points = (
            100 / len(self.task_dict)) * self.scored_points
        return percentage_scored_points

    def get_task_evaluation_string(self):
        """Returns a string containing the points for every task
        """
        self.calculate_scored_points()
        return json.dumps(self.task_points_dict)
