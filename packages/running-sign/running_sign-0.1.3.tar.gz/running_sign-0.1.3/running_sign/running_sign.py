#interval - the interval time by second btw steps
#msg_pre - prefix for the sign
#msg_post - suffix for the sign
#max_num - the max length of sign
#pct - the percentage of the progress, 0-100
#scale - the scale to enlarge or shrink the sign length


import time

def running_sign_rotation(interval= 0, msg_pre="", msg_post="",\
    sign = ["\\", "|", "/", "-", "|", "/", "-"]): #sign rotation chars
    '''
    generator to show rotating indicator.
    parameter:
    interval: number, seconds of interval time between every frame of indicator.
    msg_pre: string, content will show before indicator.
    msg_post: string, conent will show after indicator.
    sign: list, symbols which will be showed sequentially.    
    '''
    while True:  #running no stop
        for i in range(len(sign)):   #iteration to show chars in sequence
            line = msg_pre + sign[i] + msg_post
            print(line, end="",flush = True)
            if interval > 0:
                time.sleep(interval)
            yield
            print('\b' * len(line), end="", flush = True)
            

def running_sign_progress(interval=0, msg_pre = "", msg_post="", sign=".",  max_num = 120):
    max_num = 120 if max_num > 120 else max_num   #limits max number of sign in row
    '''
    generator to show progress bar.
    parameter：
    interval: number, seconds of interval time between every frame of indicator.
    msg_pre: string, content will show before indicator.
    msg_post: string, conent will show after indicator.
    sign: string, symbols which will be showed in progress way.
    max_num: number, max numbers of sign in one bar progress.
    '''
    while True:  #running no stop
        for i in range(max_num): 
            line = msg_pre + (sign * i) + msg_post
            print("\r" + line, end="", flush = True)
            # print(dotline, end=msg, flush = True)
            # dotline += sign #increse the number of sign in line
            if interval > 0:
                time.sleep(interval)
            yield
            
            #clear the print line to avoid some wrong happens in end line
            #you can try by delete the below line to see what will happen, try it

            print("\r" + (" " * len(line)), end="", flush =True)



def running_sign(interval=0, msg_pre="", msg_post="", sign=None, max_num=120):
    if sign != None:
        return running_sign_progress(interval, msg_pre, msg_post, sign, max_num)
    else:
        return running_sign_rotation(interval, msg_pre, msg_post)
    '''
    funtion, as entrance of two above function.
    parameter: refer to parameters in above function.
    return: generator.
    '''
    
    
def running_pct(msg_pre="", msg_post="", sign="■", pct=50, scale=1):    
    progress_length = int(scale * 100)
    bar = sign * int(pct * progress_length /100)
    line = msg_pre + (('%-' + ('%d' %progress_length) + 's') %(bar)) + msg_post + ('%3d%%' %(pct))
    print("\r", " " * len(line), end="", flush = True)
    print("\r", line, end="", flush = True )
    '''
    function, show progress bar.
    parameter:
    msg_pre: string, content will show before indicator.
    msg_post: string, conent will show after indicator.
    sign: string, symbols which will be showed in progress way.
    pct: number, length of progress bar.
    scale: number, scale of progress bar, default = 1 while the length of progress bar is 100 which means 100 signs.
    '''
