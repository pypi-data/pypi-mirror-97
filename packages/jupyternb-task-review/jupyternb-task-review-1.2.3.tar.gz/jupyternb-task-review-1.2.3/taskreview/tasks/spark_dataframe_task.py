"""Module that contains class to create Spark dataframe tasks."""

try:
    import pandas as pd
    from pyspark.sql import DataFrame
except ModuleNotFoundError:
    pass

from taskreview.tasks.pandas_dataframe_task import PandasDataframeTask


class SparkDataframeTask(PandasDataframeTask):
    """
    A class used to represent a spark dataframe task

    Methods
    -------
    prepare_evaluation(df)
        Evaluates the task based on the submitted solution
    user_input_of_correct_datatype(solution)
        check if user input is of spark dataframe datatype
    """

    def prepare_evaluation(self, solution):
        """Makes it possible to evaluate the task by displaying the buttons.
        Shows user solution as spark dataframe.

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            Dataframe that the user submitted
        """
        if self.user_input_of_correct_datatype(solution):
            solution.show()
            pd.set_option('precision', 15)
            self.user_solution = solution.toPandas()
            self.user_solution = self.user_solution.round(12)
            self.prepare_dataframes_spark()
            self.display_buttons()

    def user_input_of_correct_datatype(self, solution):
        """Checks if the user passed a PySpark dataframe. Otherwise a message is
        displayed to inform the user that the input is of the wrong datatype.

        Parameters
        ----------
        solution: object
            solution that the user passed to the task evaluation

        Return
        ----------
        boolean
            if the user input is of correct datatype

        """
        if isinstance(solution, DataFrame):
            return True
        else:
            print('Als Eingabe wird ein PySpark DataFrame erwartet.')
            return False

    def prepare_dataframes_spark(self):
        for name in self.solution.columns.values:
            if name in self.user_solution.columns.values:
                # check if solution column has to be converted to datetime
                if self.user_solution[name].dtype == 'datetime64[ns]':
                    try:
                        self.solution[name] = pd.to_datetime(
                            self.solution[name])
                    except Exception:
                        pass
                # check if user solution column is of type category
                if self.user_solution[name].dtype.name == 'int32':
                    try:
                        self.solution[name] = self.solution[name].astype('int32')
                    except Exception:
                        pass
