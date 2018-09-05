#!/usr/bin/env bash
# -XX:+AggressiveOpts	\ # Turn on point performance compiler optimizations
# -XX:MaxInlineSize=300 \ # Maximum bytecode size of a method to be inlined.
# -XX:FreqInlineSize=500 \ # 	Maximum bytecode size of a frequently executed method to be inlined.
# -XX:CompileThreshold=100 \ # Number of method invocations/branches before compiling [-client: 1,500]
# -XX:+BootstrapJVMCI \ bootstraps graal compiler before running the jvm (high overhead!)
# -XX:+PrintInlining \
# -XX:+BootstrapJVMCI -XX:+EagerJVMCI \
#-XX:+EnableJVMCI -XX:+UseJVMCICompiler -Djvmci.Compiler=graal \

./graalvm/bin/java \
    -XX:-EnableJVMCI -XX:-UseJVMCICompiler \
    -XX:+UseSerialGC -XX:InitialCodeCacheSize=2G -XX:ReservedCodeCacheSize=2G -Xms4G -Xmx4G \
    -XX:+UnlockDiagnosticVMOptions -XX:+UnlockExperimentalVMOptions \
    -Dgraal.Timers=CompilationTime -Djvmci.InitTimer=true -XX:+PrintCompilation -XX:+CITime \
    -XX:-BackgroundCompilation -XX:CICompilerCount=1 \
    -XX:+AggressiveOpts	-XX:-DontCompileHugeMethods -XX:-UseCodeCacheFlushing \
    -XX:LoopMaxUnroll=64 -XX:LoopUnrollMin=1 \
    -XX:InlineSmallCode=15000 -XX:MaxInlineSize=15000 -XX:FreqInlineSize=15000 \
    -XX:MaxRecursiveInlineLevel=16 -XX:MaxInlineLevel=64 \
    -XX:CompileThreshold=10000 -XX:-UseCounterDecay \
    -XX:-TieredCompilation \
    -jar scalabench.jar -n 1 -s small sunflow