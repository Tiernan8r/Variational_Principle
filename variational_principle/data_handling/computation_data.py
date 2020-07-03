from variational_principle.data_handling.cached_json_data import CachedJsonData
import logging
from numpy import ndarray


class ComputationData(CachedJsonData):

    def __init__(self, r=None, V=None, filename="data/data.json"):
        super().__init__(filename)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialising new ComputationData object.")

        self._all_psi = []
        self._all_energy = []
        self.logger.debug("Initialised lists.")

        self.r_key = "position"
        self.v_key = "potential"

        self.r = r
        self.V = V
        self.logger.debug("Assigned given r & V variables")

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r: ndarray):
        self._r = r

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, v: ndarray):
        self._V = v

    @property
    def all_psi(self):
        return self._all_psi

    @property
    def all_energy(self):
        return self._all_energy

    def add_psi(self, psi: ndarray):
        if psi is None:
            self.logger.debug("Given psi is None, returning.")
            return
        self._all_psi.append(psi)

    def add_energy(self, energy):
        if energy is None:
            self.logger.debug("Given energy is None, returning.")
            return
        self._all_energy.append(energy)

    def clear(self):
        self.logger.debug("Clearing all container types.")
        self._all_psi.clear()
        self._all_energy.clear()
        self.logger.debug("Cleared the lists.")