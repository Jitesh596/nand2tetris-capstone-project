# Nand2Tetris Capstone — Project Files

This package follows the teacher's requested structure:

```text
3. Capstone Project/
  YourName_YourRollNo_ProjectReport_TEMPLATE.pdf
  Project Files/
    assembler.py
    project_config.py
    Assembler_SmokeTest.asm
    Assembler_SmokeTest.hack
    Pending-Part-A-HDL/
      CPU.hdl
      Memory.hdl
      Computer.hdl
    Pending-Part-C-Box/
      generate_box.py
```

## Run the Python assembler smoke test

Open this `Project Files` folder in VS Code, then run in its terminal:

```powershell
py assembler.py Assembler_SmokeTest.asm Assembler_SmokeTest.hack
```

## Part A — HDL

The `Pending-Part-A-HDL` folder now contains `CPU.hdl`, `Memory.hdl`, and `Computer.hdl` implementations. Open them in the official Nand2Tetris Hardware Simulator and run all five assignment tests:

- `CPU.tst`
- `Memory.tst`
- `ComputerAdd.tst`
- `ComputerMax.tst`
- `ComputerRect.tst`

Save actual screenshots of your test results. The HDL source files are provided, but no claim is made that they have passed in your course's simulator environment. Ensure the chip dependencies from your lab workspace are available. If you use a built-in chip in place of your own lab chip, disclose that in the report.

## Part B — assembler

`assembler.py` is a two-pass Hack assembler. Test it against the official `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` files and compare each output against the official assembler. The included smoke test is only an initial check, not a substitute for the four required tests.

Set `K` in `project_config.py` to the last two digits of your own roll number. The required extra feature is selected by `K % 3`:

- `0`: write labels and variables to `symbols.txt`.
- `1`: report invalid instructions with source line numbers.
- `2`: warn when a label is defined more than once.

## Part C — personalized Box program

The assignment's box dimensions depend on your personal K. To generate the correct `Box.asm` and assemble it into `Box.hack`:

1. Set your actual K in `project_config.py`, or pass it with `--k`.
2. Run:

```powershell
py Pending-Part-C-Box/generate_box.py
```

Or provide K directly:

```powershell
py Pending-Part-C-Box/generate_box.py --k 41
```

Replace `41` with your own K. The generator creates `Box.asm` and `Box.hack` in `Pending-Part-C-Box` using the parent `assembler.py`. Then open `Box.hack` in the official CPU Emulator and test both key press and key release. Save a genuine screenshot of the final display.

## Before final submission

- Replace the report template with your actual name and roll number, and rename it to the teacher's required `Name_RollNo_ProjectReport.pdf` format.
- Complete the report with your K, dimensions, actual test screenshots, final box screenshot, and the required paragraph about a mistake you fixed.
- Verify your HDL tests, all four assembler comparison programs, and the box program.
- Do not submit placeholder or unverified screenshots as real test evidence.
