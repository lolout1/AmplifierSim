# AmplifierSim

**AmplifierSim** is a simulation repository that demonstrates the use of [PySpice](https://pyspice.fabrice-salvaire.fr/) together with Ngspice to simulate analog amplifier circuits. This repository currently includes two circuit examples:

1. A **Common-Emitter Amplifier** (BJT)
2. A **Differential Amplifier** (BJT Pair)

It also contains scripts to build the latest Ngspice from source, patch the PySpice version check (if using Ngspice 44.2), and then run the simulations.

> **Note:** Although Ngspice version 44.2 is the latest stable release, PySpice’s built‐in version check may reject it. Two approaches exist:
>
> 1. **Upgrade Ngspice:** Build and install a newer Ngspice (e.g., from a later branch such as `NGSPICE_REWORK_15` if available).
> 2. **Override the Version Check:** Patch PySpice’s `Shared.py` file to disable the check.
>
> This repository demonstrates the second option.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [1. Build and Install Ngspice](#1-build-and-install-ngspice)
  - [2. Patch PySpice for Ngspice 44.2](#2-patch-pyspice-for-ngspice-442)
  - [3. Set Environment Variables](#3-set-environment-variables)
- [Repository Structure](#repository-structure)
- [Simulation Scripts](#simulation-scripts)
  - [Common-Emitter Amplifier](#common-emitter-amplifier)
  - [Differential Amplifier](#differential-amplifier)
- [Circuit Diagrams](#circuit-diagrams)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Ngspice Integration:** Uses Ngspice as a shared library.
- **Circuit Examples:** Includes netlists for a common-emitter amplifier and a differential amplifier.
- **Automated Build:** Provides a shell script (`build_ngspice.sh`) to update/build/install Ngspice from source.
- **Patch Support:** Contains a script (`patch_and_run.sh`) that patches PySpice’s version check to allow Ngspice version 44.2.
- **Visualization:** Uses matplotlib to plot AC gain (Bode plots).

---

## Prerequisites

Before you begin, ensure you have installed:

- **Python 3.10+**
- **PySpice:** Install using `pip install PySpice`
- **Ngspice:** You will build and install this from source (see below).
- **Build Tools and Dependencies:** (for Ubuntu/Debian)

  ```bash
  sudo apt update
  sudo apt install -y build-essential bison flex libx11-dev libxaw7-dev libxmu-dev libxext-dev libreadline-dev autoconf automake libtool git

