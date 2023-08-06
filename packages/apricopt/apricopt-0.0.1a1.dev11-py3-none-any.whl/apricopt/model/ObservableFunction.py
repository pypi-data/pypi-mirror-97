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

from typing import List, Callable

def Identity(*args: List[float]) -> float:
    return LastValue(*args)


def LastValue(*args: List[float]) -> float:
    return args[0][-1]


def Average(*args: List[float]) -> float:
    if len(args[0]) == 0:
        return 0
    return sum(args[0]) / len(args[0])


def Min(*args: List[float]) -> float:
    return min(args[0])


def Max(*args: List[float]) -> float:
    return max(args[0])


def Sum(*args: List[float]) -> float:
    return sum(args[0])


def MaxDistanceFromLowerBound(*args: List[float]) -> float:
    value: List[float] = args[0]
    lowerBound: List[float] = args[1]

    return max(lowerBound[t] - value[t] for t in range(len(value)))


def MaxDistanceFromUpperBound(*args: List[float]):
    value: List[float] = args[0]
    upperBound: List[float] = args[1]

    return max(value[t] - upperBound[t] for t in range(len(value)))


def MaxDistanceFromBounds(*args: List[float]) -> float:
    value: List[float] = args[0]
    lowerBound: List[float] = args[1]
    upperBound: List[float] = args[2]

    return max(
        max(lowerBound[t] - value[t], value[t] - upperBound[t]) for t in range(len(value)))

def FinalDistanceFromUpperBound(*args: List[float]) -> float:
    value: float = args[0][-1]
    upperBound: float = args[1][-1]
    return value - upperBound

def CumSumSpikes(*args: List[float]):
    value: List[float] = args[0]

    cumsum: float = value[0]
    for t in range(1, len(value)):
        if value[t] > value[t - 1]:
            cumsum += value[t] - value[t - 1]
    return cumsum


def CumSumSpikesDistanceFromLowerBound(*args: List[float]) -> float:
    cumsum: float = CumSumSpikes(*args)
    return args[1][-1] - cumsum


def CumSumSpikesDistanceFromUpperBound(*args: List[float]) -> float:
    cumsum: float = CumSumSpikes(*args)
    return cumsum - args[1][-1]


def CumSumSpikesDistanceFromBounds(*args: List[float]) -> float:
    cumsum: float = CumSumSpikes(*args)
    return max(args[1][-1] - cumsum, cumsum - args[2][-1])


def MaxDifferenceInPeriod(*args: List[float]) -> float:
    value: List[float] = args[0]
    period_length: int = int(args[1][0])

    return max(value[t] - value[t - period_length - 1] for t in range(period_length, len(value)))


def MaxDifferenceInPeriodDistanceFromAbove(*args: List[float]) -> float:
    return MaxDifferenceInPeriod(*args) - args[2][0]


def MaxSpikesSumDifferenceInPeriodDistanceFromAbove(*args: List[float]) -> float:
    value: List[float] = args[0]
    period_length = args[1]
    upper_bound = args[2]

    cumsum: List[float] = [value[0]]
    for t in range(1, len(value)):
        if value[t] > value[t - 1]:
            cumsum[t] = value[t] - value[t - 1]
        else:
            cumsum[t] = value[t - 1]
    return MaxDifferenceInPeriodDistanceFromAbove(cumsum, period_length, upper_bound)


def IndexOfFirstGE(*args: List[float]) -> float:
    value: List[float] = args[0]
    lowerBound: List[float] = args[1]
    for t in range(len(value)):
        if value[t] >= lowerBound[t]:
            return t
    return len(value)


def IndexOfFirstGT(*args: List[float]) -> float:
    value: List[float] = args[0]
    lowerBound: List[float] = args[1]
    for t in range(len(value)):
        if value[t] > lowerBound[t]:
            return t
    return len(value)


def IndexOfFirstEQ(*args: List[float]) -> float:
    value: List[float] = args[0]
    target: List[float] = args[1]
    for t in range(len(value)):
        if value[t] == target[t]:
            return t
    return len(value)


def IndexOfFirstLE(*args: List[float]) -> float:
    value: List[float] = args[0]
    upperBound: List[float] = args[1]
    for t in range(len(value)):
        if value[t] <= upperBound[t]:
            return t
    return len(value)


def IndexOfFirstLT(*args: List[float]) -> float:
    value: List[float] = args[0]
    upperBound: List[float] = args[1]
    for t in range(len(value)):
        if value[t] < upperBound[t]:
            return t
    return len(value)


function_names = {"max": Max,
                  "min": Min,
                  "avg": Average, "mean": Average,
                  "maxdistancefrombounds": MaxDistanceFromBounds,
                  "maxdistancefromlowerbound": MaxDistanceFromLowerBound,
                  "maxdistancefromupperbound": MaxDistanceFromUpperBound,
                  "cumsumspikes": CumSumSpikes,
                  "maxdifferenceinperiod": MaxDifferenceInPeriod,
                  "maxdifferenceinperioddistancefromabove": MaxDifferenceInPeriodDistanceFromAbove,
                  "maxspikessumdifferenceinperioddistancefromabove": MaxSpikesSumDifferenceInPeriodDistanceFromAbove,
                  "indexoffirstge": IndexOfFirstGE,
                  "indexoffirstgt": IndexOfFirstGT,
                  "indexoffirsteq": IndexOfFirstEQ,
                  "indexoffirstle": IndexOfFirstLE,
                  "indexoffirstlt": IndexOfFirstLT,
                  "finaldistancefromupperbound": FinalDistanceFromUpperBound}

# function_names = dict(function_names, **user_function_names)


def getFunction(function_name: str) -> Callable:
    if function_name.lower() in function_names:
        return function_names[function_name.lower()]
    # return None
