import time

def Elapsed_Time_Wrapper(function): 
        #this wraps the OBS functions to automaticly handle when OBS is not open.
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function(*args, **kwargs)
            end_time = time.time()
            print("Time Elapsed: ",end_time-start_time)
        return wrapper