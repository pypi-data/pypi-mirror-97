# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.
import re
from copy import deepcopy
from dataclasses import dataclass
from itertools import groupby, combinations
from typing import List, Dict, Optional, Tuple

import numpy as np
from pydefect.analyzer.band_edge_states import BandEdgeStates
from pydefect.analyzer.calc_results import CalcResults
from pydefect.corrections.abstract_correction import Correction
from pydefect.corrections.manual_correction import NoCorrection
from pydefect.input_maker.defect_entry import DefectEntry
from pymatgen.core import Element, IStructure
from scipy.spatial import HalfspaceIntersection
import dash_html_components as html


@dataclass
class SingleDefectEnergy:
    name: str
    charge: int
    energy: float
    correction: float

    @property
    def corrected_energy(self):
        return self.energy + self.correction


@dataclass
class DefectEnergy:
    name: str
    charges: List[int]
    energies: List[float]
    corrections: List[float]

    def stable_charges(self, ef_min, ef_max):
        return set(self.cross_points(ef_min, ef_max).charges)

    @property
    def corrected_energies(self):
        result = []
        for energy, correction in zip(self.energies, self.corrections):
            result.append(energy + correction)
        return result

    def cross_points(self, ef_min, ef_max, base_e=0.0):
        large_minus_number = -1e4
        half_spaces = []
        for charge, corr_energy in zip(self.charges, self.corrected_energies):
            half_spaces.append([-charge, 1, -corr_energy])

        half_spaces.append([-1, 0, ef_min])
        half_spaces.append([1, 0, -ef_max])
        half_spaces.append([0, -1, large_minus_number])

        feasible_point = np.array([(ef_min + ef_max) / 2, -1e3])

        hs = HalfspaceIntersection(np.array(half_spaces), feasible_point)
        boundary_points = []
        inner_cross_points = []
        for intersection in hs.intersections:
            x, y = np.round(intersection, 8)
            if ef_min + 0.001 < x < ef_max - 0.001:
                inner_cross_points.append([x - base_e, y])
            elif y > large_minus_number + 1:
                boundary_points.append([x - base_e, y])

        return CrossPoints(inner_cross_points, boundary_points)

    def transition_levels(
            self, base_e: float = 0.0) -> Dict[Tuple[int, int], float]:
        result = {}
        for (c1, e1), (c2, e2) in combinations(
                zip(self.charges, self.corrected_energies), 2):
            result[(c1, c2)] = - (e1 - e2) / (c1 - c2) - base_e
        return result

    def pinning_level(self,
                      base_e: float = 0.0
                      ) -> Tuple[Tuple[float, Optional[int]],
                                 Tuple[float, Optional[int]]]:
        """
        :param base_e: Reference to show the pinning level such as VBM.
        :return: ((Lower pinning, its charge), (Upper pinning, its charge))
        """
        lower_pinning, upper_pinning = float("-inf"), float("inf")
        lower_charge, upper_charge = None, None
        for charge, corr_energy in zip(self.charges, self.corrected_energies):
            if charge == 0:
                continue
            pinning = - corr_energy / charge
            if charge > 0 and pinning > lower_pinning:
                lower_pinning, lower_charge = pinning, charge
            elif pinning < upper_pinning:
                upper_pinning, upper_charge = pinning, charge
        return ((lower_pinning - base_e, lower_charge),
                (upper_pinning - base_e, upper_charge))

    def energy_at_ef(self, ef: float) -> Tuple[float, int]:
        """
        :return: (Lowest energy, its charge)
        """
        result_e, result_charge = float("inf"), None
        for charge, corr_energy in zip(self.charges, self.corrected_energies):
            energy = corr_energy + charge * ef
            if energy < result_e:
                result_e, result_charge = energy, charge
        return result_e, result_charge

    def __str__(self):
        lines = []
        for c, e, cor in zip(self.charges, self.energies, self.corrections):
            lines.append(f"{self.name:>10} {c:>4} {e:12.4f} {cor:12.4f}")
        return "\n".join(lines)


@dataclass
class CrossPoints:
    inner_cross_points: List[List[float]]
    boundary_points: List[List[float]]

    @property
    def all_sorted_points(self):
        return sorted(self.boundary_points + self.inner_cross_points,
                      key=lambda v: v[0])

    @property
    def t_all_sorted_points(self):
        return np.transpose(np.array(self.all_sorted_points)).tolist()

    @property
    def t_inner_cross_points(self):
        return np.transpose(np.array(self.inner_cross_points)).tolist()

    @property
    def t_boundary_points(self):
        return np.transpose(np.array(self.boundary_points)).tolist()

    @property
    def charges(self):
        result = []
        for i, j in zip(self.all_sorted_points[:-1], self.all_sorted_points[1:]):
            dx = j[0] - i[0]
            dy = j[1] - i[1]
            result.append(int(round(dy / dx)))
        return result

    @property
    def charge_list(self):
        charges = [None] + self.charges + [None]
        return list(zip(charges[:-1], charges[1:]))

    @property
    def annotated_charge_positions(self):
        result = {}
        for ((x1, y1), (x2, y2)), charge \
                in zip(zip(self.all_sorted_points[:-1],
                           self.all_sorted_points[1:]),
                       self.charges):
            result[charge] = [(x1 + x2) / 2, (y1 + y2) / 2]
        return result

    def __str__(self):
        lines = []
        for point in self.all_sorted_points:
            lines.append(f"{point[0]:12.4f} {point[1]:12.4f}")
        return "\n".join(lines)


