from numpy.random import Generator, PCG64
import multiprocessing
import concurrent.futures
import numpy as np


class MultithreadedRNG:
    def __init__(self, seed=None, threads=None):
        rg = PCG64(seed)
        if threads is None:
            threads = multiprocessing.cpu_count()
        self.threads = threads

        self._random_generators = [rg]
        last_rg = rg
        for _ in range(0, threads-1):
            new_rg = last_rg.jumped()
            self._random_generators.append(new_rg)
            last_rg = new_rg
        self._random_generators = [Generator(rg) for rg in self._random_generators]

        self.executor = concurrent.futures.ThreadPoolExecutor(threads)

    def __del__(self):
        self.executor.shutdown(False)

    def fill(self, out: np.array, p: float):
        def filler(rg: Generator, first: int, last: int):
            out[first:last] = rg.binomial(1, p, out[first:last].shape)

        step = np.ceil(len(out) / self.threads).astype(np.int_)
        futures = {}
        for i in range(self.threads):
            args = (filler,
                    self._random_generators[i],
                    i * step,
                    (i + 1) * step,
                    )
            futures[self.executor.submit(*args)] = i
        concurrent.futures.wait(futures)
