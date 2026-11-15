#!/usr/bin/env python3
"""Generate the K-specific Box.asm and assemble Box.hack for the capstone."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_FILES = Path(__file__).resolve().parents[1]
ASSEMBLER = PROJECT_FILES / "assembler.py"


def load_config_k() -> int | None:
    sys.path.insert(0, str(PROJECT_FILES))
    try:
        from project_config import K  # type: ignore
        return K
    except Exception:
        return None


def build_assembly(k: int) -> str:
    words_per_row = (k % 4) + 1
    first_word_address = 16384 + 32 * k
    words_to_skip = 32 - words_per_row

    return f"""// Nand2Tetris capstone: keyboard-controlled black box
// Generated for K={k}
// Starts at screen row {k}; height=20 rows; width={words_per_row * 16} pixels.
// Press any key to draw the box; release the key to clear it.
// R13 = screen pointer, R14 = rows remaining, R15 = words remaining in row.

(LOOP)
@KBD
D=M
@DRAW
D;JNE
@CLEAR
0;JMP

(DRAW)
@{first_word_address}
D=A
@R13
M=D
@20
D=A
@R14
M=D

(DRAW_ROW)
@{words_per_row}
D=A
@R15
M=D

(DRAW_WORD)
@R13
A=M
M=-1
@R13
M=M+1
@R15
MD=M-1
@DRAW_WORD
D;JGT

@{words_to_skip}
D=A
@R13
M=D+M
@R14
MD=M-1
@DRAW_ROW
D;JGT
@LOOP
0;JMP

(CLEAR)
@{first_word_address}
D=A
@R13
M=D
@20
D=A
@R14
M=D

(CLEAR_ROW)
@{words_per_row}
D=A
@R15
M=D

(CLEAR_WORD)
@R13
A=M
M=0
@R13
M=M+1
@R15
MD=M-1
@CLEAR_WORD
D;JGT

@{words_to_skip}
D=A
@R13
M=D+M
@R14
MD=M-1
@CLEAR_ROW
D;JGT
@LOOP
0;JMP
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the capstone Box.asm and assemble it to Box.hack."
    )
    parser.add_argument("--k", type=int, help="last two digits of your roll number (0-99)")
    args = parser.parse_args()

    k = args.k if args.k is not None else load_config_k()
    if k is None:
        try:
            entered = input("Enter K (last two digits of your roll number, 00-99): ").strip()
            k = int(entered)
        except (ValueError, EOFError):
            print("Error: enter a whole number from 0 to 99, or set K in project_config.py.", file=sys.stderr)
            return 2

    if not 0 <= k <= 99:
        print("Error: K must be between 0 and 99.", file=sys.stderr)
        return 2
    if not ASSEMBLER.is_file():
        print(f"Error: assembler.py was not found at: {ASSEMBLER}", file=sys.stderr)
        return 2

    output_dir = Path(__file__).resolve().parent
    asm_path = output_dir / "Box.asm"
    hack_path = output_dir / "Box.hack"
    asm_path.write_text(build_assembly(k), encoding="utf-8")

    print(f"Created {asm_path}")
    print(f"K={k}; start row={k}; height=20; width={(k % 4 + 1) * 16} pixels")
    command = [sys.executable, str(ASSEMBLER), str(asm_path), str(hack_path), "--k", str(k)]
    result = subprocess.run(command, cwd=PROJECT_FILES, check=False)
    if result.returncode != 0:
        print("Assembler failed; check the error above.", file=sys.stderr)
        return result.returncode

    print(f"Created {hack_path}")
    print("Next: open Box.hack in the official Nand2Tetris CPU Emulator and test key press/release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
