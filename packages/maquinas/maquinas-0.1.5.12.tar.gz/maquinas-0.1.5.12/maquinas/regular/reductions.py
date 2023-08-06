# Código para reducciones

from maquinas.regular.dfa import DeterministicFiniteAutomaton as DFA
from maquinas.regular.ndfa import NonDeterministicFiniteAutomaton as NDFA
from maquinas.regular.ndfa_e import NonDeterministicFiniteAutomaton_epsilon as NDFA_e
from maquinas.regular.ndfa_e import epsilon
from maquinas.exceptions import *
from ordered_set import OrderedSet


def ndfa_e2ndfa(ndfa_e,rename=True,remove_sink=True):
    ndfa=NDFA()

    extra_A=set()
    for q_i in ndfa_e.Q:
        for a in ndfa_e.sigma:
            if a == epsilon:
                if len(ndfa_e.A.intersection(ndfa_e.expansion_epsilon(set([q_i]))))>0:
                    extra_A.add(q_i)
                continue
            qs_f=ndfa_e.delta_extended(set([q_i]),a)
            ndfa.add_transition(q_i,a,qs_f,force=True)

    ndfa.set_initial_state(ndfa_e.q_0)
    ndfa.A=ndfa_e.A.union(extra_A)
    if remove_sink:
        ndfa.remove_sink_states()
    if rename:
        ndfa.autorename()
    return ndfa

def codify_state(Q,s):
    s_=["0" for _ in Q]
    for q in s:
        s_[Q.index(q)]="1"
    return "".join(s_)


def ndfa2dfa(ndfa,rename=True,remove_sink=True):
    dfa=DFA()
    max_size=len(ndfa.Q)+1
    initial_state=set([ndfa.q_0])
    initial_state_=codify_state(ndfa.Q,initial_state)
    new_states={}
    new_states[initial_state_]=initial_state
    A=set()
    if len(initial_state.intersection(ndfa.A))>0:
        A.add(initial_state_)
    states={}
    lprev=-1
    while len(new_states)>0:
        states.update(new_states)
        lprev=len(states)
        new_new_states={}
        for state_,elements in new_states.items():
            for a in ndfa.sigma:
                new_state=set()
                for q in elements:
                    try:
                        new_state.update(ndfa.get_transition(q,a))
                    except DoesNotExistsTransition:
                        pass
                new_state_=codify_state(ndfa.Q,new_state)
                dfa.add_transition(state_,a,new_state_,force=True)
                if not new_state_ in states:
                    new_new_states[new_state_]=new_state
                if len(new_state.intersection(ndfa.A))>0:
                    A.add(new_state_)
        new_states=new_new_states
    dfa.set_initial_state(initial_state_)
    dfa.set_aceptors(A)

    if rename:
        dfa.autorename()
    if remove_sink:
        dfa.remove_sink_states()
    return dfa


def dfa2ndfa_e(dfa,rename=True,remove_sink=True):
    ndfa_e=NDFA_e()
    ndfa_e.Q=OrderedSet(dfa.Q)
    ndfa_e.sigma.update(dfa.sigma)
    for nq_i,t_ in dfa.ttable.items():
        for na,nq_f in t_.items():
            na=na+1
            try:
                ndfa_e.ttable[nq_i][na]=set([nq_f])
            except KeyError:
                ndfa_e.ttable[nq_i]={}
                ndfa_e.ttable[nq_i][na]=set([nq_f])

    ndfa_e.q_0=dfa.q_0
    ndfa_e.A=set(dfa.A)
    if rename:
        ndfa_e.autorename()
    if remove_sink:
        ndfa_e.remove_sink_states()
    return ndfa_e


def ndfa_e2dfa(ndfa_e,rename=True,remove_sink=True):
    return ndfa2dfa(ndfa_e2ndfa(ndfa_e,rename=rename,remove_sink=remove_sink),rename=rename,remove_sink=remove_sink)

def ndfa2ndfa_e(ndfa,rename=True,remove_sink=True):
    return dfa2ndfa_e(ndfa2dfa(ndfa,rename=rename,remove_sink=remove_sink),rename=rename,remove_sink=remove_sink)

def dfa2ndfa(dfa,rename=True,remove_sink=True):
    return ndfa_e2ndfa(dfa2ndfa_e(dfa,rename=rename,remove_sink=remove_sink),rename=rename,remove_sink=remove_sink)

