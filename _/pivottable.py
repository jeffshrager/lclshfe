"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import pickle
import dash
from dash import html
import dash_pivottable

app = dash.Dash(__name__)
server = app.server

FOLDER = "fnc_ond_tanh_false_cog_false/1658732176.595285"

with open(f"results/{FOLDER}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
    runs = pickle.load(runs_dictionary_file)

    computed_data = []
    header_list = []
    for key in runs[0].keys():
        if key != "samples":
            if key != "save_type":
                header_list.append(key)
    computed_data.append(header_list)

    for run in runs:
        temp_comp_data = []
        for sample in range(len(run['samples']['samples'])):
            for key, value in run.items():
                if key != "samples":
                    if key != "save_type":
                        if isinstance(value, list):
                            if len(value) == len(run['samples']['samples']):
                                temp_comp_data.append(value[sample])
                            else:
                                temp_comp_data.append(value[0])
                        else:
                            temp_comp_data.append(value)
            computed_data.append(temp_comp_data)
            temp_comp_data = []


    app.layout = html.Div(
        dash_pivottable.PivotTable(
            data=computed_data,
            cols=["pq"],
            rows=["op_noticing_delay"],
            vals=["N"]
        )
    )

    if __name__ == "__main__":
        app.run_server(debug=True)
