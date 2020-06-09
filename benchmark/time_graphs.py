from Brain.components import *
from Brain.Connectome import Connectome
from Brain.Connectome import NonLazySparseConnectome
from Brain.Connectome import NonLazyConnectomeOriginal
from Brain.Connectome import NonLazyConnectomeRandomMatrix

import matplotlib.pylab as plt

import os
import time
from pathlib import Path


def create_gen(cls):
    def gen(a1, a2, s1):
        inst = cls(areas=[a1, a2], stimuli=[s1], p=0.05)
        yield 'init_connectome'
        inst.project({s1: [a1]})
        inst.project({a1: [a2]})
        yield 'first_projects'
        for i in range(25):
            inst.project({a1: [a2]})
        yield 'many_projects'
    gen.__name__ = cls.__name__
    return gen


non_lazy = create_gen(Connectome)
non_lazy_original = create_gen(NonLazyConnectomeOriginal)
non_lazy_sparse = create_gen(NonLazySparseConnectome)
random_matrix = create_gen(NonLazyConnectomeRandomMatrix)

gens = [
        non_lazy,
        non_lazy_original,
        non_lazy_sparse,
        random_matrix,
        ]

def timed(g):
    durations = {}
    while True:
        try:
            before = int(time.time() * 1000)
            section = next(g)
            after = int(time.time() * 1000)
            durations[section] = (after - before)
        except StopIteration:
            return durations


def sample_timing(gen):
    # dict(n: durations)
    d = {}
    print(f"Creating sample for {gen.__name__}")
    for i in range(1, 11):
        a1 = Area(n=(1000 * i), k=(10 * i), beta=0.05)
        a2 = Area(n=(1000 * i), k=(10 * i), beta=0.05)
        s1 = Stimulus(n=(10 * i), beta=0.05)
        d[(1000 * i)] = timed(gen(a1, a2, s1))
    return d


def sample_by_section(gen):
    sample = sample_timing(gen)
    sample_by_section = {}
    for section in ['init_connectome', 'first_projects', 'many_projects']:
        sample_by_section[section] = {key: sample[key][section] for key in sample}
    return sample_by_section


def get_sample(classes=None):
    sample = {}
    sample_gens = gens if not classes else filter(lambda gen: gen.__name__ in classes, gens)
    for gen in sample_gens:
        sample[gen.__name__] = sample_by_section(gen)
    return sample


def create_graph(sample, section, path):
    legend = []
    for gen in sample:
        lists = sorted(sample[gen][section].items())
        x, y = zip(*lists)
        plt.plot(x, y, 'o-.')
        plt.title(section)
        plt.xlabel('area size (#neurons)')
        plt.ylabel('time (milliseconds)')
        name = gen if gen != 'Connectome' else 'NonLazyConnectomeNew'
        legend.append(name)
    plt.legend(legend, loc='upper left')
    plt.savefig(f"{path}/{section}.pdf")
    plt.clf()


def get_directory(root):
    index = 1
    while True:
        path = root / str(index)
        if path.exists():
            index += 1
            continue
        path.mkdir(parents=True)
        return str(path)


def graphit(name=None, classes=None):
    sample = get_sample(classes)
    root = Path(os.path.abspath('.')) / 'graphs'
    if name:
        (root / name).mkdir(parents=True, exist_ok=True)
    path = str(root / name) if name else get_directory(root)
    create_graph(sample, 'first_projects', path)
    create_graph(sample, 'many_projects', path)
    print(f"Saved graphs to {path}")
