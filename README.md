# Pysweeper
The most sub-optimal over-engineered interpretation of Minesweeper you've ever seen... because learning is important!

## Test Configs
```json
{
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true,
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./backend/tests",
    ]}

```

## Debugging
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug PySweeper",
            "type": "debugpy",
            "request": "launch",
            "module": "backend.app",
            "python": "${workspaceFolder}/.venv/bin/python3",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```