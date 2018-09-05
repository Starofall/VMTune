name = "PCA-Test"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    # "type": "pca_gauss",
    "type": "step_explorer",
    "knobs": {
        "a": ([1.0, 100.0], 30.0),
        "b": ([1.0, 100.0], 30.0),
        "c": ([1.0, 100.0], 30.0),
        "d": ([1.0, 100.0], 30.0),
        "e": ([1.0, 100.0], 30.0),
        "f": ([1.0, 100.0], 30.0),
        "g": ([1.0, 100.0], 30.0)
    }
}


def evaluator(resultState, wf):
    return resultState["result"]


def state_initializer(state, wf):
    state["result"] = 999999999
    return state


def primary_data_reducer(state, newData, wf):
    state["result"] = newData["result"]
    return state


currentConfiguration = {
    "x": 0,
    "y": 0,
    "z": 0,
}


def setParameterHook(params):
    currentConfiguration.update(params)


def getResultsHook():
    a = currentConfiguration["a"]
    b = currentConfiguration["b"]
    c = currentConfiguration["c"]
    d = currentConfiguration["d"]
    e = currentConfiguration["e"]
    f = currentConfiguration["f"]
    g = currentConfiguration["g"]
    return {
        "result": (a * a - d) + (b * e * g * g) + (f - c) - (a * g * f) + 0.1
    }


change_provider = {
    "type": "local_hook",
    "setParameterHook": setParameterHook,
}

primary_data_provider = {
    "type": "local_hook",
    "data_reducer": primary_data_reducer,
    "getResultsHook": getResultsHook
}
