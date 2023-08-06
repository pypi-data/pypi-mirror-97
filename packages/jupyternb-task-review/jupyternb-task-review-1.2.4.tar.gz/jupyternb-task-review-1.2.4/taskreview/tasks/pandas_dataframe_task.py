"""Module that contains class to create Pandas dataframe tasks."""

from IPython.core.display import display
try:
    import pandas as pd
except ModuleNotFoundError:
    pass

from taskreview.task import Task


class PandasDataframeTask(Task):
    """
    A class used to represent a dataframe task

    Methods
    -------
    interpret_solution_from_database(solution)
        Gets the solution dataframe from database
    check_solution(button)
        Checks the solution when the check button is clicked
    get_specific_error_evaluation()
        Get a specific evaluation of the given user solution
    check_num_cols_rows(shape_index)
        Check if number of rows and columns are correct
    check_col_names()
        Check if column names are correct
    get_num_equal_cols()
        Gets the amount of equal columns between user and db solution
    check_col_sorting()
        Check if columns are sorted correcty
    check_cell_content()
        Check if the content of cells is correct
    prepare_evaluation(df)
        Evaluates the task based on the submitted solution
    calculate_scored_points()
        Calculates points achieved in the task
    user_input_of_correct_datatype(solution)
        check if user input is of pandas dataframe or series datatype
    prepare_dataframes()
        Convert columns for dataframe comparison
    """

    def interpret_solution_from_database(self, solution):
        """Gets the data for the solution dataframe from database.

        Parameters
        ----------
        solution : string
            Query to get needed data from database

        Returns
        ----------
        pd.DataFrame
            solution to task
        """

        return self.db_conn.get_dataframe_from_query(solution)

    def check_solution(self, button):
        """Checks if the solution of the user is correct

        Parameters
        ----------
        button: Button
            Button that has been clicked to execute this method
        """
        self.prepare_dataframes()
        # reset_index(drop=True) needed as indexes from selected cells may
        # vary between user columns and solution columns
        if self.solution.equals(self.user_solution.reset_index(drop=True)):
            self.is_task_answered_correctly = True
            self.display_img_correct()
            self.display_disabled_buttons()
        else:
            self.get_specific_error_evaluation()

            # increment counter of tries
            self.cnt_false_answers.increment()

            if self.cnt_false_answers.get_value() >= 3:
                self.display_solution_btn()

    def get_specific_error_evaluation(self):
        """Gets a more speficic evaluation of the task if the user solution
        is not correct. Various things are evaluated: number of columns,
        number of rows, column names, sorting of columns, ...
        """

        # check number of cols
        num_cols_correct = self.check_num_cols_rows(1)
        # check the number of rows
        num_rows_correct = self.check_num_cols_rows(0)
        # check the column names
        col_names_correct = self.check_col_names()

        evaluation_txt = 'Leider ist die Eingabe nicht korrekt.\
            Bitte versuche es erneut!<br> Auswertung der Überprüfung:<ul>'

        if not num_cols_correct:
            evaluation_txt += '<li>Die Anzahl der Spalten \
                stimmt nicht.<br></li>'

        if not num_rows_correct:
            evaluation_txt += '<li>Die Anzahl der Zeilen \
                stimmt nicht.<br></li>'

        if not col_names_correct:
            evaluation_txt += '<li>Die Spaltennamen stimmen nicht.\
                <br></li>'

        if num_cols_correct and num_rows_correct and col_names_correct:
            # check sorting of columns
            col_sorting_correct = self.check_col_sorting()
            # check if the content of cells is correct
            cell_content_correct = self.check_cell_content()
            # check if cols are in the correct order
            col_order_correct = self.check_col_order()

            if not col_order_correct:
                evaluation_txt += '<li>Die Reihenfolge der Spalten \
                    stimmt nicht.<br></li>'
            if not col_sorting_correct:
                evaluation_txt += '<li>Die Sortierung der Spalten \
                    stimmt nicht.<br></li>'
            elif not cell_content_correct:
                evaluation_txt += '<li>Der Zellinhalt des DataFrames \
                    stimmt nicht.<br></li>'

        evaluation_txt += '<ul>'
        self.display_text(evaluation_txt)

    def check_num_cols_rows(self, shape_index):
        """Checks if the amount of rows and columns is correct

        Parameters
        ----------
        shape_index: int
          index of the rows (0) or the cols (1)

        Returns
        -------
        Boolean
          if the number of cols or rows of the user is correct
        """

        sol_num = self.solution.shape[shape_index]
        user_num = self.user_solution.shape[shape_index]

        return sol_num == user_num

    def check_col_names(self):
        """Checks if the column names of the user dataframe are correct

        Returns
        -------
        Boolean
          if the column names of the user dataframe are correct
        """

        sol_col_names = self.solution.columns.values
        user_col_names = self.user_solution.columns.values
        user_col_names_list = user_col_names.tolist()

        for name in user_col_names:
            if name in sol_col_names:
                user_col_names_list.remove(name)

        return not user_col_names_list

    def get_num_equal_cols(self):
        """Gets the number of equal cells between the user dataframe
        and the solution dataframe

        Returns
        -------
        int
          number of equal cells
        """

        correct_cols = 0
        for name in self.solution.columns.values:
            if name in self.user_solution.columns.values:
                # reset_index(drop=True) needed as indexes from selected
                # cells may vary between user columns and solution columns
                if self.user_solution[name].reset_index(drop=True).equals(
                        self.solution[name]):
                    correct_cols += 1

        return correct_cols

    def check_col_sorting(self):
        """Checks if the columns are sorted correctly

        Returns
        -------
        Boolean
          if the columns are sorted correctly
        """
        correct_cols = self.get_num_equal_cols()
        return correct_cols > (len(self.user_solution.columns) - correct_cols)

    def check_col_order(self):
        """Checks if the columns are in the correct order

        Returns
        -------
        Boolean
          if the columns are in the correct order
        """
        user_cols = self.user_solution.columns.values
        solution_cols = self.solution.columns.values
        equal_col_names = solution_cols == user_cols
        if False in equal_col_names:
            return False
        else:
            return True

    def check_cell_content(self):
        """Checks if the content of cells is correct

        Returns
        -------
        Boolean
          if the content of cells is correct
        """

        correct_cols = self.get_num_equal_cols()
        sol_col_names = self.solution.columns.values
        user_col_names = self.user_solution.columns.values

        wrong_col_names = len(sol_col_names)

        for name in sol_col_names:
            if name in user_col_names:
                wrong_col_names -= 1

        return (len(self.solution.columns) - correct_cols
                - wrong_col_names) == 0

    def prepare_evaluation(self, solution):
        """Makes it possible to evaluate the task by displaying the buttons.
        Display user solution. Series are converted to a dataframe.

        Parameters
        ----------
        df: pandas.DataFrame
          Dataframe that the user submitted
        """
        self.user_solution = solution

        if self.user_input_of_correct_datatype(solution):
            if isinstance(self.user_solution, pd.Series):
                self.user_solution = self.user_solution.to_frame().reset_index()
            display(solution)
            self.display_buttons()

    def user_input_of_correct_datatype(self, solution):
        """Checks if the user passed a pandas dataframe or series. Otherwise a
        message is displayed to inform the user that the input is of the wrong
        datatype.

        Parameters
        ----------
        solution: object
          solution that the user passed to the task evaluation

        Return
        ----------
        boolean
          if the user input is of correct datatype

        """
        if isinstance(solution, pd.DataFrame) or \
                isinstance(solution, pd.Series):
            return True
        else:
            print('Als Eingabe wird ein Pandas DataFrame oder eine Pandas \
Series erwartet.')
            return False

    def prepare_dataframes(self):
        """Tries to convert the columns of solution DataFrame to datetime
        datatypeif it is of datetime datatype in the user DataFrame.
        Important for comparison of the two dataframes. Datetime datatype
        is not exported from database therefore the two dataframes won't be
        equal due to different datatypes. The same applies to category datatype.
        Since the categories are not in the correct order, when a column is
        converted to category datatype, the category column of the user
        solution is converted to object.
        """
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
                if self.user_solution[name].dtype.name == 'category':
                    try:
                        self.user_solution[name] = self.user_solution[
                            name].astype(object)
                    except Exception:
                        pass
