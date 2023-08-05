# Function to load machines
import re
from maquinas.regular.dfa import * 
from maquinas.regular.ndfa import * 
from maquinas.regular.ndfa_e import * 
from maquinas.exceptions import * 

re_state = re.compile(r"^\s*(?P<initial>->)?\s*(?P<state>.*[^\]])[^\]]*(?P<final>])?$")

def load_fa(string):
    header=False
    delta={}
    for line in string.split("\n"):
        line=line.strip()
        if len(line)==0 or line.startswith("#"):
            continue
        if not header:
            sigma=read_sigma(line)
            header=True
        else:
            origin,states=read_row(line)
            delta[origin]=states
    type_machine=1
    if 'epsilon' in sigma:
        type_machine=3
    if 'ε' in sigma:
        type_machine=3
    if type_machine==1:
        for o,states in delta.items():
            for s in states:
                if len(s)>1:
                    type_machine=2
                    break
            if type_machine==2:
                break
    if type_machine==1:
        m=DeterministicFiniteAutomaton()
    elif type_machine==2:
        m=NonDeterministicFiniteAutomaton()
    elif type_machine==3:
        m=NonDeterministicFiniteAutomaton_epsilon()

    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A=set()
    for (ini,fin,q_i),states in delta.items():
        if fin:
            A.add(q_i)
        for j,state in enumerate(states):
            m.add_transition(q_i,sigma[j],state,force=True)
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m

def read_sigma(line):
    return [ a.strip() for a in  line.split("|") if len(a.strip())>0 ]

def read_row(line):
    row=[ a.strip() for a in  line.split("|") if len(a.strip())>0 ]
    origin=read_state(row[0])
    return origin, read_states(row[1:])

def read_state(state):
    m=re_state.match(state)
    return m.group('initial')!=None,m.group('final')!=None,m.group('state').strip()

def read_states(states):
    return [[s.strip() for s in  state.split(',')] for state in states ]

