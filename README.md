# Terrarium Microverse App 🌿

Welcome to the **Terrarium Microverse**. This project intends to create an interactive simulation of a terrarium-like environment, featuring dynamically behaving "creatures", decorations, food sources, and ambient lighting. Built with **Python** and **PyQt5**, it's used mostly as a testing field to learn more on the topic of multithreading & FMI standard use.

![Simulation Example](assets/simulation_example_v11.jpg)

⚠️ **This project is in its raw, early stages. Expect plenty of obvious errors and rough edges.** Feedback, contributions, and suggestions are welcome to help polish it into something amazing & useful.

---

## Features 🚀

- **Dynamic Creatures**: Simulated entities like "BlueCell" & "GreenCell" with behavior influenced by hunger, boundaries, and interactions.
- **Terrarium Environment**: Includes decorations, lighting effects, and a customizable boundary.
- **Interactive Simulation**: Real-time updates supporting FMU-based (Functional Mock-up Unit) physics-driven behavior.

---

## Getting Started 🛠️

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/raccoon-hero/terrarium-microverse.git
    cd terrarium-microverse
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add FMU Files**:
    - Place required `.fmu` files for creatures in the `fmus/` directory. See the **FMU Configuration** section below for details.

4. **Run the simulation**:
    ```bash
    python main.py
    ```

---

## Project Structure 📂

```plaintext
src/
├── environment/
│   ├── BoundaryModule.py       # Defines the simulation boundary
│   ├── DecorationModule.py     # Handles decorations in the terrarium
│   ├── FoodModule.py           # Adds and manages food sources
│   ├── LightingModule.py       # Creates dynamic lighting effects
├── creatures/
│   ├── BlueCell.py             # A simulated creature with FMU-based logic
│   └── GreenCell.py            # Another simulated creature (not implemented here)
├── simulation/
│   ├── simulation_manager.py   # Core logic to manage the simulation
│   ├── thoughts_manager.py     # Tracks creature thoughts and displays them
├── ui/
│   ├── MainWindow.py           # The main UI interface
│   └── CreatureStatusWidget.py # (not used) Displays creature-specific stats
main.py                         # Entry point to start the simulation
requirements.txt                # Python dependencies
```

---

## FMU Configuration 📦

This simulation relies on **FMU files** for dynamic creature behavior, and has corresponding **Modelica source files** (`.mo`) for testing purposes. These `.fmu` files are necessary for the proper functioning of the creatures and should be organized as follows:

```plaintext
fmus/
├── BlueCell/
│   ├── BlueCell.fmu   # Precompiled Functional Mock-up Unit for BlueCell
│   ├── BlueCell.mo    # Modelica source code for BlueCell (optional, for further customization)
└─── GreenCell/
    ├── GreenCell.fmu  # Precompiled Functional Mock-up Unit for GreenCell
    ├── GreenCell.mo   # Modelica source code for GreenCell (optional, for further customization)
```


### How to Get FMUs and Modelica Files

1. If the `.fmu` and `.mo` files are already provided, place them in the `fmus/` directory as shown above.
2. To customize or create new `.fmu` files, you can edit the `.mo` files and use a Modelica-compatible tool like **OpenModelica** or **Dymola** to generate the `.fmu` files.

### Using FMU Files in the Simulation

The FMU files are loaded during runtime to simulate creature behavior. Ensure that the paths to these files are correctly configured in the project. The simulation manager uses these files to create instances of the creatures (e.g., `BlueCell` and `GreenCell`) with physics-based behaviors.

If you're unfamiliar with FMUs or the **FMI (Functional Mock-up Interface)** standard, visit the [FMI website](https://fmi-standard.org/) for more details.

---


---

## Known Issues and Todos 🐛

- **Error Handling**: Hardcoded file paths and lack of robust validation may cause crashes.
- **Performance**: Heavy use of real-time visual effects can lead to lag even in small simulations.
- **Thread Safety**: Some shared resources (e.g., `ThoughtsManager`) need locks for concurrent access.
- **UI Scaling**: The PyQt5 UI wasn't adapted for screen rescaling.

Contributions to address these issues are highly appreciated.

---

## Contributing 🤝

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.
