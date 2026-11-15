#!/usr/bin/env python3
"""Two-pass assembler for the 16-bit Hack computer (Nand2Tetris)."""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from project_config import K as CONFIG_K
except ImportError:  # Also allow running this file from unusual launch contexts.
    CONFIG_K = None

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
PREDEFINED.update({f"R{i}": i for i in range(16)})

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010", "D-A": "0010011",
    "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000", "D|A": "0010101",
    "D|M": "1010101",
}


@dataclass(frozen=True)
class SourceLine:
    number: int
    text: str


class AssemblyError(Exception):
    """An assembly error tied to the original source line."""


def clean_source(path: Path) -> list[SourceLine]:
    lines: list[SourceLine] = []
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise AssemblyError(f"Cannot read input file '{path}': {exc}") from exc

    for line_no, raw in enumerate(raw_lines, start=1):
        # Remove // comments, then remove all whitespace within the instruction.
        code = raw.split("//", 1)[0]
        code = "".join(code.split())
        if code:
            lines.append(SourceLine(line_no, code))
    return lines


def is_valid_symbol(symbol: str) -> bool:
    if not symbol:
        return False
    if not (symbol[0].isalpha() or symbol[0] in "_.$:"):
        return False
    return all(ch.isalnum() or ch in "_.$:" for ch in symbol)


def line_error(line: SourceLine, message: str, k: int | None) -> AssemblyError:
    if k is not None and k % 3 == 1:
        return AssemblyError(f"Line {line.number}: {message}")
    return AssemblyError(f"Line {line.number}: {message}")


def first_pass(lines: Iterable[SourceLine], k: int | None) -> tuple[dict[str, int], list[SourceLine], list[str]]:
    symbols = dict(PREDEFINED)
    labels: dict[str, int] = {}
    instructions: list[SourceLine] = []
    warnings: list[str] = []
    rom_address = 0

    for line in lines:
        text = line.text
        if text.startswith("(") or text.endswith(")"):
            if not (text.startswith("(") and text.endswith(")") and text.count("(") == 1 and text.count(")") == 1):
                raise line_error(line, "malformed label declaration", k)
            label = text[1:-1]
            if not is_valid_symbol(label):
                raise line_error(line, f"invalid label name '{label}'", k)
            if label in symbols or label in labels:
                if k is not None and k % 3 == 2:
                    warnings.append(f"Warning: Line {line.number}: label '{label}' is defined more than once; keeping its first address.")
                    continue
                raise line_error(line, f"duplicate or reserved label '{label}'", k)
            labels[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1
            if rom_address > 32768:
                raise line_error(line, "program exceeds the 32K ROM address space", k)

    symbols.update(labels)
    return symbols, instructions, warnings


def encode_a_instruction(symbol_text: str, symbols: dict[str, int], next_variable: int,
                         line: SourceLine, k: int) -> tuple[str, int, tuple[str, int] | None]:
    if not symbol_text:
        raise line_error(line, "empty A-instruction", k)

    if symbol_text.isdecimal():
        value = int(symbol_text)
        if not 0 <= value <= 32767:
            raise line_error(line, f"A-instruction value {value} is outside 0..32767", k)
        return f"{value:016b}", next_variable, None

    if not is_valid_symbol(symbol_text):
        raise line_error(line, f"invalid symbol '{symbol_text}'", k)

    if symbol_text not in symbols:
        if next_variable > 32767:
            raise line_error(line, "no RAM addresses remain for new variables", k)
        symbols[symbol_text] = next_variable
        return f"{next_variable:016b}", next_variable + 1, (symbol_text, next_variable)

    value = symbols[symbol_text]
    if not 0 <= value <= 32767:
        raise line_error(line, f"symbol '{symbol_text}' has an invalid address", k)
    return f"{value:016b}", next_variable, None


def encode_c_instruction(text: str, line: SourceLine, k: int) -> str:
    if text.count("=") > 1 or text.count(";") > 1:
        raise line_error(line, f"invalid C-instruction '{text}'", k)

    if "=" in text:
        dest, remainder = text.split("=", 1)
    else:
        dest, remainder = "", text

    if ";" in remainder:
        comp, jump = remainder.split(";", 1)
    else:
        comp, jump = remainder, ""

    if dest not in DEST:
        raise line_error(line, f"invalid destination mnemonic '{dest}'", k)
    if comp not in COMP:
        raise line_error(line, f"invalid computation mnemonic '{comp}'", k)
    if jump not in JUMP:
        raise line_error(line, f"invalid jump mnemonic '{jump}'", k)

    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def assemble(input_path: Path, output_path: Path, k: int | None) -> None:
    source_lines = clean_source(input_path)
    symbols, instructions, warnings = first_pass(source_lines, k if k is not None else 0)
    for warning in warnings:
        print(warning, file=sys.stderr)

    # Track labels and variables separately for the symbols.txt extra feature.
    label_addresses = {name: address for name, address in symbols.items()
                       if name not in PREDEFINED and name not in {f"R{i}" for i in range(16)}}
    variable_addresses: dict[str, int] = {}
    machine_code: list[str] = []
    next_variable = 16

    for line in instructions:
        text = line.text
        if text.startswith("@"):
            binary, next_variable, new_variable = encode_a_instruction(text[1:], symbols,
                                                                          next_variable, line,
                                                                          k if k is not None else 0)
            machine_code.append(binary)
            if new_variable:
                variable_addresses[new_variable[0]] = new_variable[1]
        else:
            machine_code.append(encode_c_instruction(text, line, k if k is not None else 0))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text("\n".join(machine_code) + ("\n" if machine_code else ""), encoding="utf-8")
    except OSError as exc:
        raise AssemblyError(f"Cannot write output file '{output_path}': {exc}") from exc

    if k is not None and k % 3 == 0:
        symbols_path = output_path.parent / "symbols.txt"
        rows = ["# Labels and variables (predefined symbols omitted)"]
        rows.extend(f"{name} {address}" for name, address in sorted(label_addresses.items(), key=lambda item: (item[1], item[0])))
        rows.extend(f"{name} {address}" for name, address in sorted(variable_addresses.items(), key=lambda item: (item[1], item[0])))
        symbols_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        print(f"Wrote symbol table: {symbols_path}")

    print(f"Assembled {input_path} -> {output_path} ({len(machine_code)} instructions)")
    if k is None:
        print("Note: K is not set. The base assembler ran without the K-based extra feature.")
    else:
        print(f"K = {k}; K mod 3 = {k % 3}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble Hack .asm source into 16-bit .hack machine code.")
    parser.add_argument("input", type=Path, help="input .asm file")
    parser.add_argument("output", type=Path, nargs="?", help="output .hack file (default: input name with .hack)")
    parser.add_argument("--k", type=int, default=CONFIG_K, help="last two digits of your roll number (overrides project_config.py)")
    args = parser.parse_args()

    if args.k is not None and not 0 <= args.k <= 99:
        parser.error("K must be between 0 and 99 (the last two digits of your roll number).")

    output = args.output or args.input.with_suffix(".hack")
    try:
        assemble(args.input, output, args.k)
    except AssemblyError as exc:
        print(f"Assembly error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
