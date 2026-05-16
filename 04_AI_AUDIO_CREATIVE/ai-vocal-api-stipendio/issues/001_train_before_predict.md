# Issue 001 - Train before predict

## Goal

Keep model lifecycle explicit.

## Current implementation

The service refuses prediction if no trained model exists. The user must run training first or call the train endpoint.

## Acceptance criteria

Prediction without a model should produce a clear error.

README should explain the correct workflow.

CLI and API should both support training.
