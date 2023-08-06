import pedersen
from matplotlib import pyplot as plt
from scipy import stats
import time
import statistics
import board
import sys
import bitproof

def pedersen_histogram():
    """Plots histograms of public values of Pedersen commitments
    when message is zero or one
    """
    x= 1000000
    gen = pedersen.Pedersen(256)
    c0 = []
    c1 = []
    for i in range(x):
        c0.append(gen.commit(0).c / 1.0)
        c1.append(gen.commit(1).c / 1.0)
        if (i % 10000 == 0):
            print(i // 10000)

    plt.title("Histogram of Commitments when Message Equals Zero")
    plt.hist(c0, bins = "auto", range = (0, gen.state.p / 1.0))  
    plt.ylabel("Occurences")
    plt.xlabel("Commitment value")
    plt.show()
    plt.title("Histogram of Commitments when Message Equals One")
    plt.hist(c1, bins = "auto", range = (0, gen.state.p / 1.0))  
    plt.ylabel("Occurences")
    plt.xlabel("Commitment value")
    plt.show()

def time_generate():
    """Returns the time to generate a Pedersen commitment of selected sizes"""
    c = []
    x = 1000
    a = ("16", "32", "64", "128", "256")
    times = [[],[],[],[],[]]
    t = []
    e = []
    for i in range(len(a)):
        for j in range(x):
            start = time.time()
            gen = pedersen.Pedersen(2 ** (4 + i))
            end = time.time()
            times[i].append(end - start)
            if (j % 25 == 0):
                print(j)
        print(i)
        t.append(statistics.fmean(times[i]))
        e.append(statistics.stdev(times[i]))
    plt.ylabel("Bits")
    plt.xlabel("Time (avg over 1000 trials) (s)")
    plt.title("Commitment Bit Length vs Time of Generation")
    plt.barh(a, t, xerr = e)
    plt.show()

def full_proof():
    """Returns the size and time to genrerate a full proof (sum and bit)"""
    a = battleship.ShipBoard()
    a.set_spot("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8")
    times = []
    sizes = []
    for j in range(100):
        start = time.time()
        a.update_commitments()
        b = a.send_initial()
        end = time.time()
        sizes.append(sys.getsizeof(b))
        times.append(end - start)
    print(statistics.mean(times))
    print(statistics.stdev(times))
    print(statistics.mean(sizes))
    print(statistics.stdev(sizes))

def pedersen_distribution():
    """Returns tests for the distribution of public values
    for Pedersen commitments when the message is zero or one
    """ 
    x= 1000000
    gen = pedersen.Pedersen(256)
    c0 = []
    c1 = []
    for i in range(x):
        c0.append(gen.commit(0).c / 1.0)
        c1.append(gen.commit(1).c / 1.0)
        if (i % (x / 100) == 0):
            print(100 * i / x)
    print(stats.ks_2samp(c0, c1))
    print("ks 0:", stats.kstest(c0, "uniform"))
    print("ks 1:", stats.kstest(c1, "uniform"))
    print("0", stats.describe(c0))
    print("1", stats.describe(c1))
    print("0 repeats:", stats.find_repeats(c0))
    print("1 repeats:", stats.find_repeats(c1))
    print("0 entropy:", stats.entropy(c0))
    print("1 entropy:", stats.entropy(c1))
    input()

def bitproof_test(z, same_graph = False, x = 100000):
    """Print's histogram for selected value of bitproof commitment
    along with statistical tests on the values
    z takes the form of lambda x: x.(variable here)
    same_graph is whether the histograms are on the same page
    x is the number of trials
    """
    gen = pedersen.Pedersen(64)
    c0 = gen.commit(0)
    c1 = gen.commit(1)
    b0 = []
    b1 = []
    for i in range(x):
        b0.append(z(bitproof.bitproof(0, c0, gen.state)) / 1.0)
        b1.append(z(bitproof.bitproof(1, c1, gen.state)) / 1.0)
        if (i % (x/100) == 0):
            print(100 * i / x)
    print("y1")
    print(stats.ks_2samp(b0, b1))
    print("ks 0:", stats.kstest(b0, "uniform"))
    print("ks 1:", stats.kstest(b1, "uniform"))
    print("0", stats.describe(b0))
    print("1", stats.describe(b1))
    print("0 repeats:", stats.find_repeats(b0))
    print("1 repeats:", stats.find_repeats(b1))
    print("0 entropy:", stats.entropy(b0))
    print("1 entropy:", stats.entropy(b1))
    plt.hist(b0, bins = "auto", range = (0, gen.state.p / 1.0))
    if not same_graph:
        plt.show()
    plt.hist(b1, bins = "auto", range = (0, gen.state.p / 1.0))
    plt.show()

if __name__ == "__main__":
    bitproof_test(lambda x : x.y1, True)
