from Brain.components import *
from Brain.Connectome import LazyConnectome
from Brain.Connectome import NonLazyConnectome


from . import profile


a1 = Area(n=10000, k=100, beta=0.05)
a2 = Area(n=10000, k=100, beta=0.05)
s1 = Stimulus(n=100, beta=0.05)


@profile
def time_non_lazy():
    yield 'init_connectome'
    nlc = NonLazyConnectome(areas=[a1, a2], stimuli=[s1], p=0.05)
    yield 'first_projects'
    nlc.project({s1: [a1]})
    nlc.project({a1: [a2]})
    yield 'many_projects'
    for i in range(25):
        nlc.project({a1: [a2]})


@profile
def time_lazy():
    yield 'init_connectome'
    lc = LazyConnectome(areas=[a1, a2], stimuli=[s1], p=0.05)
    yield 'first_projects'
    lc.project({s1: [a1]})
    lc.project({a1: [a2]})
    yield 'many_projects'
    for i in range(25):
        lc.project({a1: [a2]})
