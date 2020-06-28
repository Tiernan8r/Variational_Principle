import variational_principle.data_handling.json_data as jd
import collections


class ComputedData(jd.JsonData):

    def __init__(self, r=None, V=None, filename="data.json"):
        super().__init__(filename)

        self._array_dict = {}
        self._energy_dict = {}

        self.r = r
        self.V = V

        self._psi_queue = collections.deque()
        self._energy_queue = collections.deque()

        self._all_psi = []
        self._all_energy = []

        self._label = super().label
        self._start = super().start
        self._stop = super().stop
        self._num_states = super().num_states
        self._num_dimensions = super().num_dimensions
        self._num_samples = super().num_samples
        self._num_iterations = super().num_iterations
        self._plot_with_potential = super().plot_with_potential
        self._plot_scale = super().plot_scale
        self._colourmap = super().colourmap

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, R):
        self._r = R
        self._array_dict["position"] = R

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, v):
        self._V = v
        self._array_dict["potential"] = v

    def get_energy(self, key):
        return self._energy_dict.get(key, None)

    def get_array(self, key):
        return self._array_dict.get(key, None)

    def put_psi(self, psi):
        i = len(self._all_psi)
        self._all_psi.append(psi)

        key = "state_{}".format(i)
        self._array_dict[key] = psi

        # TODO lock the queue
        self._psi_queue.append(psi)

    def pop_psi(self):
        # TODO lock the queue
        psi = self._psi_queue.popleft()
        return psi

    def put_energy(self, energy):
        i = len(self._all_energy)
        self._all_energy.append(energy)

        key = "state_{}".format(i)
        self._energy_dict[key] = energy

        # TODO lock the queue
        self._energy_queue.append(energy)

    def pop_energy(self):
        # TODO lock
        return self._energy_queue.popleft()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, l: str):
        super().label = l
        self._label = l

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, s):
        super().start = s
        self._start = s

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, s):
        super().stop = s
        self._stop = s

    @property
    def num_states(self):
        return self._num_states

    @num_states.setter
    def num_states(self, num):
        super().num_states = num
        self._num_states = num

    @property
    def num_dimensions(self):
        return self._num_dimensions

    @num_dimensions.setter
    def num_dimensions(self, dim):
        super().num_dimensions = dim
        self._num_dimensions = dim

    @property
    def num_samples(self):
        return self._num_samples

    @num_samples.setter
    def num_samples(self, num):
        super().num_samples = num
        self._num_samples = num

    @property
    def num_iterations(self):
        return self._num_iterations

    @num_iterations.setter
    def num_iterations(self, num):
        super().num_iterations = num
        self._num_iterations = num

    @property
    def plot_with_potential(self):
        return self._plot_with_potential

    @plot_with_potential.setter
    def plot_with_potential(self, v):
        super().plot_with_potential = v
        self._plot_with_potential = v

    @property
    def plot_scale(self):
        return self._plot_scale

    @plot_scale.setter
    def plot_scale(self, sc):
        super().plot_scale = sc
        self._plot_scale = sc

    @property
    def colourmap(self):
        return self._colourmap

    @colourmap.setter
    def colourmap(self, cmap):
        super().colourmap = cmap
        self._colourmap = cmap
