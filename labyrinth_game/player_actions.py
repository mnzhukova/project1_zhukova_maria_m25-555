# Модуль player_actions - функции, связанные с действиями игрока
from .constants import ROOMS
from .utils import describe_current_room


def show_inventory(game_state):
    '''
    Отображает содержимое инвентаря игрока.

    Args:
        game_state(dict): Словарь с состоянием игры.

    Returns:
        None: Выводит информацию в консоль, не возвращая значения.
    '''
    if game_state.get('player_inventory'):
        player_inventory_str = ' ,'.join(game_state['player_inventory'])
        print(f'Инвентарь: {player_inventory_str}')
    else:
        print('Инвентарь пуст')

def get_input(prompt='> '):
    '''
    Запрашивает ввод у пользователя с заданным приглашением (prompt).
    
    Args:
        prompt (str): Текст-приглашение для ввода (по умолчанию: '> ').
    
    Returns:
        str: Введённая пользователем строка (в нижнем регистре), либо 'quit' 
               при прерывании (Ctrl+C) или EOF.
    '''
    try:
        user_input = input(prompt).lower()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры.')
        return 'quit' 
    
def move_player(game_state, direction):
    '''
    Перемещает игрока в указанном направлении, если выход существует.

    Функция проверяет наличие допустимого выхода из текущей комнаты 
    в заданном направлении.

    При успешном перемещении:
    - обновляет текущую комнату в состоянии игры;
    - увеличивает счётчик пройденных шагов;
    - выводит описание новой комнаты.
    При отсутствии выхода выводит сообщение об ошибке.

    Args:
        game_state(dict): Словарь с состоянием игры.

    Returns:
        None: Функция не возвращает значение. Изменяет game_state и производит
            вывод в консоль.
    '''
    current_room = game_state['current_room']
    current_exits = ROOMS[current_room].get('exits')

    if direction in current_exits:
        game_state['current_room'] = current_exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print('Нельзя пойти в этом направлении.')

def take_item(game_state, item_name):
    current_room = game_state['current_room']

    if item_name in ROOMS[current_room]['items']:
       game_state['player_inventory'].append(item_name)
       ROOMS[current_room]['items'].remove(item_name)
       print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет.')
