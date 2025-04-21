import cmath
from math import pi, sqrt
from ..core.engine import Component

class PhotonicSource(Component):
    def __init__(self, amplitude=1.0, phase=0.0, bit=None, name=None):
        super().__init__(name)
        self.num_inputs = 0
        self.num_outputs = 1
        self.inputs = []
        self.outputs = [None]
        if bit is not None:
            phase = 0.0 if bit == 0 else pi
        self.amplitude = amplitude
        self.phase = phase

    def propagate(self):
        self.outputs[0] = self.amplitude * cmath.exp(1j * self.phase)

class PhotonicWaveguide(Component):
    def __init__(self, length=0.0, n_eff=1.0, wavelength=1.0, phase_delay=None, name=None):
        super().__init__(name)
        self.num_inputs = 1
        self.num_outputs = 1
        self.inputs = [None]
        self.outputs = [None]
        if phase_delay is not None:
            self.phase_delay = phase_delay
        else:
            self.phase_delay = 2 * pi * n_eff * (length / wavelength)

    def propagate(self):
        if self.inputs[0] is None:
            self.outputs[0] = None
        else:
            self.outputs[0] = self.inputs[0] * cmath.exp(1j * self.phase_delay)

class PhotonicSplitter(Component):
    def __init__(self, split_ratio=0.5, name=None):
        super().__init__(name)
        self.num_inputs = 1
        self.num_outputs = 2
        self.inputs = [None]
        self.outputs = [None, None]
        self.amp1 = sqrt(split_ratio)
        self.amp2 = sqrt(1 - split_ratio)

    def propagate(self):
        if self.inputs[0] is None:
            self.outputs = [None, None]
        else:
            self.outputs[0] = self.inputs[0] * self.amp1
            self.outputs[1] = self.inputs[0] * self.amp2

class PhotonicCombiner(Component):
    def __init__(self, name=None):
        super().__init__(name)
        self.num_inputs = 2
        self.num_outputs = 1
        self.inputs = [None, None]
        self.outputs = [None]

    def propagate(self):
        v1 = self.inputs[0]
        v2 = self.inputs[1]
        if v1 is None and v2 is None:
            self.outputs[0] = None
        elif v1 is None:
            self.outputs[0] = v2
        elif v2 is None:
            self.outputs[0] = v1
        else:
            self.outputs[0] = v1 + v2
