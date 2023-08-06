import numpy as np
import matplotlib.pyplot as plt

def orderTest(hvec,steps,solver,u0,uexact):
    errors = []
    for i,h in enumerate(hvec):
        u = u0.copy()
        for _ in range(steps[i]):
            u,hnew,h_suggest = solver.step(u,h)
            assert (hnew == h)
        errors.append(np.linalg.norm(u-uexact)/np.linalg.norm(uexact))
        solver.reset()
    return errors

def orderPlot(hvec,errors):
    
    m,c = np.polyfit(np.log(hvec),np.log(errors),1)
    pred = np.exp(m*np.log(hvec) + c)
    plt.plot(hvec,errors,'b',label='solver')
    plt.plot(hvec,pred,'r',label='fit of order {:.2f}'.format(m))
    plt.xlabel('h')
    plt.ylabel('error')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.gca().invert_xaxis()
    plt.legend(loc='upper right')



