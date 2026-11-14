# Nand2Tetris Capstone Starter (VS Code)

This is a starter workspace for the assignment **Make the Computer Draw a Box**.
It is not a completed submission: copy in your own working HDL chips from your labs,
set your personal `K` value, and finish/test `Box.asm` for your roll number.

## What's included

- `Part_A/README.md`: what to copy into the HDL section and how to test it.
- `Part_B/assembler.py`: a two-pass Hack assembler supporting A-instructions,
  C-instructions, predefined symbols, labels, and variables.
- `Part_B/project_config.py`: set your personal `K` value here.
- `Part_B/samples/Add.asm`: a small sample input to check the assembler.
- `Part_C/README.md`: the box requirements and implementation checklist.
- `.vscode/extensions.json`: recommends Microsoft's Python extension.

## 1. Open in VS Code

1. Extract this ZIP file.
2. Open VS Code and select **File → Open Folder**.
3. Select the extracted `Nand2Tetris_Capstone_Starter` folder.
4. Install the recommended Python extension when VS Code prompts you.

## 2. Check Python

Open **Terminal → New Terminal**, then run:

```powershell
py --version
```

If `py` is not recognized, try `python --version`. Install Python 3 if neither command works.
The VS Code extension does not install the Python interpreter itself.

## 3. Set your K value

Open `Part_B/project_config.py` and replace `None` with the last two digits of your roll number.
For example, if your roll number ends in `41`, use:

```python
K = 41
```

Do not use the example value unless it is actually your K.

## 4. Test the sample assembler

From the workspace root, run:

```powershell
py Part_B/assembler.py Part_B/samples/Add.asm Part_B/samples/Add.hack
```

The output should be created at `Part_B/samples/Add.hack`.
Compare it with the result from the official Nand2Tetris assembler. For the assignment,
also test using the official `Max.asm`, `Rect.asm`, and `Pong.asm` files supplied to you.

You can pass K directly instead of editing the config file:

```powershell
py Part_B/assembler.py Part_B/samples/Add.asm Part_B/samples/Add.hack --k 41
```

## 5. Part A and Part C

- Copy your own completed `CPU.hdl`, `Memory.hdl`, and `Computer.hdl` into `Part_A/`.
  Use the official Hardware Simulator and the five test scripts listed in your assignment.
- Implement `Part_C/Box.asm` using your actual K. Assemble it with this Python assembler,
  then open the resulting `.hack` file in the official CPU Emulator.
- Capture the test and emulator screenshots for the 3–4 page report.

## Important

The assignment specifies one extra assembler feature based on `K % 3`:

- `0`: write labels and variables with their addresses to `symbols.txt`.
- `1`: give a clear invalid-instruction error with its source line number.
- `2`: warn when a label is defined more than once.

This starter implements the corresponding behavior when K is set. Review the code and be
prepared to explain it in your viva. Always verify that your generated `.hack` files match
the official assembler's output.
