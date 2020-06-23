import json

# hardcoded default data incase the default_data.json file doesn't exist or can't be read.
_backup_default_data = {"label": "Linear Harmonic Oscillator",
                        "start": -10,
                        "stop": 10,
                        "num_states": 1,
                        "num_dimensions": 1,
                        "num_samples": 100,
                        "num_iterations": 5,
                        "plot_with_potential": False,
                        "plot_scale": 10
                        }


def write_data(label, start, stop, num_states, num_dimensions, num_samples, num_iterations, plot_with_potential,
               plot_scale, filename="data.json"):
    data = {"label": label,
            "start": start,
            "stop": stop,
            "num_states": num_states,
            "num_dimensions": num_dimensions,
            "num_samples": num_samples,
            "num_iterations": num_iterations,
            "plot_with_potential": plot_with_potential,
            "plot_scale": plot_scale
            }
    with open(filename, "w", encoding="utf-8") as data_file:
        dump = json.dumps(data, indent=4, separators=(",", ": "), ensure_ascii=False)
        data_file.write(dump)


def read_data(filename="data.json"):
    with open(filename) as data_file:
        try:
            json_data = json.load(data_file)
        except json.JSONDecodeError as e:
            json_data = read_default()
            ##TODO: logging
            # raise e
        return json_data


class JsonData (object):

    def __init__(self, filename="data.json"):
        self._filename = filename

    def _write(self, data: dict):

        label = data.get("label", _backup_default_data["label"])
        start = data.get("start", _backup_default_data["start"])
        stop = data.get("stop", _backup_default_data["stop"])
        num_states = data.get("num_states", _backup_default_data["num_states"])
        num_dimensions = data.get("num_dimensions", _backup_default_data["num_dimensions"])
        num_samples = data.get("num_samples", _backup_default_data["num_samples"])
        num_iterations = data.get("num_iterations", _backup_default_data["num_iterations"])
        plot_with_potential = data.get("plot_with_potential", _backup_default_data["plot_with_potential"])
        plot_scale = data.get("plot_scale", _backup_default_data["plot_scale"])

        write_data(label, start, stop, num_states, num_dimensions, num_samples, num_iterations,
                   plot_with_potential, plot_scale, filename=self._filename)

    def _read(self):
        return read_data(self._filename)

    @property
    def label(self):
        return self._read().get("label", _backup_default_data["label"])

    @label.setter
    def label(self, l: str):
        data = self._read()
        data["label"] = l
        self._write(data)

    @property
    def start(self):
        return self._read().get("start", _backup_default_data["start"])

    @start.setter
    def start(self, s):
        data = self._read()
        data["start"] = s
        self._write(data)

    @property
    def stop(self):
        return self._read().get("stop", _backup_default_data["stop"])

    @stop.setter
    def stop(self, s):
        data = self._read()
        data["stop"] = s
        self._write(data)

    @property
    def num_states(self):
        return self._read().get("num_states", _backup_default_data["num_states"])

    @num_states.setter
    def num_states(self, num):
        data = self._read()
        data["num_states"] = num
        self._write(data)

    @property
    def num_dimensions(self):
        return  self._read().get("num_dimensions", _backup_default_data["num_dimensions"])

    @num_dimensions.setter
    def num_dimensions(self, dim):
        data = self._read()
        data["num_dimensions"] = dim
        self._write(data)

    @property
    def num_samples(self):
        return self._read().get("num_samples", _backup_default_data["num_samples"])

    @num_samples.setter
    def num_samples(self, num):
        data = self._read()
        data["num_samples"] = num
        self._write(data)

    @property
    def num_iterations(self):
        return self._read().get("num_iterations", _backup_default_data["num_iterations"])

    @num_iterations.setter
    def num_iterations(self, num):
        data = self._read()
        data["num_iterations"] = num
        self._write(data)

    @property
    def plot_with_potential(self):
        return self._read().get("plot_with_potential", _backup_default_data["plot_with_potential"])

    @plot_with_potential.setter
    def plot_with_potential(self, v):
        data = self._read()
        data["plot_with_potential"] = v
        self._write(data)

    @property
    def plot_scale(self):
        return self._read().get("plot_scale", _backup_default_data["plot_scale"])

    @plot_scale.setter
    def plot_scale(self, sc):
        data = self._read()
        data["plot_scale"] = sc
        self._write(data)


def write_default():
    json_dat = JsonData("default_data.json")
    json_dat._write(_backup_default_data)
    # write_data("Linear Harmonic Oscillator", -10, 10, 1, 1, 100, 5, False, 10, filename="default_data.json")


def read_default():
    json_data = JsonData("default_data.json")
    try:
        return json_data._read()
    except json.JSONDecodeError as json_decoder_error:
        write_default()
        return json_data._read()