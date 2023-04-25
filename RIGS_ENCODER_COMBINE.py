import sys
import string
import gclib
import time
import matplotlib.pyplot as plt
import csv
import numpy as np

analog_values1 = []
counts1 = []

# Running Galil Motor
def main():
    g = gclib.py() #make an instance of the gclib python class
    try:
        print('gclib version:', g.GVersion())
        ###########################################################################
        #  Connect
        ###########################################################################
        g.GOpen('10.221.61.7 -s ALL')
        #g.GOpen('COM1')
        print(g.GInfo())
        ###########################################################################
        # Program
        ###########################################################################
        c = g.GCommand #alias the command callable
        c('DP 0') #set position to 0
        c('AB') #abort motion and program
        c('MO') #turn off all motors
        c('SHA') #servo A
        c('SPA=1000000')
        c('PRA=72000') #relative move
        c('AQ 1,1')
        print(' Starting move...')
        counts = [] # list to store counts
        analog_values = [] # list to store corresponding analog values
        c('BGA') #begin motion
        while True:
            if '1' in c("MG _BGA"):
                data = c("MG @AN[1]")
                data = float(data.strip())*1000
                
                counts.append(int(float(c("MG _TPA"))))
                counts1.append(int(float(c("MG _TPA"))))
                
                analog_values.append(int(float(data)))
                analog_values1.append(int(float(data)))
            else:
                break
        print(' done.')
        del c #delete the alias
        # plot analog values versus counts
        plt.plot(counts, analog_values)
        plt.xlabel('Counts')
        plt.ylabel('Analog Values')
        plt.title('Analog Values vs Counts')
        plt.show()
        np.savetxt('analog_values_vs_counts.csv', np.column_stack((counts1, analog_values1)), delimiter=',') # save csv file

    ###########################################################################
    # except handler
    ###########################################################################  
    except gclib.GclibError as e:
        print('Unexpected GclibError:', e)
    finally:
        g.GClose() #don't forget to close connections!
    return

#runs main() if example.py called from the console
if __name__ == '__main__':
    main()
