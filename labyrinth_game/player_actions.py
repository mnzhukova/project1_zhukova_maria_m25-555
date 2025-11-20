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
        prompt(str): Текст-приглашение для ввода (по умолчанию: '> ').
    
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
        game_state(dict): Словарь с состоянием игры
        direction(str): Направление движения (например, 'north', 'south').
            Должно соответствовать ключу в словаре 'exits' текущей комнаты.

    Returns:
        None: Функция не возвращает значение. Изменяет game_state и производит
            вывод в консоль.
    '''
    current_room = game_state['current_room']
    room_exits = ROOMS[current_room].get('exits')

    if direction in room_exits:
        game_state['current_room'] = room_exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print('Нельзя пойти в этом направлении.')

def take_item(game_state, item_name):
    '''
    Позволяет игроку взять предмет из текущей комнаты и добавить его в инвентарь.

    Функция проверяет наличие указанного предмета в текущей комнате. Если предмет 
    найден:
    - добавляет его в инвентарь игрока (game_state['player_inventory']);
    - удаляет его из списка предметов комнаты (ROOMS[current_room]['items']);
    - выводит сообщение об успешном взятии.
    Если предмет не найден — выводит сообщение об отсутствии предмета.

    Args:
        game_state(dict): Словарь с состоянием игры.
        item_name (str): Название предмета, который игрок пытается взять.

    Returns:
        bool: True — если предмет успешно взят;
               False — если предмета в комнате нет.
    '''
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    # Проверяем наличие предмета в комнате
    if item_name in room_items:
        # Добавляем в инвентарь
       game_state['player_inventory'].append(item_name)
       # Удаляем из комнаты
       room_items.remove(item_name)
       print(f'Вы подняли: {item_name}')
       return True
    else:
        print('Такого предмета здесь нет.')
        return False

def use_item(game_state, item_name):

    # Проверяем, есть ли предмет в инвентаре
    if item_name not in game_state['player_inventory']:
        print('У вас нет такого предмета.')
        return False
    
    # Обрабатываем использование конкретных предметов
    match item_name:
        case 'torch':
            print('Стало светлее. Не знаю даже, поможет ли тебе это.')

        case 'sword':
            print(
                'Ух! У тебя прибавилось уверенности. '
                'Можешь позвонить начальнику и запросить зп повыше'
            )

        case 'bronze_box':
            print('Шалость удалась! Ты открыл шкатулку')
            if 'rusty_key' in game_state['player_inventory']:
                print('Ха-ха-ха! А в шкатулке только мой смех и презрение!')
            else: 
                game_state['player_inventory'].append('rusty_key')
                print('Проверь инвентарь! Дарю сейчас, но это тебе на Новый год!')
        
        case _:
            print(
                'Ты не знаешь, как использовать этот предмет. '
                'Вырастешь - поймешь!'
            )
            
    return True