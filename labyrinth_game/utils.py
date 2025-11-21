# Модуль utils - вспомогательные функции
import math

from .constants import ROOMS, VALID_ANSWERS


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

    # Название текущей комнаты 
    print(f'\n=={current_room.upper()}==')
    
    # Описание комнаты
    print(f'\n{room_data['description']}')

    # Видимые предметы (если есть)
    if room_data.get('items'):
        items_str = ', '.join(room_data['items'])
        print(f'\nЗаметные предметы: {items_str}')

    # Доступные выходы (если есть)
    if room_data.get('exits'):
        exits_str = ', '.join(room_data['exits'].keys())
        print(f'\nВыходы: {exits_str}\n')

    # Уведомление о наличии загадки (если есть)
    if room_data.get('puzzle'):
        print('\nКажется, здесь есть загадка (используйте команду solve).\n')

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

    # Проверяем наличие загадки в комнате
    if not ROOMS[current_room].get('puzzle') :
        print('Загадок здесь нет.')

    question, correct_answer = ROOMS[current_room]['puzzle']
    # Вывод загадки
    print(question)

    valid_set = VALID_ANSWERS.get(correct_answer, {correct_answer})

    # Запрос ответа от пользователя
    user_answer = input('Ваш ответ: >> ').strip().lower()

    # Если ответ неверный, даем пользователю вводить ответы
    while user_answer not in valid_set:
        if user_answer == 'exit':
            print('Возможно, получится в следующий раз')
            break
        # Если игрок ответил неверно, находясь в trap_room
        if current_room == 'trap_room':
            trigger_trap(game_state)
        print('Неверно. Попробуйте снова.\n' 
              'Введи exit для выхода из режима решения загадки'
        )
        user_answer = input('Ваш ответ: >> ').strip().lower()
        
    # Если ответ верный
    if user_answer in valid_set:
        # В зависимости от комнаты выдаем награду
        match current_room:
            case 'hall':
                print('10 очков Гриффиндору! А тебе похвала и слава!')

            case 'trap_room':
                print('Молодец! Возьми с полки пирожок.\n\n'
                      'В твой инвентарь добавлен cherry_pie'
                )
                # добавляем награду в инвентарь
                game_state['player_inventory'].append('cherry_pie')

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
        user_answer = input('Ваш ответ: >> ').lower()

        # если пользователь ввел что-то иное от да/нет.
        while user_answer not in ('да', 'нет', 'exit'):
            print('Просто да или нет! Это не сложно!')
            user_answer = input('Ваш ответ: >> ').lower()

        # Обработка ответов да/нет
        if user_answer == 'да':
            solve_puzzle(game_state)
        else:
            print('Вы отступаете от сундука.')

    return True

def show_help(COMMANDS):
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f'{command:<16}-{description}')

def pseudo_random(seed: int, modulo: int) -> int:
    '''
    Генерирует псевдослучайное целое число в диапазоне [0, modulo) 
    на основе математической формулы с использованием синуса.

    Args:
        seed (int): Начальное число (количество шагов).
        modulo (int): Граница диапазона.

    Returns:
        int: Целое число в диапазоне [0, modulo).
    '''
    sin_value = math.sin(seed * 12.9898)
    scaled = sin_value * 43758.5453
    fractional = scaled - math.floor(scaled)
    result = fractional * modulo

    return int(result)

def trigger_trap(game_state):
    print('Ловушка активирована! Пол стал дрожать...')
    
    if game_state.get('player_inventory'):
        # Если у игрока есть предметы в инвенторе
        seed = game_state['steps_taken']
        modulo = len(game_state['player_inventory'])
        # псевдорандомно удаляем один из предметов в инвенторе
        item_random_index = pseudo_random(seed, modulo)
        removed_item = game_state['player_inventory'].pop(item_random_index)
        print(f'Ты потерял {removed_item}')
    else:
        # Игрок получает урон
        print('Ты получаешь урон!')
        if pseudo_random(45, 9) < 3:
            print('Вы самое слабое звено, прощайте!')
            game_state['game_over'] = True
        else:
            print('Но тебе повезло, ты уцелел')

def random_event(game_state):
    current_room = game_state['current_room']

    # Определяем произойдет ли событие
    if pseudo_random(35, 10) == 0:
        # какое именно событие случится
        event_type = pseudo_random(15, 3)
        match event_type:
            # Сценарий 1 (Находка)
            case 0:
                print('Вот это удача! Ты нашел монетку! Если хочешь, то возьми её')
                ROOMS[current_room]['items'].append('coin')

            # Сценарий 2 (Испуг)
            case 1:
                print('Слышно шорох')
                if 'sword' in game_state['player_inventory']:
                    print(
                        'Хорошо, что у тебя есть меч.' 
                        'Тебе удалось напугать всех мышей в этой комнате'
                )
                else:
                    print('Жаль конечно, что у тебя нет меча')    

            # Сценарий 3 (Срабатывание ловушки)
            case 2:
                if (current_room == 'trap_room' and 
                        'torch' not in game_state['player_inventory']):
                    print('Пу-пу-пууу...Сработала ловушка')
                    trigger_trap(game_state)
            case _:
                print('Мимо пробежала мышь')
