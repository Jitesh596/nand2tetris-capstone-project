# Part C — Generate the personalized Box program

The assignment requires the box position and width to depend on your personal `K` value (the last two digits of your roll number). Since K is student-specific, a generic Box.hack must not be submitted as your final output.

## Generate Box.asm and Box.hack

1. Set your actual `K` in the parent `Project Files/project_config.py`, or pass it directly as an argument.
2. Open the parent `Project Files` folder in VS Code.
3. In the terminal, run one of these commands:

```powershell
py Pending-Part-C-Box/generate_box.py
```

or, without editing `project_config.py`:

```powershell
py Pending-Part-C-Box/generate_box.py --k 41
```

Replace `41` with your own K. The script generates `Box.asm` and uses the parent folder's `assembler.py` to generate `Box.hack`.

## Required behavior

- Starts at row K.
- Is 20 rows tall.
- Is `16 * ((K % 4) + 1)` pixels wide.
- Starts at the left edge of the screen.
- Draws while any key is pressed and clears the same area after release.

## Final verification

Open the generated `Box.hack` in the official Nand2Tetris CPU Emulator. Test both key press and key release, and take a genuine screenshot for your report. Do not submit the example command's K value unless it is actually yours.
