name = "Fastest-1-Human"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 2,
    "type": "self_optimizer",
    "optimizer_method": "forest",
    "optimizer_iterations": 100,
    "optimizer_random_starts": 20,
    "knobs": {
        "compileHugeMethodsEnabled": (0, 1),  # 10-150 default 35 Maximum bytecode size of a method to be inlined
        "codeFlushingEnabled": (0, 1),  # 200-500 default 325
        "tieredCompilationEnabled": (0, 1),
        "loopMaxUnroll": (5, 50),
        "loopMinUnroll": (2, 50),
        "loopUnrollLimit": (5, 100),
        "minInliningThreshold": (5, 500)
    }
}


def evaluator(resultState, wf):
    return resultState["minimumWarmupTime"]


def state_initializer(state, wf):
    state["minimumWarmupTime"] = 999999999
    return state


def primary_data_reducer(state, newData, wf):
    if (state["minimumWarmupTime"] > newData["minimumWarmupTime"]):
        state["minimumWarmupTime"] = newData["minimumWarmupTime"]
    return state


currentConfiguration = {
    "scenarioIdentifier": "fastest",
    "scenarioCommand": " -t 1 -n 200 ",
    "scalaBenchTest": "sunflow",
    "scalaBenchSize": "small",
    "javaDir": "./graalvm/bin/java",
    "scalaBenchFile": "./scalabench.jar",
    "debugEnabled": 0,
    "codeCacheSize": "2G",
    "heapSize": "2G",
    "graalCompilerEnabled": 1,  # PREFLIGHT
    "graalBootstrapEnabled": 0,  # PREFLIGHT
    "counterDecayEnabled": 0,  # PREFLIGHT
    "backgroundCompilationEnabled": 0,  # PREFLIGHT
    "maxInlineSize": 100,  # PREFLIGHT
    "freqInlineSize": 4000,  # PREFLIGHT
    "compileThreshold": 18000,  # PREFLIGHT
    "inlineSmallCode": 2000,  # 500-5000 default 2000
    "onStackReplacePercentage": 933,  # 144-993  # method invocations (percentage of CompileThreshold) before compiling
    "maxRecursiveInlineLevel": 12,  # 0-3 default 1
    "maxInlineLevel": 15,  # 5-15 default 9 Maximum number of nested calls that are inlined
    #
    "compileHugeMethodsEnabled": 0,  # default false
    "codeFlushingEnabled": 1,  # default true
    "tieredCompilationEnabled": 1,  # default true
    "loopMaxUnroll": 16,  # 10-20 default 16
    "loopMinUnroll": 4,  # 2-10 default 4
    "loopUnrollLimit": 60,  # 40-80 default 60
    "minInliningThreshold": 250,  # default 250 Minimum invocation count a method needs to have to be inlined
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
