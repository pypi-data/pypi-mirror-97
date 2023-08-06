This package contains different types of tasks which can be used to create tests in Jupyter Notebooks. The task review is always initiated by the learner by pushing a button.

## Examples:
![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/sc_task.png)

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/task_df_overview.png)

## Buttons and task review
Every task uses buttons for interaction. There is always an evaluation button ("Auswertung") and also a solution button ("L&ouml;sung") that becomes just visible after three false answers.
Depending on the task type there may also be a hint button ("Tipp") which was left off when creating single and multiple choice tasks.
The Package also contains functionality to calculate a score out of all the tasks in a notebook.
After the solution has been submitted correctly, the buttons are deactivated and a green check mark appears.

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/9da1ef9f5ffe6656f6ee11ac2ff4c295612e9f62/PyPi-Taskreview-Readme-Images/buttons_before.png)

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/buttons_with_solution.png)

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/buttons_after.png)

At the end a total score can be determined. To start calculating the score the submit button ("Auswertung") has to be displayed. The calculation counts all the points the user got while solving the tasks and maps it to 100%. How this is done is described below.

For dataframe tasks the user can achieve a maximum of 3 points and a minimum of 0 points.

points | correctly solved? | solution not viewed? | less than 3 tries?
------ | ------ | ------ | ------
0 | - | - | -
1 | X | - | -
2 | X | X | -
3 | X | X | X

For single and multiple chocie tasks a user can achieve a maximum of 2 points and a minimum of 0 points.

points | correctly solved? | less than 3 tries?
------ | ------ | ------
0 | - | -
1 | X | -
2 | X | X

After the respective task has been evaluated and the points have been calculated, this point value is normalized to a range from 0 to 1. Because of that all tasks can be treated the same when calculating the overall score.

## Tasks Types
There are four types of tasks that can be created with the modules inside this package: single choice, multiple choice and Pandas and Spark dataframe tasks. DataFrame tasks are tasks where the user/ learner creates a dataframe depending on a specific task and this dataframe is hand over to the task, where it is checked in comparison with a desposited dataframe. When the dataframe does not correspond to the solution it is also checked what is wrong with the dataframe (number of columns, number of rows, sorting of columns, content of cell, labeling of rows).

Examples for tasks:

DataFrame Pandas:

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/pandas_dataframe_task.png)

Single Choice:

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/single_choice_task.png)

Multiple Choice:

![image](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse/-/raw/add-images-for-pypi-readme/PyPi-Taskreview-Readme-Images/multiple_choice_task.png)

## How to implement and add tasks?
To create tasks for a jupyter notebook you just have to create a sqllite database that contains all the information necessary to automatically create the tasks.
The task database table has to contain 5 columns:
- taskID(Integer, not null, unique): uniquely identifies a task, with this id the task can be called directly from inside the notebook
- taskType(Text, not null): SC, MC, DFP, DFS; assigns the task to predefined task types, ensures that the correct task review functionality is selected in the background
- tipp(Text): can be added optionally to provide guidance when solving a task (can be formatted by using HTML Tags)
- solutionForReview(Integer, not null): sulotion that is used when checking the task
- additionalInformation(Text, not null): SC/MC: this field saves the options that the user can choose from, PDF/SDF: to deposit a solution that can be shown when the solution button is pushed (can be formatted using HTML tags)

**SQL statement to create a task:**

`
INSERT INTO "table"
VALUES (taskID, 'taskType', 'tipp', 'solutionForReview', 'additionalInformation)`

**To review a dataframe task the solution dataframe has to be saved as a database table. To create this table you can use the library sqlite3 inside the notebook:**

`
import sqlite3
con = sqlite3.connect('data/database.db')
data.to_sql('table', con, index=False, if_exists="replace")`

## How to import and use the package?
To install the package you just have to use `pip install jupyternb-task-review`. Afterwards you have to import the package to your Jupyter Notebook and then create an instance of the class LearningModule. When creating this instance you must handover the filename of your task database. To create and show a specific task you can use the method show_task(task_id) that is called by the LarningModule instance. The task_id identifies which information should be taken from the task database.

Methods used inside the notebook (called by the learning module instance):
- show_task(taskID): creates and displays the single choice or multiple choice task with the given id
- show_task(taskID, dataframe): creates and displays the dataframe task with the given id; dataframe is the users solution
- display_submit_button(): initiates the score calculation
