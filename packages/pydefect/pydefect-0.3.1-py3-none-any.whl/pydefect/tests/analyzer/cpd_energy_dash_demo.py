# -*- coding: utf-8 -*-
#  Copyright (c) 2020 Kumagai group.
from pathlib import Path

from dash import Dash
from pydefect.analyzer.dash_components.cpd_energy_dash import CpdEnergyComponent
from pydefect.chem_pot_diag.chem_pot_diag import CpdPlotInfo
from pymatgen import loadfn
import dash_html_components as html
import crystal_toolkit.components as ctc

app = Dash()

cwd = Path(__file__).parent

cpd = loadfn(str(cwd / "chem_pot_diag.json"))
info = CpdPlotInfo(cpd)
perfect = loadfn(str(cwd / "NaCl_perf_calc_results.json"))
defects = [loadfn(str(cwd / "NaCl_Va_Na1_0" / "calc_results.json")),
           loadfn(str(cwd / "NaCl_Va_Na1_-1" / "calc_results.json"))]
defect_entries = [loadfn(str(cwd / "NaCl_Va_Na1_0" / "defect_entry.json")),
                  loadfn(str(cwd / "NaCl_Va_Na1_-1" / "defect_entry.json"))]
corrections = [loadfn(str(cwd / "NaCl_Va_Na1_0" / "correction.json")),
               loadfn(str(cwd / "NaCl_Va_Na1_-1" / "correction.json"))]

component = CpdEnergyComponent(info, perfect, defects, defect_entries, corrections)

# example layout to demonstrate capabilities of component
my_layout = html.Div([component.layout])

ctc.register_crystal_toolkit(app=app, layout=my_layout, cache=None)

#app.run_server(mode='inline')


if __name__ == "__main__":
    app.run_server(debug=True, port=8086)