"""
Distributed under my own will

Author: Severn Anderson
"""

import sys

def variable_print(line_by_line=False, to_file=False, full_output=False):
    def wrapper(func):  
        def wrapped_wrapper(*args, **kwargs):
            with debug_context(func.__name__):
                return_value = func(*args, **kwargs)
            return return_value
            print(locals())
        return wrapped_wrapper
    return wrapper

class debug_context():
    """ 
    Debug context to trace any function calls inside the context manager.
    :param function_name: str, needed to grab the correct trace calls
    :param line_by_line: bool, if True it gives the variable values at each call
    :param to_file: bool, if True it writes results to a file
    :param full_output: bool, if True it writes line by line trace to file
    """

    def __init__(self, function_name, line_by_line=False, to_file=False, full_output=False):
        self.name = function_name
        self.line_logs = []
        self.line_by_line = line_by_line
        self.full_output = []
        self.full_detail = full_output
        self.to_file = to_file

    def __enter__(self):
        print('Starting Decorated Function')
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
        
        output_string = f'In {func_name} on {event} {line_no} locals: {local_vars}' 
        self.full_output.append(output_string + "\n")
        if self.line_by_line:
            print (output_string)
            
        
        self.line_logs.append(local_vars)
        
    def variable_analyasis(self):
        var_dict = self.line_logs[-1]
        write_log = []
        for key in var_dict:
            value = var_dict[key]
            if callable(value):
                line = f"{key} is a callable function"
            else:
                line = f"{key} = {value}"
            
            print(line)
            write_log.append(line + "\n")

        if self.to_file:
            with open(f"{self.name}_variables.txt", "w+") as var_txt:
                var_txt.write("Start Output: \n")
                if self.full_detail:
                    var_txt.writelines(self.full_output)
                else:
                    var_txt.writelines(write_log)

            






        
