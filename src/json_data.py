import json

#default_data = {"label":"Linear Harmonic Oscillator",
#                "start":-10,
#                "stop":10,
#                "num_states":1,
#                "dimensions":1,
#                "samples":100,
#                "iterations":5,
#                "plot_with_potential":false,
#                "plot_scale":10
#                }


def write_data(label, start, stop, num_states, num_dimensions, num_samples, num_iterations, plot_with_potential, plot_scale):
        data = {"label":label,
                "start":start,
                "stop":stop,
                "num_states":num_states,
                "dimensions":num_dimensions,
                "samples":num_samples,
                "iterations":num_iterations,
                "plot_with_potential":plot_with_potential,
                "plot_scale":plot_scale
                }
        with open("data.json", "w", encoding="utf-8") as data_file:
                dump = json.dumps(data, indent=4, separators=(",", ": "), ensure_ascii=False)
                data_file.write(dump)


def write_default():
        write_data("Linear Harmonic Oscillator", -10, 10, 1, 1, 100, 5, False, 10)


def read_data():
        with open("data.json") as data_file:
                try:
                    json_data = json.load(data_file)
                except:
                        raise
                return json_data


if __name__ == "__main__":
        #write_default()
        data = read_data()
        print(data)

