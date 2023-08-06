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

from unittest import TestCase, main

from apricopt.model.Model import Model
from apricopt.model.Observable import Observable
from apricopt.model.Parameter import Parameter
from apricopt.simulation.MockUp.MockUpSimulationEngine import MockUpSimulationEngine
from apricopt.solving.MockUp.MockUpSolver import MockUpSolver

class TestMockUp(TestCase):
    def test(self):
        sim_engine = MockUpSimulationEngine()
        model = Model(sim_engine, "", 0, 0, 1, observed_outputs=["output"])
        model.objective = Observable("output", "output", ["output"])
        parameter = Parameter("parameter", "parameter", lower_bound=0, upper_bound=1, nominal_value=0.5)
        model.set_parameter_space({parameter})
        solver = MockUpSolver()
        horizon = 1
        iterations = 1000
        min_params, min_obj, _, _, _ = solver.solve(model, horizon, sim_engine, [iterations])
        print(f"\n\n==================================\nSolution: {min_params}\nBest Objective Value: {min_obj}")


if __name__ == "__main__":
    main()
