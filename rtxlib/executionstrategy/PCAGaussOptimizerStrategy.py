from colorama import Fore
from skopt import gp_minimize

from rtxlib import info
from rtxlib.execution import experimentFunction


# 1. do a stepExplorer to evaluate the feature area
# 2. do a PCA on the result data / store a pca_result.txt
# 3. do a step explorer using ([1,0] * PCA) * (StepRanges)

def start_pca_gauss_optimizer_strategy(wf):
    """ executes a self optimizing strategy """
    info("> ExecStrategy   | PCAGauss", Fore.CYAN)
    wf.totalExperiments =500

    # we look at the ranges the user has specified in the knobs
    knobs = wf.execution_strategy["knobs"]
    # we create a list of variable names and a list of knob (from,to)
    variables = []
    range_tuples = []
    # we fill the arrays and use the index to map from gauss-optimizer-value to variable
    for key in knobs:
        variables += [key]
        range_tuples += [(knobs[key][0][0], knobs[key][0][1])]
    # we give the minimization function a callback to execute
    # it uses the return value (it tries to minimize it) to select new knobs to test
    optimizer_result = gp_minimize(lambda opti_values: self_optimizer_execution(wf, opti_values, variables),
                                   range_tuples, n_calls=wf.totalExperiments, n_random_starts=450)
    # optimizer is done, print results
    info(">")
    info("> OptimalResult  | Knobs:  " + str(recreate_knob_from_optimizer_values(variables, optimizer_result.x)))
    info(">                | Result: " + str(optimizer_result.fun))


def recreate_knob_from_optimizer_values(variables, opti_values):
    """ recreates knob values from a variable """
    knob_object = {}
    # create the knobObject based on the position of the opti_values and variables in their array
    for idx, val in enumerate(variables):
        knob_object[val] = opti_values[idx]
    return knob_object


def self_optimizer_execution(wf, opti_values, variables):
    """ this is the function we call and that returns a value for optimization """
    knob_object = recreate_knob_from_optimizer_values(variables, opti_values)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_results"] = wf.execution_strategy["ignore_first_n_results"]
    exp["sample_size"] = wf.execution_strategy["sample_size"]
    exp["knobs"] = knob_object
    return experimentFunction(wf, exp)
