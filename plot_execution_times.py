import subprocess
import string
import numpy as np
import sys
import matplotlib.pyplot as plt
import time


def timerun(program, args) :
    print('Starting timed execution of ' + program + ' with ' + str(len(args)) + ' arguments.')
    i = 1

    subprocess.Popen(['rm', 'runtimes.txt'], stdout=subprocess.PIPE)

    # Execute program, once for each n argument
    for n in args:

        # This was really annoying. Build the arguments to the time system call to the time command.
        # First of all, for whatever reason 'time' didn't work correctly with any arguments other than -p,
        # so I used /usr/bin/time instead. Since I could not figure out why the output of 'time' was not
        # coming back to stdin, I use the -o (output file) and -a (append) option to just output the real
        # execution time ( thats where '-f' and '%e' comes from ) to the file.
        #p = subprocess.Popen(['/usr/bin/time', '-o', 'runtimes.txt', '-a', '-f', '%e', './' + program, str(n)],
        #                     stdout=subprocess.PIPE)
        p = subprocess.Popen(['./' + program, str(n)], stdout=subprocess.PIPE)
        # Read back from stdin, print where we are
        output = p.communicate()[0]
        sys.stdout.write(str(i) + ':\tseq_nw(' + str(n) + ') = ' + str(output))
        i += 1
    print('done')

    # Open up, read and return the times in the output file
    f = open('runtimes.txt', 'r')
    times = f.read().splitlines()

    subprocess.Popen(['rm', 'runtimes.txt'], stdout=subprocess.PIPE)

    return times


def main():

    # Arguments
    args = np.arange(5,16,1)
    args = 2**args
    print(args) 
    args_sq = np.square(args) /(2.5*(10**8))
	
    # Compute the runtimes of the algorithm for various N
    times = timerun('seq_nw', args)
    times = [float(x) for x in times]

    #plt.figure(figsize=(14, 4))
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Needleman-Wunsch Execution Times vs Input Size', fontsize=14, weight='bold')
    plt.plot(args, times, 'r+-', label = "NW")
    plt.plot(args,args_sq, 'b+-', label = "N^2")
    plt.xscale('log',basex=2)
    plt.yscale('log',basey=2)
    plt.legend()	
    plt.grid()

    # save the plot as a SVG image
    plt.savefig('execution_times2.png')

    # show the pylab plot window
    
    plt.show()


if __name__ == "__main__":
    main()
