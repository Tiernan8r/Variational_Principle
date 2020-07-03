from variational_principle.data_handling.json_data import JsonData
import logging
from multiprocessing import Lock


class CachedJsonData(JsonData):

    def __init__(self, filename="data/data.json"):
        super().__init__(filename)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialising new CachedJsonData object.")

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

        self.logger.debug("Cached data from '%s'" % self._filename)

        self.access_lock = Lock()

    @property
    def label(self):
        with self.access_lock:
            return self._label

    @label.setter
    def label(self, l: str):
        with self.access_lock:
            JsonData.label.fset(self, l)
            self._label = l

    @property
    def start(self):
        with self.access_lock:
            return self._start

    @start.setter
    def start(self, s):
        with self.access_lock:
            JsonData.start.fset(self, s)
            self._start = s

    @property
    def stop(self):
        with self.access_lock:
            return self._stop

    @stop.setter
    def stop(self, s):
        with self.access_lock:
            JsonData.stop.fset(self, s)
            self._stop = s

    @property
    def num_states(self):
        with self.access_lock:
            return self._num_states

    @num_states.setter
    def num_states(self, num):
        with self.access_lock:
            JsonData.num_states.fset(self, num)
            self._num_states = num

    @property
    def num_dimensions(self):
        with self.access_lock:
            return self._num_dimensions

    @num_dimensions.setter
    def num_dimensions(self, dim):
        with self.access_lock:
            JsonData.num_dimensions.fset(self, dim)
            self._num_dimensions = dim

    @property
    def num_samples(self):
        with self.access_lock:
            return self._num_samples

    @num_samples.setter
    def num_samples(self, num):
        with self.access_lock:
            JsonData.num_samples.fset(self, num)
            self._num_samples = num

    @property
    def num_iterations(self):
        with self.access_lock:
            return self._num_iterations

    @num_iterations.setter
    def num_iterations(self, num):
        with self.access_lock:
            JsonData.num_iterations.fset(self, num)
            self._num_iterations = num

    @property
    def plot_with_potential(self):
        with self.access_lock:
            return self._plot_with_potential

    @plot_with_potential.setter
    def plot_with_potential(self, v):
        with self.access_lock:
            JsonData.plot_with_potential.fset(self, v)
            self._plot_with_potential = v

    @property
    def plot_scale(self):
        with self.access_lock:
            return self._plot_scale

    @plot_scale.setter
    def plot_scale(self, sc):
        with self.access_lock:
            JsonData.plot_scale.fset(self, sc)
            self._plot_scale = sc

    @property
    def colourmap(self):
        with self.access_lock:
            return self._colourmap

    @colourmap.setter
    def colourmap(self, cmap):
        with self.access_lock:
            JsonData.colourmap.fset(self, cmap)
            self._colourmap = cmap
