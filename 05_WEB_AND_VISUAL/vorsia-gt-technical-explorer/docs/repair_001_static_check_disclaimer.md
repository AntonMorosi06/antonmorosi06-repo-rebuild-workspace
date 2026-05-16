# Repair 001 - Static check disclaimer

## Problem

The first static check expected the exact phrase `not a real vehicle` inside README.md.

The repository already described Vorsia GT as a fictional concept and not a real product, but the wording was not identical to the assertion.

## Fix

The README now includes an explicit concept disclaimer.

The static check now verifies the concept across README, concept brief and known limitations instead of relying on one fragile exact phrase.

## Expected behavior

python3 tests/static_file_check.py should pass.

The project remains clearly framed as a fictional automotive concept and portfolio interface, not a real vehicle or manufacturer-affiliated product.
