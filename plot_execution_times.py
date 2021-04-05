import subprocess
import string
import numpy as np
import sys
import matplotlib.pyplot as plt
import time


def timerun(program, args) :
    print('Starting timed execution of ' + program + ' with ' + str(len(args)) + ' arguments.')
    i = 1

    subprocess.Popen(['rm', 'runtimes_seq.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu0.txt'], stdout=subprocess.PIPE)

    # Execute program, once for each n argument
    for n in args:

        # This was really annoying. Build the arguments to the time system call to the time command.
        # First of all, for whatever reason 'time' didn't work correctly with any arguments other than -p,
        # so I used /usr/bin/time instead. Since I could not figure out why the output of 'time' was not
        # coming back to stdin, I use the -o (output file) and -a (append) option to just output the real
        # execution time ( thats where '-f' and '%e' comes from ) to the file.
        #p = subprocess.Popen(['/usr/bin/time', '-o', 'runtimes.txt', '-a', '-f', '%e', './' + program, str(n)],
        #                     stdout=subprocess.PIPE)
        p = subprocess.Popen(['./' + program, '-0', '-N', str(n)], stdout=subprocess.PIPE)
        # Read back from stdin, print where we are
        output = p.communicate()[0]
        sys.stdout.write(str(i) + ':\tnw(' + str(n) + ') = ' + str(output))
        i += 1
    print('done')

    # Open up, read and return the times in the output file
    f_seq = open('runtimes_seq.txt', 'r')
    times_seq = f_seq.read().splitlines()
    f_gpu0= open('runtimes_gpu0.txt', 'r')
    times_gpu0 = f_gpu0.read().splitlines()

    subprocess.Popen(['rm', 'runtimes_seq.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu0.txt'], stdout=subprocess.PIPE)

    return times_seq, times_gpu0


def main():

    # Arguments
    args = np.arange(5,16,1)
    args = 2**args
    print(args) 
    args_sq = np.square(args) /(2.5*(10**8))
	
    # Compute the runtimes of the algorithm for various N
    times_seq, times_gpu0 = timerun('nw', args)
    times_seq = [float(x) for x in times_seq]
    times_gpu0 = [float(x) for x in times_gpu0]

    #plt.figure(figsize=(14, 4))
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Needleman-Wunsch Execution Time vs Input Size', fontsize=14, weight='bold')
    plt.plot(args, times_seq, 'r+-', label = "Sequential NW")
    plt.plot(args, times_gpu0, 'g+-', label = "Parallel NW v0")
    plt.plot(args,args_sq, 'b+-', label = "N^2")
    plt.xscale('log',basex=2)
    plt.yscale('log',basey=2)
    plt.legend()	
    plt.grid()

    # save the plot as a SVG image
    plt.savefig('execution_times.png')

    # show the pylab plot window
    
    plt.show()


if __name__ == "__main__":
    main()
