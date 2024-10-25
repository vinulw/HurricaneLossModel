import subprocess
from time import time
import numpy as np

import matplotlib.pyplot as plt


def collect_samples(samples, repeats):
    '''
    Collect data to plot performance of `gethurricaneloss` command.

    Parameters
    ----------
    samples: List[int]
       List of numbers of samples to collect.
    repeats: int
        Number of repeats of each sample number to take.

    Returns
    -------
    times: List of list of times at each sample number.
    outputs: List of list of calculated outputs at each sample number.
    '''
    # Execut command
    cmd = ["gethurricaneloss", "-n", "1", "3", "5", "1", "3", "5", "1"]
    times = []
    outputs = []
    for n in samples:
        print(f"Current n: {n}")
        cmd[2] = n
        currTimes = []
        currOutput = []
        for _ in range(repeats):
            start = time()
            process = subprocess.run(cmd, capture_output=True,
                                     encoding='utf-8')
            end = time()
            currOutput.append(float(process.stdout))
            currTimes.append(end-start)
        times.append(currTimes)
        outputs.append(currOutput)

    return np.array(times), np.array(outputs)


if __name__ == "__main__":
    samples = [str(10**i) for i in range(1, 5)]
    repeats = 10

    times, output = collect_samples(samples, repeats)

    samplesArray = np.array([int(s) for s in samples])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot times vs sample number
    ax.errorbar(samplesArray, times.mean(axis=1), yerr=times.std(axis=1),
                fmt='x--', capsize=5)
    ax.set_xlabel('Number of samples')
    ax.set_ylabel('Simulation Time (s)')
    ax.set_xscale('log')
    ax.grid()

    plt.savefig('time_vs_samples.png')

    # Plot mean loss vs sample number
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.errorbar(samplesArray, output.mean(axis=1), yerr=output.std(axis=1),
                fmt='x--', capsize=5, color='green')
    ax.set_xlabel('Number of samples')
    ax.set_ylabel('Mean Loss')
    ax.set_xscale('log')
    ax.grid()

    plt.savefig('mean_loss_vs_samples.png')

    plt.show()
