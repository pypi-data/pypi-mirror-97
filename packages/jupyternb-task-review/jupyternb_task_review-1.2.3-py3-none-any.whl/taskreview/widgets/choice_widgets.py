"""Module that contains a class to create single and
multiple choice widgets"""

from IPython.core.display import display
from IPython.display import clear_output
from ipywidgets import widgets, Output


class ChoiceWidgets:
    """
    A class used to represent single choice widgets

    ...

    Attributes
    ----------
    options : list
        list of options to choose from when answering the question
    choice_btns : RadioButtons
        buttons to choose an answer


    Methods
    -------
    create_single_choice_buttons(options)
        Creates the single choice buttons
    create_multiple_choice_buttons(options)
        Creates the multiple choice buttons
    display_single_choice_buttons()
        Displays the single choice buttons
    display_multiple_choice_buttons()
        Displays the multiple choice buttons
    get_selected_options()
        Returns the selected options for multiple choice tasks
    """

    def __init__(self, options, single_choice=True):
        self.out_choice = Output()

        # information about task
        self.options = options

        # init buttons to choose from
        if single_choice:
            self.sc_btns = self.create_single_choice_buttons()
        else:
            self.mc_btns = self.create_multiple_choice_buttons()

    def create_single_choice_buttons(self, value=0):
        """Creates radio buttons with the passed options

        Parameters
        -------
        options : list
            list of options to create radio buttons from
        value : int
            represents the selected element of the options
            (preset to 0, first element is selected)

        Returns
        -------
        btns : Buttons
            radio buttons that can be used for a single choice task
        """
        radio_options = [(words, i)
                         for i, words in enumerate(self.options.values())]

        layout = widgets.Layout(width='auto', height='auto')

        btns = widgets.RadioButtons(
            options=radio_options,
            description='',
            disabled=False,
            indent=False,
            value=value,
            layout=layout
        )

        return btns

    def create_multiple_choice_buttons(self):
        """Creates Checkboxes with the answers for multiple choice questions

        Parameters
        -------
        options : list
            list of options to create radio buttons from

        Returns
        -------
        options_widget : VBox with Checkboxes
            Checkboxes in a VBox for display
        """
        layout = widgets.Layout(width='auto', height='auto')

        options_dict = {option: widgets.Checkbox(description=option,
                                                 indent=False, value=False,
                                                 layout=layout)
                        for option in self.options.values()}
        options = [options_dict[option] for option in self.options.values()]
        options_widget = widgets.VBox(options)

        return options_widget

    def display_single_choice_buttons(self):
        """Displays the single choice buttons
        """

        display(self.out_choice)

        with self.out_choice:
            clear_output()
            display(self.sc_btns)

    def display_multiple_choice_buttons(self):
        """Displays the multiple choice buttons
        """

        display(self.out_choice)

        with self.out_choice:
            clear_output()
            display(self.mc_btns)

    def get_selected_options(self):
        """Returns the selected options for multiple choice tasks
        """

        selected_options = [
            w.description for w in self.mc_btns.children if w.value]
        return selected_options
