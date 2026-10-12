#!/bin/bash

# Test game create
echo "Creating 'gabe' game"
curl -ki -X POST --json '{"name": "gabe", "difficulty": 1}' http://127.0.0.1:8000/game/new
echo "Creating 'connor' game"
curl -ki -X POST --json '{"name": "connor", "difficulty": 1}' http://127.0.0.1:8000/game/new

# Test game delete
echo "Deleting connor"
curl -ki -X POST --json '{"name": "connor"}' http://127.0.0.1:8000/game/delete

# Test click square
echo "Clicking a square"
curl -ki -X POST --json '{"x": 5, "y": 5}' http://127.0.0.1:8000/game/square/gabe

# Test set flag
echo "Placing a flag"
curl -ki -X POST --json '{"x": 5, "y": 6, "flag": true}' http://127.0.0.1:8000/game/square/gabe

# Test get game state
echo "Getting a game"
curl -ki -X GET http://127.0.0.1:8000/game/play/gabe