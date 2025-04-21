import cmath
from math import pi
from ..core.engine import Component

class MagnonicSource(Component):
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

class MagnonicWaveguide(Component):
    def __init__(self, length=0.0, wavelength=1.0, phase_delay=None, name=None):
        super().__init__(name)
        self.num_inputs = 1
        self.num_outputs = 1
        self.inputs = [None]
        self.outputs = [None]
        if phase_delay is not None:
            self.phase_delay = phase_delay
        else:
            self.phase_delay = 2 * pi * (length / wavelength)

    def propagate(self):
        if self.inputs[0] is None:
            self.outputs[0] = None
        else:
            self.outputs[0] = self.inputs[0] * cmath.exp(1j * self.phase_delay)

class MagnonicMajorityGate(Component):
    def __init__(self, name=None):
        super().__init__(name)
        self.num_inputs = 3
        self.num_outputs = 1
        self.inputs = [None, None, None]
        self.outputs = [None]
        self.logic_output = None

    def propagate(self):
        count_one = 0
        amplitude_sum = 0.0
        for v in self.inputs:
            if v is None:
                self.outputs[0] = None
                return
            if v.real < 0:
                count_one += 1
            amplitude_sum += abs(v)
        if count_one >= 2:
            self.logic_output = 1
            phase_out = pi
        else:
            self.logic_output = 0
            phase_out = 0.0
        avg_amp = amplitude_sum / 3.0
        self.outputs[0] = avg_amp * cmath.exp(1j * phase_out)
 