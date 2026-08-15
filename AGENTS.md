# AGENTS.md

This repository contains a lightweight MicroPython SX1278 LoRa driver for Raspberry Pi Pico and Pico 2.

- Keep changes small and compatible with MicroPython; do not introduce CPython-only APIs or external dependencies.
- The driver lives in `sx1278.py`; keep `example/` and `README.md` consistent with public API changes.
- Preserve hardware-safe defaults, especially frequency and transmit-power limits.
- There is no automated test suite. Check Python syntax and, for hardware behavior, test on a Pico with an SX1278/Ra-01 module.
