"""
Distributed under my own will

Author: Severn Anderson
"""

import sys

def variable_print(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        with debug_context(func.__name__):
            return_value = func(*args, **kwargs)
        return return_value
        print(locals())
    return wrapper

class debug_context():
    """ Debug context to trace any function calls inside the context """

    def __init__(self, name):
        self.name = name
        self.line_logs = []

    def __enter__(self):
        print('Entering Debug Decorated func')
        # Set the trace function to the trace_calls function
        # So all events are now traced
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        # Stop tracing all events
        sys.settrace = None
        self.variable_analyasis()
        
    def trace_calls(self, frame, event, arg): 
        # We want to only trace our call to the decorated function
        if event != 'call':
            return
        elif frame.f_code.co_name != self.name:
            return
        # return the trace function to use when you go into that 
        # function call
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # If you want to print local variables each line
        # keep the check for the event 'line'
        # If you want to print local variables only on return
        # check only for the 'return' event
        if event not in ['line', 'return']:
            return
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        local_vars = frame.f_locals
        print ('  {0} {1} {2} locals: {3}'.format(func_name, event, line_no, local_vars))
        self.line_logs.append(local_vars)
        
    def variable_analyasis(self):
        var_dict = self.line_logs[-1]
        write_log = []
        for key in var_dict:
            value = var_dict[key]
            if callable(value):
                line = f"{key} is a callable function"
            else:
                line = f"{key} ends at {value}"

            print(line)
            write_log.append(line + "\n")

        with open(f"{self.name}_variables.txt", "w+") as var_txt:
            var_txt.writelines(write_log)

            






        
