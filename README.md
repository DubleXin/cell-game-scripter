# Cell Game Scripter

Cell Game Scripter is a small cellular automata project with a Python UI and a simulation engine written in C.

The application allows you to:

- configure the initial grid size;
- toggle cells between alive and dead states;
- configure the number of generations;
- define simple custom simulation rules;
- run the C simulation engine;
- inspect generated generations using Previous, Next, Play/Pause, Reset, and playback speed controls.

## Tech Stack

The project uses:

- **Python** for the application layer and UI;
- **Tkinter / ttk** for the graphical interface;
- **C** for the cellular automata simulation engine;
- **Make** for building and running the project.

### Tkinter / ttk

`ttk` is part of Python's Tkinter package, but Tkinter may need to be installed separately as a system dependency.

On Fedora:

```bash
sudo dnf install python3-tkinter
```

You can verify the installation with:

```bash
python3 -m tkinter
```

## Build and Run

The project includes a `Makefile`.

Build the C engine:

```bash
make build
```

Run the application:

```bash
make run
```

`make run` starts the Python application and uses the compiled C engine during simulations.

## Architecture

The project is split into two main parts:

```text
Python application
        |
        | writes simulation input and rules
        | starts the engine
        v
C simulation engine
        |
        | calculates generations
        | writes simulation output
        v
Python application
```

The Python process owns the UI, application state, serialization, and interaction with the engine.

The C process is responsible for reading the provided grid and rules, applying the cellular automata rules, and producing the resulting generations.

The two parts communicate through files stored in the project's data directory.

## Rules

Cells have two possible states:

```text
0 = dead
1 = alive
```

Rules can depend on:

- the number of alive cells in the configured neighborhood;
- the state of a specific neighboring cell.

If no rule matches a cell, its current state is preserved.

The neighborhood size and rules can be configured through the Rules tab.
