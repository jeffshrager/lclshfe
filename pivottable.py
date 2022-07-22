"""Dash"""
import pickle
import dash
from dash import html
import dash_pivottable

app = dash.Dash(__name__)
server = app.server

FOLDER = "op_delay1-7/1658207804.691573 copy"

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
