# Cell Game Scripter — First Vertical Slice

## Goal

> A Python application creates or loads a small grid, runs a C implementation of Conway's Game of Life, reads several calculated generations, and visualizes the result.

## Scope Constraints

- [ ] Use Conway's Game of Life rules only
- [ ] Do not implement custom rules yet
- [ ] Do not implement the visual rule editor yet
- [ ] Use a standalone C executable
- [ ] Use files for Python ↔ C data exchange
- [ ] Store full generation snapshots instead of diffs
- [ ] Keep the UI minimal

## C Engine

- [ ] Define a simple cell representation
- [ ] Define a simple 2D grid representation
- [ ] Implement grid creation
- [ ] Implement grid cleanup
- [ ] Implement neighbor counting
- [ ] Implement Conway transition rules
- [ ] Implement `current_grid` and `next_grid`
- [ ] Implement generation swapping
- [ ] Decide first-slice boundary behavior
- [ ] Run the simulation for a specified number of generations
- [ ] Return exit code `0` on success
- [ ] Return non-zero exit codes on failure

## Input Format

- [ ] Define a minimal input format
- [ ] Store grid width
- [ ] Store grid height
- [ ] Store initial cell states
- [ ] Store requested generation count
- [ ] Document the format

Conceptually:

```text
width
height
generation_count
initial_grid
```

## Output Format

- [ ] Define a minimal result format
- [ ] Store generation number
- [ ] Store complete grid state for each generation
- [ ] Make the format easy for Python to parse
- [ ] Document the format
- [ ] Produce deterministic output

## Python Integration

- [ ] Create or load an initial grid
- [ ] Write the C engine input file
- [ ] Start the C executable
- [ ] Pass input and output paths
- [ ] Wait for the executable to finish
- [ ] Check its exit status
- [ ] Show a useful error when execution fails
- [ ] Read the generated result file
- [ ] Convert the result into Python generation objects

## Minimal UI

- [ ] Create the application window
- [ ] Display a small cell grid
- [ ] Allow cells to be toggled alive/dead
- [ ] Add a `Run` button
- [ ] Run the C simulation when the button is pressed
- [ ] Display the returned generation
- [ ] Add `Previous` and `Next` generation controls
- [ ] Display the current generation number

## First-Slice Test Patterns

- [ ] Empty grid
- [ ] Single live cell
- [ ] 2×2 block
- [ ] Blinker
- [ ] One manually calculated small pattern

## Integration Checks

- [ ] Python can successfully launch the compiled C executable
- [ ] C can read Python-generated input
- [ ] C produces valid output
- [ ] Python can parse C-generated output
- [ ] UI can visualize parsed output
- [ ] Multiple generations can be navigated
- [ ] Failed C execution does not crash the Python UI

## Definition of Done

- [ ] A user can define a small initial grid
- [ ] Python sends that grid to the C engine
- [ ] C calculates multiple Conway generations
- [ ] Python receives the result
- [ ] The application displays the generations
- [ ] Blinker behaves correctly
- [ ] The entire flow works from a clean application start without manual intermediate steps

## First Vertical Slice Pipeline

```text
UI
 ↓
Python data
 ↓
input file
 ↓
C engine
 ↓
result file
 ↓
Python parser
 ↓
visualization
```

Once this pipeline works, custom rules, rule serialization, the visual rule builder, richer cell states, and other features can be added on top of an already working system.
