#!/usr/bin/env python3
"""
Модуль main — точка входа в игру.
"""
from .constants import ROOMS

ROOMS

def main():
    """Основная функция игры."""
    print("Первая попытка запустить проект!")

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}

if __name__ == "__main__":
    main()
