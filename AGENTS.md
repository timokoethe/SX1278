# AGENTS.md

This repository contains a lightweight MicroPython SX1278 LoRa driver for Raspberry Pi Pico and Pico 2.

- Keep changes small and compatible with MicroPython; do not introduce CPython-only APIs or external dependencies.
- The driver lives in `sx1278.py`. The public API reference lives in `docs/api.md`; keep it, `README.md`, and `example/` consistent with public API and behavior changes.
- Keep `README.md` focused on installation and quick-start usage. Put detailed method signatures, defaults, value ranges, limitations, and radio-mode requirements in `docs/api.md`.
- Preserve hardware-safe defaults, especially frequency and transmit-power limits.
- There is no automated test suite. Check Python syntax and, for hardware behavior, test on a Pico with an SX1278/Ra-01 module.
