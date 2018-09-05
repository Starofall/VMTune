# VMTune
A project to apply RTX to JVM/GraalVM in order to find out optimal JVM startup parameters for given scenarios

### Introduction

The idea of the project is that we have different scenarios a JVM might 
run in and we want to optimize the JVMs startup parameters to tune the results.
 
The scenarios are to run a given code... 
1) as fast as possible (in JIT)
2) with minimum variance (no high spikes)
3) in a memory limited environment (compilation is limited)
4) as a batch that should finish fast (JVM startup & compilation included)

As there are many parameters on the JVM, we focus on those that are responsible for 
loop unrolling, code inlining and compilation thresholds. As this still is a high dimensional
optimization problem we want to use RTX with a ANOVA-Optimizer to find out relevant knobs fast
and optimize the scenario.


### Setup

1) Run `> sudo python setup.py` to install all python and JVM dependencies
2) Start a scenario like `> python start.py start scenarios/singleRun/1a-inlining-size`
