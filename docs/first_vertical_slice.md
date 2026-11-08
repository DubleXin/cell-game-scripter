# Cell Game Scripter — First Vertical Slice

## Goal

> A Python application creates or loads a small grid, runs a C implementation of Conway's Game of Life, reads several calculated generations, and visualizes the result.

## Scope Constraints

- [x] Use Conway's Game of Life rules only
- [x] Do not implement custom rules yet
- [x] Do not implement the visual rule editor yet
- [x] Use a standalone C executable
- [x] Use files for Python ↔ C data exchange
- [x] Store full generation snapshots instead of diffs
- [ ] Keep the UI minimal

## C Engine

- [x] Define a simple cell representation
- [x] Define a simple 2D grid representation
- [x] Implement grid creation
- [x] Implement grid cleanup
- [x] Implement neighbor counting
- [x] Implement Conway transition rules
- [x] Implement `current_grid` and `next_grid`
- [x] Implement generation swapping
- [x] Decide first-slice boundary behavior
- [x] Run the simulation for a specified number of generations
- [x] Return exit code `0` on success
- [x] Return non-zero exit codes on failure

## Input Format

- [x] Define a minimal input format
- [x] Store grid width
- [x] Store grid height
- [x] Store initial cell states
- [x] Store requested generation count
- [x] Document the format

Conceptually:

```text
width
height
generation_count
initial_grid
```

## Output Format

- [x] Define a minimal result format
- [x] Store generation number
- [x] Store complete grid state for each generation
- [x] Make the format easy for Python to parse
- [x] Document the format
- [x] Produce deterministic output

## Python Integration

- [x] Create or load an initial grid
- [x] Write the C engine input file
- [x] Start the C executable
- [x] Pass input and output paths
- [x] Wait for the executable to finish
- [x] Check its exit status
- [ ] Show a useful error when execution fails
- [ ] Read the generated result file
- [x] Convert the result into Python generation objects

## Minimal UI

- [x] Create the application window
- [x] Display a small cell grid
- [x] Allow cells to be toggled alive/dead
- [x] Add a `Run` button
- [x] Run the C simulation when the button is pressed
- [x] Display the returned generation
- [x] Add `Previous` and `Next` generation controls
- [x] Display the current generation number

## First-Slice Test Patterns

- [x] Empty grid
- [x] Single live cell
- [x] 2×2 block
- [x] Blinker
- [x] One manually calculated small pattern

## Integration Checks

- [x] Python can successfully launch the compiled C executable
- [x] C can read Python-generated input
- [x] C produces valid output
- [x] Python can parse C-generated output
- [x] UI can visualize parsed output
- [x] Multiple generations can be navigated
- [x] Failed C execution does not crash the Python UI

## Definition of Done

- [x] A user can define a small initial grid
- [x] Python sends that grid to the C engine
- [x] C calculates multiple Conway generations
- [x] Python receives the result
- [x] The application displays the generations
- [x] Blinker behaves correctly
- [x] The entire flow works from a clean application start without manual intermediate steps

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
