
---

```markdown
# AmplifierSim

**AmplifierSim** is a simulation repository that demonstrates how to simulate analog amplifier circuits using [PySpice](https://pyspice.fabrice-salvaire.fr/) with Ngspice as a shared library. This repository includes two example circuits:

1. A **Common-Emitter Amplifier** (BJT)
2. A **Differential Amplifier** (BJT pair)

It also includes a discussion of op-amp concepts (which are not yet implemented in simulation) and a collection of build/patch scripts to compile and install Ngspice as well as to patch PySpice's version check.

> **Note:**  
> PySpice may reject Ngspice version 44.x by default. You can either upgrade Ngspice (to a newer branch) or patch PySpice to override the version check. This repository demonstrates the patch method.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [1. Build and Install Ngspice](#1-build-and-install-ngspice)
  - [2. Patch PySpice for Ngspice 44.2](#2-patch-pyspice-for-ngspice-442)
  - [3. Set Environment Variables](#3-set-environment-variables)
- [Concepts and Theory](#concepts-and-theory)
  - [Common-Emitter Amplifier](#common-emitter-amplifier)
  - [Differential Amplifier](#differential-amplifier)
  - [Op Amp Overview](#op-amp-overview)
- [Repository Structure](#repository-structure)
- [Simulation Scripts](#simulation-scripts)
- [Circuit Diagrams](#circuit-diagrams)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Ngspice Integration:** Uses Ngspice as a shared library for circuit simulations.
- **Circuit Examples:** Provides netlists and simulations for a common-emitter amplifier and a differential amplifier.
- **Theory Overview:** Includes formatted formulas and conceptual overviews for both amplifier types.
- **Op Amp Concepts:** Contains a section discussing op amp fundamentals (to be implemented in future versions).
- **Automated Build:** Provides shell scripts (`build_ngspice.sh` and `patch_and_run.sh`) to update, build, and install Ngspice and to patch PySpice.
- **Visualization:** Uses Matplotlib for plotting AC gain (Bode plots).

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.10+**
- **PySpice:** Install using `pip install PySpice`
- **Ngspice:** This will be built and installed from source using the provided script.
- **Build Tools and Dependencies:** (for Ubuntu/Debian)

  ```bash
  sudo apt update
  sudo apt install -y build-essential bison flex libx11-dev libxaw7-dev libxmu-dev libxext-dev libreadline-dev autoconf automake libtool git
  ```

- **Matplotlib and NumPy:** For plotting and numerical operations.
  
  ```bash
  pip install matplotlib numpy
  ```

- **Schemdraw (optional):** For drawing circuit diagrams.
  
  ```bash
  pip install schemdraw
  ```

---

## Installation and Setup

### 1. Build and Install Ngspice

The provided script `build_ngspice.sh` (located in the repository root) performs the following tasks:

- Updates package lists and installs required build dependencies.
- Clones (or updates) the Ngspice repository (default version is v44.2).
- Runs `./autogen.sh`, creates a build directory (`release`), and configures the build with options such as `--with-x`, `--enable-cider`, and `--enable-predictor`.
- Compiles Ngspice using `make -j4` and installs it with `sudo make install` and `sudo ldconfig`.
- Adds `/usr/local/lib/ngspice` to the system’s linker configuration.

If a newer stable branch (e.g., `NGSPICE_REWORK_15`) becomes available, you can modify the checkout command in the script accordingly.

### 2. Patch PySpice for Ngspice 44.2

Since PySpice may raise an error for version 44.x, the `patch_and_run.sh` script locates the PySpice file `PySpice/Spice/NgSpice/Shared.py` in your site-packages, creates a backup, and comments out the version-check lines.

To manually patch, open the file (for example, `/home/username/.local/lib/python3.10/site-packages/PySpice/Spice/NgSpice/Shared.py`), find the code that looks like:

```python
if self.version.startswith('44'):
    raise Exception("Unsupported Ngspice version 44")
