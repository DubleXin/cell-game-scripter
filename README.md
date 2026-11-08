# Cell Game Scripter — General Project Checklist

## Project Setup

- [ ] Create the project repository
- [ ] Define the project directory structure
- [ ] Add a basic README
- [ ] Add build/run instructions
- [ ] Decide how Python will invoke the C engine
- [ ] Decide where temporary and generated files will live
- [ ] Define basic error/exit codes for the C executable

## Python Application

- [ ] Choose a lightweight UI library
- [ ] Create the main application window
- [ ] Implement basic grid rendering
- [ ] Implement basic user interaction with the grid
- [ ] Add controls for starting and stopping a simulation
- [ ] Add generation navigation or playback
- [ ] Create a Python-side representation of the simulation configuration
- [ ] Add validation for configuration and input data

## C Simulation Engine

- [ ] Define the cell representation
- [ ] Define the grid representation
- [ ] Implement grid allocation and cleanup
- [ ] Implement reading the current generation
- [ ] Implement calculation of the next generation
- [ ] Keep the current generation immutable during next-generation calculation
- [ ] Implement `current_grid` / `next_grid` swapping
- [ ] Implement boundary behavior
- [ ] Implement standard Conway's Game of Life rules
- [ ] Add clear exit statuses for failures
- [ ] Compile the engine as a standalone executable

## Python ↔ C Integration

- [ ] Launch the C executable from Python
- [ ] Pass input/configuration file paths as command-line arguments
- [ ] Check the process exit status
- [ ] Capture useful error output
- [ ] Read simulation output after successful execution
- [ ] Handle missing or invalid output files
- [ ] Keep simulation data separate from process status/error reporting

## Simulation Data Format

- [ ] Define the initial-state format
- [ ] Define the simulation configuration format
- [ ] Define the result format
- [ ] Decide whether results store full snapshots or diffs
- [ ] Use full snapshots for the first implementation
- [ ] Document coordinate conventions
- [ ] Document grid dimensions
- [ ] Document generation numbering
- [ ] Document supported cell states

## Rule System

- [ ] Define the minimum rule model before choosing the final serialization format
- [ ] Define how neighbors are addressed
- [ ] Define the neighborhood size/radius
- [ ] Define available cell properties
- [ ] Define available comparison operators
- [ ] Define available actions
- [ ] Define rule evaluation order
- [ ] Define behavior when multiple rules match
- [ ] Define whether `AND`, `OR`, and `NOT` are supported
- [ ] Define whether rules may inspect the current cell
- [ ] Define whether rules may use aggregate values such as alive-neighbor count
- [ ] Design the serialized rule format
- [ ] Implement rule parsing in C
- [ ] Implement rule evaluation in C
- [ ] Validate invalid or unsupported rules

## Visual Rule Editor

- [ ] Create a UI for defining conditions
- [ ] Create a UI for selecting neighbor positions
- [ ] Create a UI for defining actions
- [ ] Create a UI for adding/removing rules
- [ ] Convert UI state into the internal rule model
- [ ] Serialize rules into the supported rule format
- [ ] Load existing rule files into the editor
- [ ] Validate rules before running the simulation

## Visualization

- [ ] Render the initial generation
- [ ] Render calculated generations
- [ ] Add next/previous generation controls
- [ ] Add automatic playback
- [ ] Add pause/reset controls
- [ ] Display the current generation number
- [ ] Handle simulation completion
- [ ] Handle malformed or incomplete result data

## Basic Tests

- [ ] Empty grid stays empty
- [ ] Stable pattern stays stable
- [ ] Blinker oscillates correctly
- [ ] Same input produces the same output
- [ ] Calculating the next generation does not mutate the current generation
- [ ] Python correctly detects successful C execution
- [ ] Python correctly detects failed C execution
- [ ] Result parsing works for known simulation output
- [ ] Rule parsing works for known valid rules
- [ ] Invalid rule input fails cleanly

## Release

- [ ] Run the project from a clean checkout
- [ ] Verify build instructions
- [ ] Verify run instructions
- [ ] Remove debug-only files/output
- [ ] Document known limitations
- [ ] Add one or more example simulations
- [ ] Add one or more example rule files
- [ ] Perform a final end-to-end test
