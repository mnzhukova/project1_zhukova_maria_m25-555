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

def happy_end(game_state):
    current_room = game_state['current_room']
    # Удаляем 'treasure_chest' из комнаты
    ROOMS[current_room]['items'].remove('treasure_chest')
    # Сообщение о победе
    print('В сундуке сокровище! Вы победили!')
    # Завершение игры
    game_state['game_over'] = True 


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
        
    # Вывод загадки
    print(room_puzzle[0])

    # Запрос ответа от пользователя
    print('Ваш ответ: ')
    user_answer = input('>').strip().lower()

    # Если ответ неверный, даем пользователю вводить ответы
    while user_answer != room_puzzle[1]:
        if user_answer == 'exit':
            print('Возможно, получится в следующий раз')
            break
        print('Неверно. Попробуйте снова.\n' 
              'Введи exit для выхода из режима решения загадки'
        )
        user_answer = input('>').strip().lower()
        
    # Если ответ верный
    if user_answer == room_puzzle[1]:
        # В зависимости от комнаты выдаем награду
        match current_room:
            case 'hall':
                print('10 очков Гриффиндору! А тебе похвала и слава!')

            case 'trap_room':
                print('Молодец! Возьми с полки пирожок.\n\n'
                      'В твой инвентарь добавлен cherry_pie'
                )
                # добавляем награду в инвентарь
                game_state['player_inventory'].append('cherry pie')

            case 'library':
                print('Вот это поворот! Верно! В этот раз тебе даю действительно '
                      'чего-то стоящую вещь в этой игре\n\n'
                      'В твой инвентарь добавлен treasure_key'
                )
                # добавляем награду в инвентарь
                game_state['player_inventory'].append('treasure_key')

            case 'treasure_room':
                happy_end(game_state)

            case 'lavatory':
                print('Повезло! Пользуйся - не благодари!'
                      'В твой инвентарь добавлена toilet_paper'
                )
                # добавляем награду в инвентарь
                game_state['player_inventory'].append('toilet_paper')

            case _:
                print('Решение верное! Забыл придумать для тебя награду')

        # Убираем загадку из комнаты
        del ROOMS[current_room]['puzzle']
        
        return True

def attempt_open_treasure(game_state):

    # Проверяем есть ли у игрока 'treasure_key'
    if 'treasure_key' in game_state['player_inventory']:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        happy_end(game_state)
    # Если 'treasure_key' нет, то сценарий с загадкой
    else:
        print("Сундук заперт. ... Ввести код? (да/нет)")
        user_answer = input('>').lower()

        # если пользователь ввел что-то иное от да/нет.
        while user_answer not in ('да', 'нет'):
            print('Просто да или нет! Это не сложно!')
            user_answer = input('>').lower()

        # Обработка ответов да/нет
        if user_answer == 'да':
            solve_puzzle(game_state)
        elif user_answer == 'нет':
            print('Вы отступаете от сундука.')

    return True

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")     
