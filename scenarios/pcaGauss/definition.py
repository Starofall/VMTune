name = "PCAGauss"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "pcaGauss",
    "knobs": {
        "x": ([1, 100], 5), # ranges needed
        "y": ([1, 100], 5),
        "z": ([1, 100], 5)
    },
    "pcaExplainedVariance": 0.8,  # 80%
    "pca": [  # preconfigured PCA
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
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
    x = currentConfiguration["x"]
    y = currentConfiguration["y"]
    z = currentConfiguration["z"]
    return {
        "result": x + y + z
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
