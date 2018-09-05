import re
import subprocess
import time
import statistics
# from tinydb import TinyDB


def runConfig(config):
    start = time.time()
    command = buildCommand(config)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    config["stdOut"] = process.stdout.read()
    config["stdErr"] = process.stderr.read()
    # print(config["stdOut"])
    # print(config["stdErr"])
    config["totalTime"] = time.time() - start
    parseResults(config)
    config["stdOut"] = None
    config["stdErr"] = None
    # db = TinyDB('./db.json')
    # db.insert(config)
    return config


def parseResults(result):
    try:
        result["compilationTime"] = float(
            re.search("Total compilation time\s*:\s*([0-9,]*) s", result["stdOut"]).group(1).replace(",", "."))
        result["compiledMethods"] = int(re.search("Total compiled methods\s*:\s*([0-9]*) methods", result["stdOut"]).group(
            1))
        result["compiledByteCodes"] = int(re.search("Total compiled bytecodes\s*:\s*([0-9]*) bytes",
                                                result["stdOut"]).group(1))
        result["nmethodCodeSize"] = int(re.search("nmethod code size\s*:\s*([0-9]*) bytes", result["stdOut"]).group(1))
        result["nmethodTotalSize"] = int(re.search(" nmethod total size\s*:\s*([0-9]*) bytes", result["stdOut"]).group(1))
    except:
        pass
    try:
        result["passedTime"] = int(re.search("PASSED in ([0-9]*) msec", result["stdErr"]).group(1))
    except:
        pass
    try:
        result["warmupTimes"] = []
        for match in re.finditer("completed warmup [0-9]* in ([0-9]*) msec", result["stdErr"]):
            result["warmupTimes"].append(int(match.group(1)))
    except:
        pass
    try:
        result["minimumWarmupTime"] = min(result["warmupTimes"])
        result["maximumWarmupTime"] = max(result["warmupTimes"])
        result["averageWarmupTime"] = statistics.mean(result["warmupTimes"])
        result["varianceWarmupTime"] = statistics.variance(result["warmupTimes"])
        result["medianWarmupTime"] = statistics.median(result["warmupTimes"])
    except:
        pass


def buildCommand(config):
    return __buildProcessPriority() + __buildJVMExecString(config) + config["scenarioCommand"] + __buildScalaBenchString(config)


def __buildProcessPriority():
    return "nice -n -20 "


def __buildJVMExecString(config):
    return config["javaDir"] + __buildOptionString(config) + " -jar " + config["scalaBenchFile"] + " "


def __buildScalaBenchString(config):
    return "-s " + config["scalaBenchSize"] + " " + config["scalaBenchTest"]


def __buildOptionString(config):
    javaOptions = ""
    javaOptions = javaOptions + " -XX:+UnlockDiagnosticVMOptions -XX:+UnlockExperimentalVMOptions "
    javaOptions = javaOptions + " -XX:+CITime -XX:+UseSerialGC "

    javaOptions = javaOptions + " -XX:InitialCodeCacheSize=" + str(config["codeCacheSize"]) + " "
    javaOptions = javaOptions + " -XX:ReservedCodeCacheSize=" + str(config["codeCacheSize"]) + " "
    javaOptions = javaOptions + " -Xms" + config["heapSize"] + " -Xmx" + str(config["heapSize"]) + " "
    javaOptions = javaOptions + " -XX:LoopMaxUnroll=" + str(config["loopMaxUnroll"]) + " "
    javaOptions = javaOptions + " -XX:LoopUnrollMin=" + str(config["loopMinUnroll"]) + " "
    javaOptions = javaOptions + " -XX:LoopUnrollLimit=" + str(config["loopUnrollLimit"]) + " "
    javaOptions = javaOptions + " -XX:InlineSmallCode=" + str(config["inlineSmallCode"]) + " "
    javaOptions = javaOptions + " -XX:MinInliningThreshold=" + str(config["minInliningThreshold"]) + " "
    javaOptions = javaOptions + " -XX:MaxInlineSize=" + str(config["maxInlineSize"]) + " "
    javaOptions = javaOptions + " -XX:MaxInlineLevel=" + str(config["maxInlineLevel"]) + " "
    javaOptions = javaOptions + " -XX:FreqInlineSize=" + str(config["freqInlineSize"]) + " "
    javaOptions = javaOptions + " -XX:MaxRecursiveInlineLevel=" + str(config["maxRecursiveInlineLevel"]) + " "
    javaOptions = javaOptions + " -XX:CompileThreshold=" + str(config["compileThreshold"]) + " "
    javaOptions = javaOptions + " -XX:OnStackReplacePercentage=" + str(config["onStackReplacePercentage"]) + " "
    javaOptions = javaOptions + " -XX:Tier4BackEdgeThreshold=" + str(config["tier4BackEdgeThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier4CompileThreshold=" + str(config["tier4CompileThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier4InvocationThreshold=" + str(config["tier4InvocationThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier4MinInvocationThreshold=" + str(config["tier4MinInvocationThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier3BackEdgeThreshold=" + str(config["tier3BackEdgeThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier3CompileThreshold=" + str(config["tier3CompileThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier3InvocationThreshold=" + str(config["tier3InvocationThreshold"]) + " "
    javaOptions = javaOptions + " -XX:Tier3MinInvocationThreshold=" + str(config["tier3MinInvocationThreshold"]) + " "
    javaOptions = javaOptions + " -XX:CompileThreshold=" + str(config["compileThreshold"]) + " "

    if (config["compileHugeMethodsEnabled"]):
        javaOptions = javaOptions + " -XX:-DontCompileHugeMethods "
    else:
        javaOptions = javaOptions + " -XX:+DontCompileHugeMethods "

    if (config["aggressiveOptEnabled"]):
        javaOptions = javaOptions + " -XX:+AggressiveOpts "
    else:
        javaOptions = javaOptions + " -XX:-AggressiveOpts "

    if (config["codeFlushingEnabled"]):
        javaOptions = javaOptions + " -XX:+UseCodeCacheFlushing "
    else:
        javaOptions = javaOptions + " -XX:-UseCodeCacheFlushing "

    if (config["counterDecayEnabled"]):
        javaOptions = javaOptions + " -XX:+UseCounterDecay "
    else:
        javaOptions = javaOptions + " -XX:-UseCounterDecay "

    if (config["tieredCompilationEnabled"]):
        javaOptions = javaOptions + " -XX:+TieredCompilation -XX:CICompilerCount=2"
    else:
        javaOptions = javaOptions + " -XX:-TieredCompilation -XX:CICompilerCount=1"

    if (config["backgroundCompilationEnabled"]):
        javaOptions = javaOptions + " -XX:+BackgroundCompilation "
    else:
        javaOptions = javaOptions + " -XX:-BackgroundCompilation "

    if (config["graalCompilerEnabled"]):
        javaOptions = javaOptions + " -XX:+EnableJVMCI -XX:+UseJVMCICompiler -Djvmci.Compiler=graal "
        if (config["graalBootstrapEnabled"]):
            javaOptions = javaOptions + " -XX:+BootstrapJVMCI -XX:+EagerJVMCI "
    else:
        javaOptions = javaOptions + " -XX:-EnableJVMCI -XX:-UseJVMCICompiler "

    if (config["debugEnabled"]):
        javaOptions = javaOptions + "-Dgraal.Timers=CompilationTime -XX:+PrintCompilation "

    return javaOptions
