from .core import engine

class Circuit:
    def __init__(self):
        self.components = []
        self.input_map = {}
        self._type_counters = {}

    def add_component(self, comp, name=None):
        if name:
            comp.name = name
        if comp.name is None:
            type_name = comp.__class__.__name__
            count = self._type_counters.get(type_name, 0) + 1
            self._type_counters[type_name] = count
            comp.name = f"{type_name}{count}"
        else:
            for c in self.components:
                if c.name == comp.name:
                    raise ValueError(f"Duplicate component name: {comp.name}")
        self.components.append(comp)
        return comp

    def connect(self, src_comp, dest_comp, src_port=0, dest_port=0):
        if src_comp not in self.components:
            self.add_component(src_comp)
        if dest_comp not in self.components:
            self.add_component(dest_comp)
        key = (dest_comp, dest_port)
        self.input_map.setdefault(key, []).append((src_comp, src_port))

    def simulate(self, frequency=1.0):
        return engine.simulate(self, frequency=frequency)

    # Convenience functions
    def add_photonic_source(self, amplitude=1.0, phase=0.0, bit=None, name=None):
        from .components.photonic import PhotonicSource
        return self.add_component(PhotonicSource(amplitude, phase, bit, name))

    def add_photonic_waveguide(self, length=0.0, n_eff=1.0, wavelength=1.0, phase_delay=None, name=None):
        from .components.photonic import PhotonicWaveguide
        return self.add_component(PhotonicWaveguide(length, n_eff, wavelength, phase_delay, name))

    def add_photonic_splitter(self, split_ratio=0.5, name=None):
        from .components.photonic import PhotonicSplitter
        return self.add_component(PhotonicSplitter(split_ratio, name))

    def add_photonic_combiner(self, name=None):
        from .components.photonic import PhotonicCombiner
        return self.add_component(PhotonicCombiner(name))

    def add_magnonic_source(self, amplitude=1.0, phase=0.0, bit=None, name=None):
        from .components.magnonic import MagnonicSource
        return self.add_component(MagnonicSource(amplitude, phase, bit, name))

    def add_magnonic_waveguide(self, length=0.0, wavelength=1.0, phase_delay=None, name=None):
        from .components.magnonic import MagnonicWaveguide
        return self.add_component(MagnonicWaveguide(length, wavelength, phase_delay, name))

    def add_magnonic_majority(self, name=None):
        from .components.magnonic import MagnonicMajorityGate
        return self.add_component(MagnonicMajorityGate(name))