def make_defect_energies(single_energies: List[SingleDefectEnergy]
                         ) -> List[DefectEnergy]:
    sorted_energies = sorted(single_energies, key=lambda x: x.name)
    result = []
    for _, grouped_energies in groupby(sorted_energies, lambda x: x.name):
        charges = []
        energies = []
        corrections = []
        for single_energy in grouped_energies:
            charges.append(single_energy.charge)
            energies.append(single_energy.energy)
            corrections.append(single_energy.correction)
        result.append(DefectEnergy(single_energy.name, charges, energies, corrections))
    return result


def make_energies(perfect: CalcResults,
                  defects: List[CalcResults],
                  defect_entries: List[DefectEntry],
                  corrections: List[Correction],
                  abs_chem_pot: Dict[Element, float],
                  allow_shallow: bool = True,
                  band_edges: List[BandEdgeStates] = None):

    single_energies = []
    for i, (d, e, c) in enumerate(zip(defects, defect_entries, corrections)):
        if allow_shallow is False:
            if band_edges and band_edges[i].is_shallow:
                continue
        single_energies.append(
            make_single_defect_energy(perfect, d, e, abs_chem_pot, c))
    return make_defect_energies(single_energies)


def make_single_defect_energy(perfect: CalcResults,
                              defect: CalcResults,
                              defect_entry: DefectEntry,
                              abs_chem_pot: Dict[Element, float],
                              correction: Optional[Correction] = NoCorrection()
                              ) -> SingleDefectEnergy:
    n_diffs = num_atom_differences(defect.structure, perfect.structure)
    energy = (defect.energy - perfect.energy
              + reservoir_energy(n_diffs, abs_chem_pot))
    return SingleDefectEnergy(defect_entry.name, defect_entry.charge, energy,
                              correction.correction_energy)


def reservoir_energy(diffs: Dict[Element, int],
                     abs_chem_pot: Dict[Element, float]) -> float:
    return sum([-diff * abs_chem_pot[elem] for elem, diff in diffs.items()])


def num_atom_differences(structure: IStructure,
                         ref_structure: IStructure) -> Dict[Element, int]:
    target_composition = structure.composition.as_dict()
    reference_composition = ref_structure.composition.as_dict()
    result = {}
    for k in set(target_composition.keys()) | set(reference_composition.keys()):
        n_atom_diff = int(target_composition[k] - reference_composition[k])
        if n_atom_diff:
            result[Element(k)] = n_atom_diff
    return result


def remove_digits(name):
    return ''.join([i for i in name if not i.isdigit()])


def only_digits(name):
    return ''.join([i for i in name if i.isdigit()])


elements = [str(e) for e in Element]


def defect_mpl_name(name):
    in_name, out_name = name.split("_")
    if in_name in elements:
        in_name = "{\\rm " + in_name + "}"
    elif in_name == "Va":
        in_name = "V"

    r_out_name = remove_digits(out_name)
    if r_out_name in elements:
        out_name = "{{\\rm " + r_out_name + "}" + only_digits(out_name) + "}"
    else:
        out_name = "{" + out_name + "}"

    return f"${in_name}_{out_name}$"


def defect_plotly_name(name):
    in_name, out_name = name.split("_")
    if in_name == "Va":
        in_name = "<i>V</i>"

    out_name = f"<sub>{out_name}</sub>"
    return f"{in_name}{out_name}"


def defect_plotly_full_name(fullname):
    in_name, out_name, charge = fullname.split("_")
    if in_name == "Va":
        in_name = "<i>V</i>"
    return f"{in_name}<sub>{out_name}</sub><sup>{charge}</sup>"


def defect_html_title_name(fullname):
    x = fullname.split("_")
    if len(x) == 2:
        in_name, out_name = x
    elif len(x) == 3:
        in_name, out_name, charge = x
    else:
        raise ValueError

    if in_name == "Va":
        in_name = html.I("V")
    else:
        in_name = html.Span(in_name)

    result = [in_name, html.Sub(out_name)]
    if len(x) == 3:
        result.append(html.Sup(charge))
    return result


def sanitize_defect_energies_for_plot(defect_energies: List[DefectEnergy],
                                      for_plotly: bool = False):
    result = []
    out_names = [e.name.split("_")[1] for e in defect_energies]

    for e in defect_energies:
        ee = deepcopy(e)
        in_name, out_name = e.name.split("_")
        r_out_name = remove_digits(out_name)
        out_name = r_out_name if f"{r_out_name}2" not in out_names else out_name
        if for_plotly:
            ee.name = defect_plotly_name("_".join([in_name, out_name]))
        else:
            ee.name = defect_mpl_name("_".join([in_name, out_name]))
        result.append(ee)

    return result


def slide_energy(defect_energies: List[DefectEnergy], base_level: float):
    result = []
    for e in defect_energies:
        ee = deepcopy(e)
        ee.energies = [e + base_level * c for e, c in zip(e.energies, e.charges)]
        result.append(ee)
    return result
