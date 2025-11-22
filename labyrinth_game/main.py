#!/usr/bin/env python3

#Модуль main — точка входа в игру.
from .constants import COMMANDS
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def main():
    '''
    Основная функция запуска и управления игровым процессом.

    Инициализирует игру, выводит приветственное сообщение, отображает описание 
    начальной комнаты и запускает основной игровой цикл. Цикл продолжается до тех 
    пор, пока флаг game_over не будет установлен в True.

    Args:
        None: функция не принимает аргументов. Использует глобальное состояние 
        game_state.

    Returns:
        None: функция выполняет игровой цикл и не возвращает значения.
    '''
    print('\n' + '-' * 50)
    print('     ДОБРО ПОЖАЛОВАТЬ В ЛАБИРИНТ СОКРОВИЩ!')
    print('-' * 50)
    print('• Введи help, чтобы увидеть список команд.')
    print('• Введи exit/quit, если станет страшно и захочешь покинуть игру.')
 
    describe_current_room(game_state)

    while not game_state['game_over']:       
        process_command(game_state, command = get_input())

def process_command(game_state, command):
    '''
    Обрабатывает введённую игроком команду и выполняет соответствующее действие.

    Функция разбивает входную строку на команду и аргумент, затем сопоставляет команду
    с доступным действием (перемещение, использование предмета, просмотр комнаты и т.д.)
    и вызывает соответствующую функцию.

    Args:
        game_state (dict): Словарь с состоянием игры.
        command (str): Введённая игроком команда.

    Returns:
        None: функция не возвращает значение, только выполняет действия.
    '''
    # Разделение команды на части (разделитель - пробел)
    parts = command.strip().lower().split() 

    if not parts:
        print('Не время для шалостей — лабиринт ждёт слова.' 
              ' Введи команду. Для подсказки — help.')
        return
    
    action = parts[0] #команда
    arg = parts[1] if len(parts) > 1 else None #аргумент (с проверкой на существование)

    directions = {'north', 'south', 'east', 'west'}
    is_directions = action in directions

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

        case cmd if is_directions:
                move_player(game_state, direction=cmd)

        case 'take':
            if arg:
                take_item(game_state, item_name=arg)
            else:
                print('Соберись! Укажи конкретно, что ты хочешь взять!')

        case 'solve':
            if game_state['current_room'] != 'treasure_room':
                solve_puzzle(game_state)
            else:
                attempt_open_treasure(game_state)

        case 'inventory':
            show_inventory(game_state)

        case 'help':
            show_help(COMMANDS)

        case 'quit' | 'exit':
            game_state['game_over'] = True
            print('Уже уходишь? В следующий раз выпей элексир смелости, ' 
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
