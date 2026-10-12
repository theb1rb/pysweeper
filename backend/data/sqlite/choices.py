from backend.choices import PysweeperItemTypes

PYSWEEPER_TABLE_COLUMN_CHOICES = {
    PysweeperItemTypes.GAME: [
        "name",
        "difficulty",
        "game_over",
        "start_date",
        "end_date",
    ],
    PysweeperItemTypes.SQUARE: [
        "name",
        "pos_x",
        "pos_y",
        "number",
        "bomb",
        "flag",
        "revealed",
        "id",
    ],
}
