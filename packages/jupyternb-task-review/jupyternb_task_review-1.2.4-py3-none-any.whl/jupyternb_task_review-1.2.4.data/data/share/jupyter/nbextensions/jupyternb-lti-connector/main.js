// Hides Element with css.
const hideElement = (element) => {
  element.style.position = 'absolute';
  element.style.clip = 'rect(1px, 1px, 1px, 1px)';
  element.style.overflow = 'hidden';
  element.style.width = '1px';
  element.style.height = '1px';
};

// Returns URL parameters as URLParameter object.
const getParams = () => new URL(window.location.href).searchParams;

// Executes cells with timeout to ensure kernel is properly loaded.
const executeCell = (cell, timeout = 1000) => {
  // Different timeouts needed because of race conditions
  window.setTimeout(() => {
    cell.execute();
  }, timeout);
};

// Content of submit score button.
const submitButton = `from ipywidgets import widgets, Button
import requests
btn = widgets.Button(description='Ergebnis absenden')

display(btn);

def submit_score(obj):
    try:
        if not endpoint or not uuid or not username:
            raise RuntimeError("Parameters missing");
        elif not lm:
            raise RuntimeError("LearningModule-Instance not as lm defined")

        score = lm.get_score();
        taskEvaluationString = lm.get_task_evaluation_string();
        response = requests.post(endpoint, data= {"uuid": uuid, "grade": score, "username": username, "details": taskEvaluationString })
        if response.status_code != 200:
            raise RuntimeError("Fehler beim Request: " + str(response.status_code))
    except RuntimeError as e:
        print(e)
    else:
        print("Durchführung erfolgreich abgegeben!")
btn.on_click(submit_score)`;

define([
  'base/js/namespace',
  'base/js/events',
],
  (Jupyter, events) => {
    // Selects needed cells, but just once to reduce method calls.
    const setup = () => {
      const codeCells = Jupyter.notebook.get_cells().filter((cell) => cell.cell_type === 'code');

      const hiddenCells = codeCells.filter((cell) => cell.get_text().startsWith('#hideCell'));
      const hiddenInputCells = codeCells.filter((cell) => cell.get_text().startsWith('#hideInput'));
      const submitButtonCell = codeCells.find((codeCell) => codeCell.get_text().startsWith('#submitButton'));

      return { hiddenCells, hiddenInputCells, submitButtonCell }
    }

    // Injects parameters as variables into jupyter notebook
    const injectParams = () => {
      getParams().forEach((value, key) => {
        const cell = Jupyter.notebook.insert_cell_above('code');
        cell.set_text(`${key} = ${value};`);

        hideElement(cell.element[0]);
        executeCell(cell, 1000);
      });
    };

    // Adds instructions to pass params and execute notebook on the local device.
    const addLocalExecutionCell = () => {
      let paramsAsString = '';

      getParams().forEach((value, key) => {
        paramsAsString = paramsAsString.concat(`${key} = ${value}\n`);
      });

      if (!paramsAsString) return;

      const cell = Jupyter.notebook.insert_cell_above('markdown');

      cell.set_text(`Kopiere diesen Code in die erste Zelle deines Notebooks und führe sie anschließend aus, wenn du das Notebook lokal in einem Docker Container ausführen möchtest([Anleitung](https://projectbase.medien.hs-duesseldorf.de/eild.nrw-module/lernmodul-datenanalyse#Docker-Lokal)):\n\`\`\`python\n${paramsAsString}\`\`\``);

      cell.render();
    };

    // hides and execute cells that start with #hideCell
    const hideAndExecuteHiddenCells = (hiddenCells) => {
      hiddenCells.forEach((cell) => {
        hideElement(cell.element[0]);
        executeCell(cell, 2000);
      });
    };

    // hides the dom-node with `input`-class and executes them: cells need to start with #hideInput
    const hideAndExecuteInputCells = (hiddenInputCells) => {
      hiddenInputCells.forEach((cell) => {
        hideElement(cell.element[0].querySelector('.input'));
        executeCell(cell, 3000);
      });
    };

    // Injects the submit button which sends the results to the lti-server
    const injectSubmitButton = (submitButtonCell) => {
      let cell = submitButtonCell;

      if (!cell) {
        cell = Jupyter.notebook.insert_cell_at_bottom('code');
      }

      cell.set_text(submitButton);

      hideElement(cell.element[0].querySelector('.input'));
      executeCell(cell, 4000);
    };

    // Methods called when Notebook is ready.
    const initialize = () => {
      const { hiddenCells, hiddenInputCells, submitButtonCell } = setup();

      // Execute methods after timeouts to have enough buffering to succeed.
      window.setTimeout(() => {
        injectParams();
        addLocalExecutionCell();
        hideAndExecuteHiddenCells(hiddenCells);
        hideAndExecuteInputCells(hiddenInputCells);
        injectSubmitButton(submitButtonCell);
      }, 3000);
    };

    // Initialization function listens on specific notebook states.
    function load_ipython_extension() {
      events.on('kernel_ready.Kernel', () => {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
          initialize();
        } else {
          events.on('notebook_loaded.Notebook', () => {
            initialize();
          });
        }
      });
    }

    return {
      load_ipython_extension,
    };
  });
