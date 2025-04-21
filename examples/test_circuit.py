import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wave_logic_sim.components.photonic import PhotonicSource, PhotonicWaveguide, PhotonicSplitter, PhotonicCombiner
from wave_logic_sim.components.magnonic import MagnonicSource, MagnonicMajorityGate
from wave_logic_sim.circuit import Circuit
from wave_logic_sim.visualization.plotter import plot_signals
import numpy as np



# --- MACH-ZEHNDER INTERFEROMETER (PHOTONIC) ---
circuit1 = Circuit()

# Components
src = PhotonicSource(phase=0.0, name="LaserInput")
split = PhotonicSplitter(name="Splitter")
wg1 = PhotonicWaveguide(length=1.0, name="Arm1")
wg2 = PhotonicWaveguide(length=1.0, name="Arm2")
phase_shift = PhotonicWaveguide(phase_delay=np.pi, name="PhaseShifter")  # try 0.0 or np.pi
comb = PhotonicCombiner(name="Combiner")

# Wiring
circuit1.connect(src, split)
circuit1.connect(split, wg1, src_port=0, dest_port=0)
circuit1.connect(split, wg2, src_port=1, dest_port=0)
circuit1.connect(wg1, comb, dest_port=0)
circuit1.connect(wg2, phase_shift)
circuit1.connect(phase_shift, comb, dest_port=1)

# Simulate
result1 = circuit1.simulate()
print("Photonic Combiner Output:", result1["Combiner"])

# --- SPIN-WAVE MAJORITY GATE (MAGNONIC) ---
circuit2 = Circuit()

# Inputs: two logic 1s and one logic 0
s1 = MagnonicSource(bit=0, name="SpinA")
s2 = MagnonicSource(bit=1, name="SpinB")
s3 = MagnonicSource(bit=1, name="SpinC")
maj_gate = MagnonicMajorityGate(name="Majority")

# Wiring
circuit2.connect(s1, maj_gate, dest_port=0)
circuit2.connect(s2, maj_gate, dest_port=1)
circuit2.connect(s3, maj_gate, dest_port=2)

# Simulate
result2 = circuit2.simulate()
output_wave = result2["Majority"]
logic_result = maj_gate.logic_output
print("Magnonic Majority Output (wave):", output_wave)
print("Magnonic Logic Result:", logic_result)

# --- VISUALIZE WAVEFORMS ---
t = np.linspace(0, 1.0, 300)
y1 = s1.amplitude * np.sin(2 * np.pi * t + s1.phase)
y2 = s2.amplitude * np.sin(2 * np.pi * t + s2.phase)
y3 = s3.amplitude * np.sin(2 * np.pi * t + s3.phase)
out = abs(output_wave) * np.sin(2 * np.pi * t + np.angle(output_wave))

plot_signals(t, {
    "Spin A": y1,
    "Spin B": y2,
    "Spin C": y3,
    "Majority Output": out
}, title="Spin-Wave Majority Gate")
