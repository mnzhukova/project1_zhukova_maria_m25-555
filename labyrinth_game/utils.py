# Модуль utils - вспомогательные функции
from .constants import ROOMS


def describe_current_room(game_state):
    '''
    Описывает текущую комнату: выводит название, описание, список видимых предметов,
    доступные выходы и уведомление о наличии загадки.

    Args:
        game_state(dict): Словарь с состоянием игры.

    Returns:
        None: Выводит информацию в консоль, не возвращая значения.

    ROOMS = { 
   'название комнаты': { 
        'description': 'Описание комнаты',  
        'exists': {'направление': 'название комнаты, куда ведет выход'},
        'items': ['Список предметов, которые находятся в комнате'],
        'puzzle': Кортеж из двух элементов (вопрос, ответ) или None, если загадки нет
 }
    '''
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    #Название текущей комнаты 
    print(f'=={current_room.upper()}==')
    
    #Описание комнаты
    print(f'{room_data['description']}\n')

    #Видимые предметы (если есть)
    if room_data.get('items'):
        items_str = ', '.join(room_data['items'])
        print(f'Заметные предметы: {items_str}\n')

    #Доступные выходы (если есть)
    if room_data.get('exits'):
        exits_str = ', '.join(room_data['exits'].keys())
        print(f'Выходы: {exits_str}\n')

    #Уведомление о наличии загадки (если есть)
    if room_data.get('puzzle'):
        print('Кажется, здесь есть загадка (используйте команду solve).\n')
    
def solve_puzzle(game_state):
    '''
    Позволяет игроку решить загадку в текущей комнате.

    Args:
        game_state (dict): Словарь с состоянием игры.

    Returns:
        bool:
            - True: если загадка решена или её не было в комнате.
            - False: если ответ неверный.
    '''
    current_room = game_state['current_room']
    room_puzzle = ROOMS[current_room].get('puzzle') 

    # Проверяем наличие загадки в комнате
    if not room_puzzle:
        print('Загадок здесь нет.')
        return True
        
    # Вывод загадки
    print(room_puzzle[0])

    # Запрос ответа от пользователя
    print(f'Ваш ответ: ')
    user_answer = input().strip().lower()

    # Проверяем правильность ответа
    if user_answer == room_puzzle[1]:
        print('Успех! Получай медальку')
        # добавляем награду в инвентарь
        game_state['player_inventory'].append('medal')

        # Убираем загадку из комнаты
        del ROOMS[current_room]['puzzle']
        
        return True
    else:
        print('Неверно. Попробуйте снова.')
        return False



