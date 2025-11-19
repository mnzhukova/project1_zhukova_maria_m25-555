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