name = "SingleRun-2b-Inlining-size"

# test different inlining sizes to search for the optimal value

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "step_explorer",
    "knobs": {
        "freqInlineSize": ([5, 1000], 5)
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
    "maxInlineLevel": 9,  # 5-15 Maximum number of nested calls that are inlined
    "maxInlineSize": 35,  # 10-150 Maximum bytecode size of a method to be inlined
    "freqInlineSize": 325,  # 200-500
    "maxRecursiveInlineLevel": 1,  # 0-3
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

