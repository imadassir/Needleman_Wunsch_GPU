import subprocess
import string
import numpy as np
import sys
import pylab  # matplotlib
import matplotlib.pyplot as plt


def timerun(program, args) :
    print('Starting timed execution of ' + program + ' with ' + str(len(args)) + ' arguments.')
    i = 1

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
    args = np.arange(10, 500, 50)
    args2 = np.arange(501, 20001, 500)
    args = np.concatenate((args, args2), axis=None)

    # Compute the runtimes of the algorithm for various N
    times = timerun('seq_nw', args)
    times = [float(x) for x in times]

    # Plot it with pylab
    plt.figure(figsize=(14, 4))
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Needleman-Wunsch Execution Times vs Input Size', fontsize=14, weight='bold')
    plt.plot(args, times, 'r+-')
    plt.grid()

    # save the plot as a SVG image
    plt.savefig('execution_times.png')

    # show the pylab plot window
    
    plt.show()


if __name__ == "__main__":
    main()
