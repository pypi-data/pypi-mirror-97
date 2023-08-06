import time


prev  = time.time()
start = time.time()

def gt():
    global prev
    t = time.time()
    strD = "{:.3f} {:.3f} ".format(t,t - prev)
    prev = t
    return strD

def dt():
    global prev
    t = time.time()
    strD = "{:.3f} ".format(t - prev)
    prev = t
    return strD

def tfs():
    global start
    t = time.time()
    strD = "{:.3f} ".format(t - start)
    return strD