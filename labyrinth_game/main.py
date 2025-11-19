#!/usr/bin/env python3
"""
Модуль main — точка входа в игру.
"""
from .player_actions import show_inventory


def main():
    """Основная функция игры."""
    print("Первая попытка запустить проект!")

game_state = {
        'player_inventory': ['knife'], # Инвентарь игрока
        'current_room': 'hall', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}

if __name__ == "__main__":
    main()

show_inventory(game_state)
