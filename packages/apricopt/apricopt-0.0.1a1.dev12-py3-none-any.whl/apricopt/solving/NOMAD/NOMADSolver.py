"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020 Marco Esposito, Leonardo Picchiami.
"""

import time
from typing import List, Dict, Set, Callable
import PyNomad

from apricopt.model.Model import Model
from apricopt.model.Observable import Observable
from apricopt.simulation.SimulationEngine import SimulationEngine
from apricopt.solving.BlackBoxSolver import BlackBoxSolver


def build_bounds_x0_granularity_lists(m: Model) -> (list, list, list):
    lower_bounds: List[float] = [0] * len(m.parameters)
    upper_bounds: List[float] = [0] * len(m.parameters)
    x0: List[float] = [0] * len(m.parameters)

    params_ids: List[str] = [p_id for p_id in m.parameters]
    params_ids.sort()

    granularity_string = "("

    for p_idx in range(len(params_ids)):
        lower_bounds[p_idx] = m.parameters[params_ids[p_idx]].lower_bound
        upper_bounds[p_idx] = m.parameters[params_ids[p_idx]].upper_bound
        x0[p_idx] = m.parameters[params_ids[p_idx]].nominal_value
        granularity_string += " " + str(m.parameters[params_ids[p_idx]].granularity)

    granularity_string += ")"

    return lower_bounds, upper_bounds, x0, granularity_string

'''
def build_output_type_string(m: Model) -> str:
    obj = "OBJ"
    eb = " ".join(["EB"] * (len(m.fast_constraints) + len(m.hard_constraints)))
    pb = " ".join(["PB"] * len(m.feasibility_constraints))
    return f"{obj} {eb} {pb}"
'''

def build_output_type_string(m: Model) -> str:
    obj = "OBJ"
    eb = " ".join(["EB"] * (len(m.fast_constraints) + len(m.constraints)))
    pb = " ".join(["PB"] * len(m.feasibility_constraints))
    return f"{obj} {eb} {pb}"


def build_params_value_dict(m: Model, eval_point: PyNomad.PyNomadEvalPoint) -> Dict[str, float]:
    params_values: List[float] = [eval_point.get_coord(i) for i in range(eval_point.size())]
    return build_params_value_dict_from_list(m, params_values)


def build_params_value_dict_from_list(m: Model, params_values: List[float]) -> Dict[str, float]:
    params_ids: List[str] = [p_id for p_id in m.parameters]
    params_ids.sort()

    values_dict: Dict[str, float] = dict()

    for idx in range(len(params_ids)):
        values_dict[params_ids[idx]] = params_values[idx]

    return values_dict

'''
def build_output_string(m: Model, sim_output: Dict[str, float]) -> str:
    obj = str(sim_output[m.objective.id])

    fast_constraints_str = build_type_observable_string(m.fast_constraints, sim_output)
    hard_constraints_str = build_type_observable_string(m.hard_constraints, sim_output)
    feas_constraints_str = build_type_observable_string(m.feasibility_constraints, sim_output)

    return f"{obj} {fast_constraints_str} {hard_constraints_str} {feas_constraints_str}"
'''

def build_output_string(m: Model, sim_output: Dict[str, float]) -> str:
    obj = str(sim_output[m.objective.id])

    fast_constraints_str = build_type_observable_string(m.fast_constraints, sim_output)
    constraints_str = build_type_observable_string(m.constraints, sim_output)
    feas_constraints_str = build_type_observable_string(m.feasibility_constraints, sim_output)

    return f"{obj} {fast_constraints_str} {constraints_str} {feas_constraints_str}"


def build_type_observable_string(model_obs: Set[Observable],
                                 sim_output: Dict[str, float]) -> str:
    obs_ids: List[str] = [fo.id for fo in model_obs]
    obs_ids.sort()
    c: List[str] = list()
    for idx in range(len(model_obs)):
        c.append(str(sim_output[obs_ids[idx]]))
    fast_c_str: str = " ".join(c)
    return fast_c_str


class NOMADSolver(BlackBoxSolver):

    def __init__(self):
        super().__init__()

    '''
    def build_bb_function(self, m: Model, H: float, sim_engine: SimulationEngine,
                          output_type_string: str) -> Callable:
        def bb(x, dict_given=False) -> int:

            eval_ok = 1
            try:
                if not dict_given:
                    params_values_dict = build_params_value_dict(m, x)
                # print(f"\nTrying with params: {params_values_dict}")
                else:
                    params_values_dict = x
                m.set_params(params_values_dict)
                fast_constraints_eval_results = m.evaluate_fast_constraints(params_values_dict)
                fast_violated = False
                for fast_id, fast_value in fast_constraints_eval_results.items():
                    # self.fast_constraints_values[fast_id].append(fast_value)
                    if fast_value > 0:
                        fast_violated = True
                sim_output: Dict[str, float]
                if fast_violated:
                    sim_output = m.build_zero_sim_output()
                    # for fc in m.feasibility_constraints:
                    #     self.feasibility_constraints_values[fc.id].append(sim_output[fc.id])
                    # for hc in m.hard_constraints:
                    #    self.hard_constraints_values[hc.id].append(hc.id)
                    # self.objective_values.append(sim_output[m.objective.id])
                else:
                    
                    sim_output = sim_engine.simulate(m, H)
                            
                    line: str
                    for feasibility_constraint in m.feasibility_constraints:
                        # self.feasibility_constraints_values[feasibility_constraint.id].append(
                        #     sim_output[feasibility_constraint.id])
                        line = f"\tFeasibility Constraint '{feasibility_constraint.name}' value: {sim_output[feasibility_constraint.id]}"
                        # self.log.append(line)
                        print(line, flush=True)
                    for hard_constraint in m.hard_constraints:
                        # self.hard_constraints_values[hard_constraint.id].append(sim_output[hard_constraint.id])
                        line = f"\tHard Constraint '{hard_constraint.name}' value: {sim_output[hard_constraint.id]}"
                        # self.log.append(line)
                        print(line, flush=True)

                    # self.objective_values.append(sim_output[m.objective.id])
                    line = f"\tObjective value: {sim_output[m.objective.id]}"
                    # self.log.append(line)
                    print(line, flush=True)
                bb_eval_output = dict(sim_output, **fast_constraints_eval_results)

                x.setBBO(build_output_string(m, bb_eval_output)
                         .encode("UTF-8"), output_type_string.encode("UTF-8"))

                # self.times.append(time.perf_counter() - self.start_time)
                # return 1
            except:
                eval_ok = 0
                sim_output = dict()
                fast_constraints_eval_results = dict()
                fast_violated = False
                # self.times.append(time.perf_counter() - self.start_time)
                # return 0

            if eval_ok == 1:
                self.execution_info(m, sim_output, fast_constraints_eval_results, fast_violated)
    
            return eval_ok
        return bb

    def initialize_storage(self, model: Model) -> None:
        super().initialize_storage(model)
        self.start_time = time.perf_counter()
        
        
    def execution_info(self, m: Model, sim_output: Dict[str, float], fast_constraints_eval_results, fast_violated: bool):
        line: str
        for fast_id, fast_value in fast_constraints_eval_results.items():
            self.fast_constraints_values[fast_id].append(fast_value)
        for fc in m.feasibility_constraints:
            self.feasibility_constraints_values[fc.id].append(sim_output[fc.id])
            if not fast_violated:
                line = f"\tFeasibility Constraint '{fc.name}' value: {sim_output[fc.id]}"
                self.log.append(line)
        for hc in m.hard_constraints:
            if fast_violated:
                self.hard_constraints_values[hc.id].append(hc.id)
            else:
                self.hard_constraints_values[hc.id].append(sim_output[hc.id])
                line = f"\tHard Constraint '{hc.name}' value: {sim_output[hc.id]}"
                self.log.append(line)
                
        self.objective_values.append(sim_output[m.objective.id])
            
        if not fast_violated:
            line = f"\tObjective value: {sim_output[m.objective.id]}"
            self.log.append(line)
            
        self.times.append(time.perf_counter() - self.start_time)
    '''
    
    def solve(self, m: Model, H: float, sim_engine: SimulationEngine,
              solver_params: list, bb_function: Callable) -> (Dict[str, float], float, float):
        lower_bounds, upper_bounds, x0, granularity_string = build_bounds_x0_granularity_lists(m)
        output_type_string = build_output_type_string(m)

        #self.initialize_storage(m, H)
        #self.initialize_storage(m)
    
        bb = bb_function(m, H, sim_engine, output_type_string)

        solve_parameters = solver_params[:]
        solve_parameters.append(f"BB_OUTPUT_TYPE {output_type_string}")
        solve_parameters.append(" GRANULARITY " + granularity_string)

        print(f"NOMAD parameters: {solve_parameters}", flush=True)

        
        [x_return, f_return, h_return, nb_evals, nb_iters, stopflag] = \
            PyNomad.optimize(bb, x0, lower_bounds, upper_bounds, solve_parameters)
        
        optimal_params = build_params_value_dict_from_list(m, x_return)
        
        return optimal_params, f_return, h_return, nb_evals, nb_iters
