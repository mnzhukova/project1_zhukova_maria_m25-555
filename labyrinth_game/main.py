#!/usr/bin/env python3
"""
Модуль main — точка входа в игру.
"""
from .constants import ROOMS
from .utils import describe_current_room
from .player_actions import show_inventory, get_input


def main():
    '''Основная функция игры.'''
    print('Добро пожаловать в Лабиринт сокровищ!')
    print('Введи quit, если захочешь выйти из игры')
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input('> ')

        if command == 'quit':
            game_state['game_over'] = True
            print('Выход из игры')

game_state = {
        'player_inventory': ['knife'], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}

if __name__ == "__main__":
    main()
