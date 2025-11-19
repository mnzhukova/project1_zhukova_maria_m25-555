# Модуль player_actions - функции, связанные с действиями игрока

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