# Part C — Box program

Create your `Box.asm` here after entering your real K value in `Part_B/project_config.py`.
Do not assemble a sample K: the position and width must match your own roll number.

Assignment requirements:

- While any key is pressed, show a black box.
- When the key is released, erase the box.
- Start at screen row `K`.
- Height: 20 rows.
- Width: `16 * ((K % 4) + 1)` pixels, from the left edge.
- One screen row contains 32 words; one word represents 16 pixels.
- Row `r` starts at `SCREEN + 32*r`.

Suggested development order from the assignment: one dash → wider dash → box with a loop → add the key check.

When finished, generate `Box.hack` using your own `Part_B/assembler.py`, then run it in the official
CPU Emulator and capture a screenshot.
