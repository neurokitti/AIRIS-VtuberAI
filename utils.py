import time

def Elapsed_Time_Wrapper(function): 
        #this wraps the OBS functions to automaticly handle when OBS is not open.
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function(*args, **kwargs)
            end_time = time.time()
            print("Time Elapsed: ",end_time-start_time)
        return wrapper

def get_from_txt(file_name):
        #returns a string from a text file.
        with open(file_name, 'r') as file:
            content = file.read()
        return content