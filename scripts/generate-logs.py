import threading
import _thread as thread

class generate_original(threading.Thread):

  def __init__(self, filename, traces, events, trace_attribute, event_attribute, execute_lock):
    threading.Thread.__init__(self)
    self.filename = filename
    self.traces = traces
    self.events = events
    self.trace_attribute = trace_attribute
    self.event_attribute = event_attribute
    self.execute_lock = execute_lock
  
  def run(self):
    try:
      log = open(self.filename, "w+")
      generate(log, self.traces, self.events, 10, 10)
      log.close()
    except ValueError:
        pass


class generate_s1(threading.Thread):

  def __init__(self, filename, traces, events, trace_attribute, event_attribute, execute_lock):
    threading.Thread.__init__(self)
    self.filename = filename
    self.traces = traces
    self.events = events
    self.trace_attribute = trace_attribute
    self.event_attribute = event_attribute
    self.execute_lock = execute_lock
  
  def run(self):
    try:
      log = open(self.filename, "w+")
      generate(log, self.traces - 1, self.events, 10, 10)
      log.close()
    except ValueError:
        pass


class generate_s2(threading.Thread):

  def __init__(self, filename, traces, events, trace_attribute, event_attribute, execute_lock):
    threading.Thread.__init__(self)
    self.filename = filename
    self.traces = traces
    self.events = events
    self.trace_attribute = trace_attribute
    self.event_attribute = event_attribute
    self.execute_lock = execute_lock
  
  def run(self):
    try:
      log = open(self.filename, "w+")
      generate(log, self.traces, self.events, 10, 10, True)
      log.close()
    except ValueError:
        pass


class generate_s3(threading.Thread):

  def __init__(self, filename, traces, events, trace_attribute, event_attribute, execute_lock):
    threading.Thread.__init__(self)
    self.filename = filename
    self.traces = traces
    self.events = events
    self.trace_attribute = trace_attribute
    self.event_attribute = event_attribute
    self.execute_lock = execute_lock
  
  def run(self):
    try:
      log = open(self.filename, "w+")
      generate(log, self.traces, self.events, 10, 10, False, True)
      log.close()
    except ValueError:
        pass


class generate_s4(threading.Thread):

  def __init__(self, filename, traces, events, trace_attribute, event_attribute, execute_lock):
    threading.Thread.__init__(self)
    self.filename = filename
    self.traces = traces
    self.events = events
    self.trace_attribute = trace_attribute
    self.event_attribute = event_attribute
    self.execute_lock = execute_lock

  def run(self):
    try:
      log = open(self.filename, "w+")
      generate(log, self.traces, self.events, 10, 10, False, False, True)
      log.close()
    except ValueError:
        pass







def generate(log, traces, events, trace_attribute, event_attribute, skip_last_event=False, different_attribute_trace=False, different_attribute_event=False):
  log.write("""<?xml version="1.0" encoding="UTF-8"?>
<log xes.version="1849.2016" xmlns="http://www.xes-standard.org" xes.creator="Fluxicon Disco">
<extension name="Concept" prefix="concept" uri="http://www.xes-standard.org/concept.xesext"/>
<classifier name="Activity" keys="concept:name"/>
""")
  for i in range(1,traces+1):
    log.write("<trace>\n")
    log.write("\t<string key=\"concept:name\" value=\"c_" + str(i) + "\"/>\n")
    for ta in range(1,trace_attribute+1):
      trace_attribute_value = "va_" + str(ta)
      if different_attribute_trace and i == traces and ta == trace_attribute:
        trace_attribute_value += "_changed"
      log.write("\t<string key=\"ta_" + str(ta) + "\" value=\"" + trace_attribute_value + "\"/>\n")
    for j in range(1,events+1):
      if skip_last_event and i == traces and j == events:
        break
      act_name = "e_" + str(i) + str(j)
      if different_attribute_event and i == traces and j == events:
          act_name += "_changed"
      log.write("\t<event>\n")
      log.write("\t\t<string key=\"concept:name\" value=\"" + act_name +  "\"/>\n")
      for ea in range(1, event_attribute+1):
        event_attribute_value = "va_" + str(ea)
        log.write("\t\t<string key=\"ea_" + str(ea) + "\" value=\"" + event_attribute_value + "\"/>\n")
      log.write("\t</event>\n")
    log.write("</trace>\n")
  log.write("</log>")
  return log


configurations = [
    ("c1",    100, 10),
    ("c2",   1000, 10),
    ("c3",  10000, 10),
    ("c4", 100000, 10),
    ("c5",    100, 50),
    ("c6",   1000, 50),
    ("c7",  10000, 50),
    ("c8", 100000, 50),
    ("c9",    100, 250),
    ("c10",  1000, 250),
    ("c11", 10000, 250),
    ("c12",100000, 250)
]

for c in configurations:
  name = c[0]
  no_traces = c[1]
  no_events = c[2]
  execute_lock = thread.allocate_lock()

  tr1 = generate_original("log_" + name + "_original.xes", no_traces, no_events, 10, 10, execute_lock)
  tr2 = generate_s1("log_" + name + "_s1.xes", no_traces, no_events, 10, 10, execute_lock)
  tr3 = generate_s2("log_" + name + "_s2.xes", no_traces, no_events, 10, 10, execute_lock)
  tr4 = generate_s3("log_" + name + "_s3.xes", no_traces, no_events, 10, 10, execute_lock)
  tr5 = generate_s4("log_" + name + "_s4.xes", no_traces, no_events, 10, 10, execute_lock)
  
  tr1.start()
  tr2.start()
  tr3.start()
  tr4.start()
  tr5.start()

  tr1.join()
  tr2.join()
  tr3.join()
  tr4.join()
  tr5.join()
