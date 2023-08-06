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

Copyright (C) 2020-2021 Marco Esposito, Leonardo Picchiami.
"""

from typing import Dict
import random

from apricopt.model.Model import Model
from apricopt.simulation.SimulationEngine import SimulationEngine
from apricopt.solving.BlackBoxSolver import BlackBoxSolver


class MockUpSolver(BlackBoxSolver):

    def __init__(self):
        super().__init__()

    def solve(self, model: Model, H: float, sim_engine: SimulationEngine,
              solver_params: list) -> (Dict[str, float], float, float):
        min_obj = float("Inf")
        min_params = None
        for i in range(solver_params[0]):
            print(f"Iteration {i+1}")
            params = dict()
            for param in model.parameters.values():
                params[param.id] = random.uniform(param.lower_bound, param.upper_bound)
            print(f"Parameters: {params}")

            params_values_dict = params
            print(f"\nTrying with params: {params_values_dict}")
            model.set_params(params_values_dict)
            fast_constraints_eval_results = model.evaluate_fast_constraints(params_values_dict)
            fast_violated = False
            for fast_id, fast_value in fast_constraints_eval_results.items():
                if fast_value > 0:
                    fast_violated = True
                    print(f"Violated Fast Constraint: {fast_id} with value {fast_value}")
                    break
            sim_output: Dict[str, float]
            if fast_violated:
                print("Fast constraints not satisfied")
                sim_output = model.build_zero_sim_output()
            else:
                sim_output = sim_engine.simulate(model, H)

            bb_eval_output = dict(sim_output, **fast_constraints_eval_results)

            if not fast_violated:
                objective = bb_eval_output[model.objective.id]
                print(f"Objective value: {objective}")
                if objective <= min_obj:
                    min_obj = objective
                    min_params = params

        return min_params, min_obj, solver_params[0], solver_params[0], solver_params[0]
