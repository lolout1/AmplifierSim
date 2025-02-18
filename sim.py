#!/usr/bin/env python3
"""
sim.py

Simulates two amplifier circuits using PySpice:
  1. A Common-Emitter Amplifier (BJT)
  2. A Differential Amplifier (BJT pair)

Requirements:
  • Ngspice (v44.2) must be built as a shared library and installed.
  • The following environment variables should be set:
        export NGSPICE_SHARED_LIBRARY=/usr/local/lib/ngspice/libngspice.so
        export LD_LIBRARY_PATH=/usr/local/lib/ngspice:$LD_LIBRARY_PATH
        export NGSPICE_VERSION_OVERRIDE=44.2
  • Python packages: PySpice, matplotlib, numpy, and (optionally) schemdraw for drawing diagrams.

Usage:
    python3 sim.py
"""

import matplotlib.pyplot as plt
import numpy as np

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_V, u_kΩ, u_Hz, u_MHz

# Try to import schemdraw for circuit diagram drawing.
try:
    import schemdraw
    import schemdraw.elements as elm
    schemdraw_available = True
except ImportError:
    schemdraw_available = False
    print("schemdraw not installed. To draw circuit diagrams, install it with 'pip install schemdraw'.")

def draw_common_emitter_circuit():
    """Draw a simple schematic of the common-emitter amplifier using schemdraw."""
    if not schemdraw_available:
        print("schemdraw not available, skipping circuit diagram.")
        return

    d = schemdraw.Drawing(unit=1)
    d += elm.SourceV().label('12V\nVcc', loc='top').up()  # Voltage source (Vcc)
    d += elm.Resistor().label('100kΩ\nR1', loc='right').right()  # R1 from Vcc to base
    # Draw transistor (using BJT symbol from schemdraw; the element name might vary with version)
    # In current schemdraw versions, use elm.BjtNpn() for an NPN transistor.
    d += elm.BjtNpn().label('2N3904\nQ1', loc='right')
    d += elm.Resistor().label('1kΩ\nR4', loc='right').down()  # Emitter resistor
    d += elm.Ground()
    d.draw()

def simulate_common_emitter():
    # Build the Common-Emitter Amplifier circuit.
    circuit = Circuit('Common-Emitter Amplifier')

    # Supply voltage at Vcc.
    circuit.V(1, 'Vcc', circuit.gnd, 12 @ u_V)

    # Create an input voltage source for the base.
    # Use a unique name (e.g., "Vin") and store the returned object.
    vin_source = circuit.V('Vin', 'base', circuit.gnd, 0 @ u_V)
    # Set AC amplitude separately.
    vin_source.ac = 1 @ u_V

    # Bias and load resistors.
    circuit.R(1, 'Vcc', 'base', 100 @ u_kΩ)
    circuit.R(2, 'base', circuit.gnd, 10 @ u_kΩ)
    circuit.R(3, 'Vcc', 'collector', 4.7 @ u_kΩ)
    circuit.R(4, 'emitter', circuit.gnd, 1 @ u_kΩ)

    # Transistor Q1: 2N3904 (NPN)
    circuit.Q(1, 'collector', 'base', 'emitter', model='2N3904')
    circuit.model('2N3904', 'NPN', BF=100)

    print("\n--- Common-Emitter Amplifier Netlist ---")
    print(circuit)

    # Run an AC analysis.
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=10 @ u_Hz,
                             stop_frequency=100 @ u_MHz,
                             number_of_points=100,
                             variation='dec')

    frequency = analysis.frequency.as_ndarray()
    try:
        collector_voltage = analysis['collector'].as_ndarray()
    except KeyError:
        print("Warning: Node 'collector' not found; using zeros.")
        collector_voltage = np.zeros_like(frequency)

    epsilon = 1e-12  # to avoid log(0)
    gain_dB = 20 * np.log10(np.abs(collector_voltage) + epsilon)

    # Plot the AC gain (Bode plot).
    plt.figure()
    plt.semilogx(frequency, gain_dB)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Gain [dB]')
    plt.title('Common-Emitter Amplifier AC Analysis')
    plt.grid(True)
    plt.show()

def simulate_differential_amplifier():
    # Build the Differential Amplifier circuit.
    circuit = Circuit('Differential Amplifier')

    circuit.V(1, 'Vcc', circuit.gnd, 12 @ u_V)
    circuit.R(1, 'E', circuit.gnd, 1 @ u_kΩ)
    circuit.Q(1, 'collector1', 'base1', 'E', model='2N3904')
    circuit.Q(2, 'collector2', 'base2', 'E', model='2N3904')
    circuit.R(2, 'Vcc', 'collector1', 4.7 @ u_kΩ)
    circuit.R(3, 'Vcc', 'collector2', 4.7 @ u_kΩ)
    circuit.R(4, 'Vcc', 'base1', 100 @ u_kΩ)
    circuit.R(5, 'base1', circuit.gnd, 10 @ u_kΩ)
    circuit.R(6, 'Vcc', 'base2', 100 @ u_kΩ)
    circuit.R(7, 'base2', circuit.gnd, 10 @ u_kΩ)
    circuit.model('2N3904', 'NPN', BF=100)

    print("\n--- Differential Amplifier Netlist ---")
    print(circuit)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=10 @ u_Hz,
                             stop_frequency=100 @ u_MHz,
                             number_of_points=100,
                             variation='dec')

    frequency = analysis.frequency.as_ndarray()
    try:
        collector1_voltage = analysis['collector1'].as_ndarray()
    except KeyError:
        print("Warning: Node 'collector1' not found; using zeros.")
        collector1_voltage = np.zeros_like(frequency)
    try:
        collector2_voltage = analysis['collector2'].as_ndarray()
    except KeyError:
        print("Warning: Node 'collector2' not found; using zeros.")
        collector2_voltage = np.zeros_like(frequency)

    epsilon = 1e-12
    gain1_dB = 20 * np.log10(np.abs(collector1_voltage) + epsilon)
    gain2_dB = 20 * np.log10(np.abs(collector2_voltage) + epsilon)

    # Plot the AC gains for both outputs.
    plt.figure()
    plt.semilogx(frequency, gain1_dB, label='Collector 1')
    plt.semilogx(frequency, gain2_dB, label='Collector 2')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Gain [dB]')
    plt.title('Differential Amplifier AC Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    print("Simulating Common-Emitter Amplifier...")
    simulate_common_emitter()

    print("Drawing Common-Emitter Amplifier circuit diagram (if available)...")
    draw_common_emitter_circuit()

    print("Simulating Differential Amplifier...")
    simulate_differential_amplifier()

