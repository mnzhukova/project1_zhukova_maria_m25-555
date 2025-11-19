#!/usr/bin/env python3

#Модуль main — точка входа в игру.

from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import describe_current_room


def main():
    '''Основная функция игры.'''
    print(40*'-', '  \nДобро пожаловать в Лабиринт сокровищ!\n',39*'-')
    print('Введи exit/quit, если станет страшно и захочешь покинуть игру\n')
    describe_current_room(game_state)

    while not game_state['game_over']:       
        process_command(game_state, command = get_input())

def process_command(game_state, command):
    # Разделение команды на части (разделитель - пробел)
    parts = command.strip().lower().split() 

    if not parts:
        print('Не время для шалостей — лабиринт ждёт слова.' 
              ' Введи команду. Для подсказки — help.')
        return
    
    action = parts[0] #команда
    arg = parts[1] if len(parts) > 1 else None #аргумент (с проверкой на существование)

    match action:
        case 'look':
            describe_current_room(game_state)
        case 'use':
            if arg:
                use_item(game_state, item_name=arg)
            else:
                print('Я что экстрасенс? Напиши, что именно ты хочешь использовать')
        case 'go':
            if arg:
                move_player(game_state, direction=arg)
            else:
                print('Если хочешь идти - иди! ' 
                      'Но ты останешься на месте, если не задать одно из направлений:' 
                      ' north, south, west, east')
        case 'take':
            if arg:
                take_item(game_state, item_name=arg)
            else:
                print('Соберись! Укажи конкретно, что ты хочешь взять!')
        case 'inventory':
            show_inventory(game_state)
        case 'help':
            print('Список существующих команд:\n'
                    'look — осмотреть комнату\n'
                    'inventory — показать инвентарь\n'
                    'go <направление> — пойти в указанном направлении\n'
                    'solve — решить загадку\n'
                    'quit/exit — выйти из игры'
            )
        case 'quit' | 'exit':
            game_state['game_over'] = True
            print('Уже уходишь? В следующий раз выпей элексир смелости,' 
                  'прежде чем начать игру!')
        case _:
            print('Эхо лабиринта не узнаёт этого слова. Попроси помощи '
                  '— введи help.')

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}

if __name__ == '__main__':
    main()
