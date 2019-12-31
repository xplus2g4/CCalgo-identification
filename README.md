# Identification of rate-base congestion control algorithms

## Prerequisite

* [BBR](https://queue.acm.org/detail.cfm?id=3022184)
* [PCC-Vivace](https://github.com/PCCproject/PCC-Uspace)
* [Copa](https://github.com/venkatarun95/genericCC)
* iperf3

## Sender

In `localize_bottleneck.sh`, update `test_${algo}()` methods with the path to each CC algorithms. \\
In main method of `process.py`, switch between `processSingle()` and `processMultiple()` depending on the need.
