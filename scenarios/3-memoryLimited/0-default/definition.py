name = "LowVariance-0-Default"

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "step_explorer",
    "knobs": {
        "irrelevant": ([1, 20], 1)
    }
}

def evaluator(resultState, wf):
    return resultState["totalTime"]


def state_initializer(state, wf):
    state["totalTime"] = 999999999
    return state


def primary_data_reducer(state, newData, wf):
    if (state["totalTime"] > newData["totalTime"]):
        state["totalTime"] = newData["totalTime"]
    return state


currentConfiguration = {
    "scenarioIdentifier": "memoryLimited",
    "scenarioCommand": " -t 1 -n 10 ",
    "scalaBenchTest": "sunflow",
    "scalaBenchSize": "small",
    "javaDir": "./graalvm/bin/java",
    "scalaBenchFile": "./scalabench.jar",
    "debugEnabled": 0,
    "codeCacheSize": "2M", # !!! ONLY 2 MB of memory!
    "heapSize": "2G",
    "graalCompilerEnabled": 0,
    "graalBootstrapEnabled": 0,
    "compileHugeMethodsEnabled": 0,
    "aggressiveOptEnabled": 0,
    "codeFlushingEnabled": 1,
    "counterDecayEnabled": 1,
    "tieredCompilationEnabled": 1,  #
    "backgroundCompilationEnabled": 0,  # default is on, but introduces multi-threading variance
    "loopMaxUnroll": 16,  # 10-20
    "loopMinUnroll": 4,  # 2-10
    "loopUnrollLimit": 60,  # 40-80
    "minInliningThreshold": 250,  # Minimum invocation count a method needs to have to be inlined
    "inlineSmallCode": 2000,  # 500-5000
    "maxInlineSize": 35,  # 10-150 Maximum bytecode size of a method to be inlined
    "freqInlineSize": 325,  # 200-500
    "maxRecursiveInlineLevel": 1,  # 0-3
    "maxInlineLevel": 9,  # 5-15 Maximum number of nested calls that are inlined
    "compileThreshold": 10000,  # 2000-50000
    "onStackReplacePercentage": 933,  # 144-993  # method invocations (percentage of CompileThreshold) before compiling
    "tier4BackEdgeThreshold": 40000,  #
    "tier4CompileThreshold": 15000,  # 5000-50000
    "tier4InvocationThreshold": 5000,  #
    "tier4MinInvocationThreshold": 600,  #
    "tier3BackEdgeThreshold": 60000,  #
    "tier3CompileThreshold": 2000,  # 5000-50000
    "tier3InvocationThreshold": 200,  #
    "tier3MinInvocationThreshold": 100,  #
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
