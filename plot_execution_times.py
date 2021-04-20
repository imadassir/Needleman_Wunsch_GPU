import subprocess
import string
import numpy as np
import sys
import matplotlib.pyplot as plt
import time
from statistics import mean


def timerun(program, args) :
    print('Starting timed execution of ' + program + ' with ' + str(len(args)) + ' arguments.')
    i = 1

    subprocess.Popen(['rm', 'runtimes_seq.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu0.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu1.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu2.txt'], stdout=subprocess.PIPE)

    # Execute program, once for each n argument
    for n in args:
        #p = subprocess.Popen(['/usr/bin/time', '-o', 'runtimes.txt', '-a', '-f', '%e', './' + program, str(n)],
        #                     stdout=subprocess.PIPE)
        p = subprocess.Popen(['./' + program, '-0', '-1', '-2', '-N', str(n)], stdout=subprocess.PIPE)
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
    f_gpu1= open('runtimes_gpu1.txt', 'r')
    times_gpu1 = f_gpu1.read().splitlines()
    f_gpu2= open('runtimes_gpu2.txt', 'r')
    times_gpu2 = f_gpu2.read().splitlines()
    
    div0_2= [float(i)/float(j) for i,j in zip(times_gpu0,times_gpu2)]
    div1_2= [float(i)/float(j) for i,j in zip(times_gpu1,times_gpu2)]
    speedup0_2 = mean(div0_2)
    speedup1_2 = mean(div1_2)
    subprocess.Popen(['rm', 'runtimes_seq.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu0.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu1.txt'], stdout=subprocess.PIPE)
    subprocess.Popen(['rm', 'runtimes_gpu2.txt'], stdout=subprocess.PIPE)

    return times_seq, times_gpu0, times_gpu1, times_gpu2, speedup0_2, speedup1_2


def main():
    # Get system information
    p = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
    # Read back from stdin, print
    output = p.communicate()[0]
    sys.stdout.write('\n\n\nProcessor info' +  str(output) + '\n' )

    # Arguments
    args = np.arange(5,13,1)
    args = 2**args
	
    # Compute the runtimes of the algorithm for various N
    times_seq, times_gpu0, times_gpu1, times_gpu2, speedup0_2, speedup1_2 = timerun('nw', args)
    times_seq = [float(x) for x in times_seq]
    times_gpu0 = [float(x) for x in times_gpu0]
    times_gpu1 = [float(x) for x in times_gpu1]
    times_gpu2 = [float(x) for x in times_gpu2]
    print('Average speedup with reference to GPU v0:' + str(speedup0_2))
    print('Average speedup with reference to GPU v1:' + str(speedup1_2))
    #plt.figure(figsize=(14, 4))
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Needleman-Wunsch Execution Time vs Input Size', fontsize=14, weight='bold')
    plt.plot(args, times_seq, 'r+-', label = "Sequential NW")
    plt.plot(args, times_gpu0, 'g+-', label = "Parallel NW v0")
    plt.plot(args, times_gpu1, 'b+-', label = "Parallel NW v1")
    plt.plot(args, times_gpu2, 'o+-', label = "Parallel NW v2")
    plt.xscale('log',basex=2)
    plt.yscale('log',basey=2)
    plt.legend()	
    plt.grid()

    # save the plot as a PNG image
    plt.savefig('execution_times.png')
	
    plt.show()


if __name__ == "__main__":
    main()
