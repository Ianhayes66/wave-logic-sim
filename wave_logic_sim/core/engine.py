import math
import cmath

class Component:
    def __init__(self, name=None):
        self.name = name
        self.num_inputs = 0
        self.num_outputs = 0
        self.inputs = []
        self.outputs = []

    def propagate(self):
        raise NotImplementedError("Each component must implement propagate()")

def simulate(circuit, frequency=1.0):
    for comp in circuit.components:
        comp.outputs = [None] * comp.num_outputs
        comp.inputs = [None] * comp.num_inputs

    done = {comp: False for comp in circuit.components}
    made_progress = True

    while made_progress:
        made_progress = False
        for comp in circuit.components:
            if done[comp]:
                continue
            ready = all(
                (comp, i) in circuit.input_map and all(src.outputs[src_port] is not None
                for src, src_port in circuit.input_map[(comp, i)])
                for i in range(comp.num_inputs)
            )
            if ready:
                for i in range(comp.num_inputs):
                    sources = circuit.input_map[(comp, i)]
                    value = sum(src.outputs[src_port] for src, src_port in sources)
                    comp.inputs[i] = value
                comp.propagate()
                done[comp] = True
                made_progress = True

    if not all(done.values()):
        raise RuntimeError("Simulation incomplete: cycle or missing input?")

    return {comp.name: comp.outputs[0] if comp.num_outputs == 1 else comp.outputs for comp in circuit.components}
