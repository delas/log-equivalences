import time
import pm4py


def evaluation_trace_no(logA, logB):
    return len(logA) == len(logB)


def evaluation_complete(logA, logB):
    if len(logA) != len(logB):
        return False

    for trace in logA:
        case = trace.attributes["concept:name"]

        other_trace = []
        for trace2 in logB:
            if trace2.attributes["concept:name"] == case:
                other_trace = trace2
        if other_trace == []:
            return False
        if len(trace) != len(other_trace):
            return False
        if other_trace.attributes != trace.attributes:
            return False

        for i in range(0, len(trace)):
            e_1 = trace[i]
            e_2 = other_trace[i]
            if e_1["concept:name"] != e_2["concept:name"]:
                return False

    return True


def current_milli_time():
    return time.perf_counter_ns()


def monitor(eq_func, logA, logB):
    start_time = current_milli_time()
    eq_func(logA, logB)
    return current_milli_time() - start_time


for i in range(12):
    config = "c" + str(i + 1)
    print(config)
    log_orig = pm4py.read_xes("test-logs/log_" + config + "_original.xes.gz")
    log_s1 = pm4py.read_xes("test-logs/log_" + config + "_s1.xes.gz")
    print(monitor(evaluation_complete, log_orig, log_s1), end='\t')
    print(monitor(evaluation_trace_no, log_orig, log_s1))
    del log_s1
    log_s2 = pm4py.read_xes("test-logs/log_" + config + "_s2.xes.gz")
    print(monitor(evaluation_complete, log_orig, log_s2), end='\t')
    print(monitor(evaluation_trace_no, log_orig, log_s2))
    del log_s2
    log_s3 = pm4py.read_xes("test-logs/log_" + config + "_s3.xes.gz")
    print(monitor(evaluation_complete, log_orig, log_s3), end='\t')
    print(monitor(evaluation_trace_no, log_orig, log_s3))
    del log_s3
    log_s4 = pm4py.read_xes("test-logs/log_" + config + "_s4.xes.gz")
    print(monitor(evaluation_complete, log_orig, log_s4), end='\t')
    print(monitor(evaluation_trace_no, log_orig, log_s4))
    del log_s4
    log_s5 = log_orig
    print(monitor(evaluation_complete, log_orig, log_s5), end='\t')
    print(monitor(evaluation_trace_no, log_orig, log_s5))

