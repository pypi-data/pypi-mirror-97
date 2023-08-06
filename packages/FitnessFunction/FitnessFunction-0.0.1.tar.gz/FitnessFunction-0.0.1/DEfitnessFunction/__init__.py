def elliptic_function(x_array):
    a = 0
    D = 5
    for i in range(len(x_array)):
        a = a + pow(pow(10,6),(i-1)/(D-1))*(x_array[i]**2)
    return a

def schwefel_function(x_array):
    #schwefel function 1.2
    s = 0;sum1=0
    for i in range(len(x_array)):
        s = s + (x_array[i])
        sum1 = sum1 + (s**2)
    return sum1

 #schwefel function 2.22
def schwefel_fun(x_array):
    f=0;b=0;c=1
    for i in range(len(x_array)):
        b=b+ np.fabs(x_array[i])
        c=c* np.fabs(x_array[i])
    f=b+c
    return f
