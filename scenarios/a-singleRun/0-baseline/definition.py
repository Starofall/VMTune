name = "SingleRun-0-Baseline"
# Testing 10 times the same thing just to see if sampleSize is enough to get reliable min values

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "step_explorer",
    "knobs": {
        "irrelevant": ([1, 10], 1)
    }
}


def evaluator(resultState, wf):
    return resultState["passedTime"]


def state_initializer(state, wf):
    state["passedTime"] = 999999999
    return state


def primary_data_reducer(state, newData, wf):
    if (state["passedTime"] > newData["passedTime"]):
        state["passedTime"] = newData["passedTime"]
    return state


currentConfiguration = {
    "scenarioIdentifier": "SingleRun",
    "scenarioCommand": " -t 1 -n 1 ",
    "scalaBenchTest": "sunflow",
    "scalaBenchSize": "default",
    "javaDir": "./graalvm/bin/java",
    "scalaBenchFile": "./scalabench.jar",
    "debugEnabled": 0,
    "codeCacheSize": "2G",
    "heapSize": "2G"
}


def setParameterHook(params):
    currentConfiguration.update(params)


def getResultsHook():
    from tunr.AutoTune import startAutoTune
    config = currentConfiguration.copy()
    return startAutoTune(config)


change_provider = {
    "type": "local_hook",
    "setParameterHook": setParameterHook,
}

primary_data_provider = {
    "type": "local_hook",
    "data_reducer": primary_data_reducer,
    "getResultsHook": getResultsHook
}
