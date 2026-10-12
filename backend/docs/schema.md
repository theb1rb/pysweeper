# Database Columns
GameBoard:
- name: string
- difficulty: int
- game_status: bool
- start_date: string
- end_date: string

Square:
- name: string
- pos_x: int 
- pos_y: int 
- number: int
- bomb: bool
- flag: bool
- clickable: bool

# Object Constructor args
GameBoard:
- name: string
- difficulty: string

Square:
- pos_x: int
- pos_y: int
- number: int
- bomb: bool
- flag: bool
- clickable: bool

# Object attrs
GameBoard:
- name
- difficulty
- base
- grid_x
- grid_y
- total_squares
- total_bombs
- bomb_locations
- revealed_squares
- revealable_squares
- rows
- game_over