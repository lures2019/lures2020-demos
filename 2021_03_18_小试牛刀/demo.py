def SIR_step(S,I,R,a,b):
    N = S + I + R
    S_next = S - (b / N) * S * I
    I_next = I + (b / N) * S * I  - a * I
    R_next = R + a * I
    return [S_next,I_next,R_next]



def simulate30months():
    a = 0.2
    b = 0.5
    c = 0.1
    S0 = 100000
    I0 = 100
    R0 = 0
    Is = []
    for i in range(11):
        S0,I0,R0 = SIR_step(S0,I0,R0,a,b)
        Is.append(I0)
    for i in range(11,31):
        b = 0.6
        S, I, R = SIR_step(S0, I0, R0, a, b)
        Is.append(I)
    return Is

Is = simulate30months()
for i in range(len(Is)):
    if i <= 20 and Is[i] >= 10000:
        print("The first month I exceeds 10,000 is month {}.".format(i))
        break
    else:
        if Is[i] < 10000:
            print("The first month drops below 10,000 is month {}.".format(i))
            break