```

and comment it out:

```python
# if self.version.startswith('44'):
#     raise Exception("Unsupported Ngspice version 44")
```

### 3. Set Environment Variables

Set the following environment variables (add these to your `~/.bashrc` or `~/.profile`):

```bash
export NGSPICE_SHARED_LIBRARY=/usr/local/lib/ngspice/libngspice.so
export LD_LIBRARY_PATH=/usr/local/lib/ngspice:$LD_LIBRARY_PATH
export NGSPICE_VERSION_OVERRIDE=44.2
```

Then update your current session:

```bash
source ~/.bashrc
```

---

## Concepts and Theory

### Common-Emitter Amplifier

The **common-emitter amplifier** is one of the most widely used configurations in BJT amplifier circuits. Its main features include:

- **Voltage Gain (Approximate):**

  $$
  A_v \approx -\frac{R_C}{R_E}
  $$

  where:
  - \( R_C \) is the collector resistor.
  - \( R_E \) is the emitter resistor (if present; if bypassed, gain increases).

- **Input and Output Impedances:**  
  The input impedance is determined by the biasing network and the transistor’s base resistance, while the output impedance is primarily \( R_C \).

- **Phase Inversion:**  
  The negative sign in the gain indicates that the output signal is 180° out of phase with the input.

### Differential Amplifier

The **differential amplifier** uses a pair of matched transistors to amplify the difference between two input signals. Key concepts include:

- **Differential Gain:**

  $$
  A_d \approx \frac{R_C}{2R_E}
  $$

  where:
  - \( R_C \) is the collector resistor (assumed equal for both transistors).
  - \( R_E \) is the shared emitter resistor.

- **Common-Mode Rejection Ratio (CMRR):**  
  The ability of the amplifier to reject signals common to both inputs. A high CMRR is desirable in differential applications.

- **Biasing:**  
  Proper biasing is crucial to ensure both transistors operate in the active region and to minimize mismatches.

### Op Amp Overview (Concepts Not Yet Implemented)

While the current repository does not simulate op amp circuits, here are key concepts:

- **Ideal Op Amp Assumptions:**
  - Infinite open-loop gain.
  - Infinite input impedance.
  - Zero output impedance.
  - Zero offset voltage.

- **Common Configurations:**
  - **Inverting Amplifier:**

    $$
    A_v = -\frac{R_f}{R_{in}}
    $$

  - **Non-Inverting Amplifier:**

    $$
    A_v = 1 + \frac{R_f}{R_{in}}
    $$

- **Practical Considerations:**  
  Real op amps have finite gain, bandwidth, and slew rate. Future versions of this project may simulate these non-ideal behaviors.

---

## Repository Structure

```
AmplifierSim/         # Contains simulation examples and netlist scripts
├── sim.py            # Main simulation script for amplifier circuits
├── requirements.txt  # Python dependencies (PySpice, matplotlib, etc.)
build_ngspice.sh      # Script to build and install Ngspice from source
patch_and_run.sh      # Script to patch PySpice’s Ngspice version check and run simulations
ngspice/              # (Optional) local clone of the Ngspice repository
README.md             # This file
```

---

## Simulation Scripts

### Common-Emitter Amplifier

The `simulate_common_emitter()` function in `sim.py` builds a common-emitter amplifier circuit that includes:
- A DC supply (12 V)
- An input voltage source at the base with AC excitation
- Biasing resistors and collector/emitter resistors
- A 2N3904 transistor with a simple NPN model (`BF=100`)

It then performs an AC analysis from 10 Hz to 100 MHz, calculates the voltage gain (in dB), and displays a Bode plot.

### Differential Amplifier

The `simulate_differential_amplifier()` function builds a differential amplifier with:
- A common supply (12 V)
- A shared emitter resistor for biasing
- A pair of 2N3904 transistors forming the differential pair
- Bias resistors for each transistor

An AC analysis is performed on both collector nodes, and their gains are plotted.

---

## Circuit Diagrams

*Optional:* If you have `schemdraw` installed, you can generate schematic diagrams. For example, the following function (not included in the simulation by default) shows how to draw a common-emitter amplifier schematic:

```python
import schemdraw
import schemdraw.elements as elm

def draw_common_emitter_circuit():
    d = schemdraw.Drawing()
    d += elm.SourceV().label('12V\nVcc', loc='top')
    d.push()  # Save position
    d += elm.Resistor().down().label('100kΩ', loc='right')
    d.pop()   # Return to saved position
    d += elm.Resistor().right().label('10kΩ', loc='bottom')
    d += elm.TransistorNpn().label('2N3904\nQ1', loc='right')
    d.draw()
```

Call this function (for example, at the beginning of `simulate_common_emitter()`) to view the schematic.

---

## Troubleshooting

- **Ngspice Version Error:**  
  If you see an "Unsupported Ngspice version 44" error, make sure you have patched PySpice (using `patch_and_run.sh` or manually) and that `NGSPICE_VERSION_OVERRIDE` is set to `44.2`.

- **Node Not Found Errors:**  
  Verify that the node names in your netlist match those referenced in your simulation code. Adjust names accordingly.

- **Plotting/Display Issues on WSL:**  
  Set your `DISPLAY` environment variable appropriately (e.g., `export DISPLAY=:0`).

---

## Contributing

Contributions are welcome! If you have suggestions, find bugs, or wish to add new features (such as op-amp simulation), please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

---

