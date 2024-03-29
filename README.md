# Error and another error =/
---
Игра запускается из файла main.py  
Идея: Создать игру, в которой нужно будет применять знания python и писать свою логику поведения объектов.
---
![alt text](https://github.com/MR-Geri/projectPygame/blob/master/idea/menu.png)

1. Возможности:
    - TextInput поддерживает:
        - Полное очищение (Shift + del | Shift + Backspace)
        - Перемещение курсора
        - Вставку (Ctrl + V)
    - Меню прокрутки поддерживает:
        - Прокрутку с помощью ползунка
        - Прокрутку с помощью колеса мыши
    - Игра поддерживает PLAY|PAUSE (Press Space)
    - Игра поддерживает несколько скоростей (Press <) | (Press >)
    - Игра поддерживает Zoom (CTRL + mouse_SCROLL)
    - Игра поддерживает воспроизведение ваших треков:
        - В папку ../Data/Sounds/background_music/ поместите ваши треки и они отобразятся в плеере игры
    - Вызов меню для использования разового кода происходит по нажатию на клавишу (~)
    - Игроку доступны константы, которые он может импортировать из файла const
        ```
        ORES = ['IronOre', 'GoldOre', 'CooperOre', 'TinOre', 'SiliconOre', 'PlatinumOre']
        BIOMES = ['Plain', 'Swamp', 'Mountain', 'Desert']
        ROBOTS = ['MK0', 'MK1', 'MK2', 'MK3']
        RESOURCES = ['Железо', 'Алюминий', 'Золото', 'Медь', 'Олово', 'Кремний', 'Платина']
        ```
2. Логика мира:
    - Сектор выглядит так:  
      ![alt text](https://github.com/MR-Geri/projectPygame/blob/master/idea/sector.png)
    - В функции, которые пишет игрок, передаётся:
        1. Статистика объекта, для которого пишется код
        2. Список списков с [`название биома ячейки`, `стоимость перемещения в эту ячейку`]
        3. Список списков со `статистикой всех объектов в секторе`
3. Логика роботов:
    - Если робот (А) _наступает на ячейку_, где находится робот (В), то робот (В) **уничтожается**.
    - Если робот (А) _наступает на ячейку_, где находится строение, то робот (А) **уничтожается**.
    - Роботы не могут перемещаться по горам.
    - Робот передаёт предметы в неограниченном количестве
        1. Если у объекта, которому передаётся предмет, заполнено хранилище, то ресурс теряется.
    - У робота есть permissions в котором указано может ли робот сейчас выполнять то или иное действие.
     ```
    class PermissionsRobot:
        def __init__(self, states: dict = None) -> None:
            if states is None:
                states = {'can_move': True, 'can_charging': True, 'can_mine': True, 'can_item_transfer': True}
            self.can_move = states['can_move']
            self.can_charging = states['can_charging']
            self.can_mine = states['can_mine']
            self.can_item_transfer = states['can_item_transfer']
    
        def set_move(self, flag: bool) -> None:
            self.can_move = flag
    
        def set_charging(self, flag: bool) -> None:
            self.can_charging = flag
    
        def set_mine(self, flag: bool) -> None:
            self.can_mine = flag
    
        def set_item_transfer(self, flag: bool) -> None:
            self.can_item_transfer = flag
    
        def get_state(self) -> dict:
            return {'can_move': self.can_move, 'can_charging': self.can_charging, 'can_mine': self.can_mine,
                    'can_item_transfer': self.can_item_transfer}
   ```
    - На permissions могут влиять другие объекты. Например **База** блокирует перемещение для **Робота**:
    ```
    # Логика базы для зарядки робота
    def energy_transfer(state, board, entities) -> Union[Tuple[int, Tuple[int, int]], None]:
        robot = entities[28][0]
        if robot:
            if robot['energy'] < robot['energy_max']:
                robot['permissions'].set_move(False)
                return (5, (0, 28)), (5, (0, 29))
            else:
                robot['permissions'].set_move(True)
        return None
    ```
    - Функции
        - Перемещение:
            1. Должна называться **move**
            2. Должна вернуть позицию **(x, y)** -> **Tuple[int, int]** или ***None***
        - Добыча ресурсов:
            1. Должна называться **mine**
            2. Должна вернуть позицию **(x, y)** -> **Tuple[int, int]** или ***None***
        - Передача ресурсов:
            1. Должна называться **item_transfer**
            2. Должна вернуть **tuple(pos, resource, condition, quantity)** или ***None***:
                - pos => позиция **(x, y)** -> **Tuple[int, int]**
                - resource => название ресурса [*RESOURCES*]
                - condition => состояние ресурса ['сырьё' or 'продукт'] -> **str**
                - quantity => количество -> **int**
4. Логика баз:
    - База получает урон только от противников.
    - База создаёт роботов вокруг себя по кругу, если есть свободное место, иначе не создаёт.
    - База передаёт энергию лучом
        1. Если на ячейке, куда она передаёт энергию ничего нет, то энергия теряется.
        2. Если энергии у объекта, которому передаётся энергия, заполнено хранилище, то энергия теряется.
    - База передаёт предметы в неограниченном количестве
        1. Если у объекта, которому передаётся предмет, заполнено хранилище, то ресурс теряется.
    - У базы есть permissions в котором указано может ли база сейчас выполнять то или иное действие.
     ```
   class PermissionsBase:
        def __init__(self, states: dict = None) -> None:
            if states is None:
                states = {'can_charging': True, 'can_generate': True, 'can_item_transfer': True}
            self.can_charging = states['can_charging']
            self.can_generate = states['can_generate']
            self.can_item_transfer = states['can_item_transfer']
    
        def set_charging(self, flag: bool) -> None:
            self.can_charging = flag
    
        def set_generate(self, flag: bool) -> None:
            self.can_generate = flag
    
        def set_item_transfer(self, flag: bool) -> None:
            self.can_item_transfer = flag
    
        def get_state(self) -> dict:
            return {'can_charging': self.can_charging, 'can_generate': self.can_generate,
                    'can_item_transfer': self.can_item_transfer}
   ```
    - На permissions могут влиять другие объекты.
    - Функции
        - Передача энергии:
            1. Должна называться **energy_transfer**
            2. Должна вернуть количество энергии которое нужно передать, позицию куда нужно передать **(energy, (x,
               y))** -> **Tuple[int, Tuple[int, int]]** или ***None***
        - Передача ресурсов:
            1. Должна называться **item_transfer**
            2. Должна вернуть **tuple(pos, resource, condition, quantity)** или ***None***:
                - pos => позиция **(x, y)** -> **Tuple[int, int]**
                - resource => название ресурса [*RESOURCES*]
                - condition => состояние ресурса ['сырьё' or 'продукт'] -> **str**
                - quantity => количество -> **int**
5. Логика плавилен:
    - Плавильня получает урон только от противников.
    - Плавильня передаёт предметы в неограниченном количестве
        1. Если у объекта, которому передаётся предмет, заполнено хранилище, то ресурс теряется.
    - У плавильни есть permissions в котором указано может ли плавильня сейчас выполнять то или иное действие.
     ```
   class PermissionsFoundry:
        def __init__(self, states: dict = None) -> None:
            if states is None:
                states = {'can_melt': True, 'can_item_transfer': True, 'can_charging': True}
            self.can_melt = states['can_melt']
            self.can_item_transfer = states['can_item_transfer']
            self.can_charging = states['can_charging']
    
        def set_melt(self, flag: bool) -> None:
            self.can_melt = flag
    
        def set_item_transfer(self, flag: bool) -> None:
            self.can_item_transfer = flag
    
        def set_charging(self, flag: bool) -> None:
            self.can_charging = flag
    
        def get_state(self) -> dict:
            return {'can_melt': self.can_melt, 'can_item_transfer': self.can_item_transfer,
                    'can_charging': self.can_charging}
   ```
    - На permissions могут влиять другие объекты.
    - Функции
        - Передача ресурсов:
            1. Должна называться **item_transfer**
            2. Должна вернуть **tuple(pos, resource, condition, quantity)** или ***None***:
                - pos => позиция **(x, y)** -> **Tuple[int, int]**
                - resource => название ресурса [*RESOURCES*]
                - condition => состояние ресурса ['сырьё' or 'продукт'] -> **str**
                - quantity => количество -> **int**
6. Функции разового кода:
    - place_base(x: int, y: int) -> Размещение базы на поле
    - place_foundry(x: int, y: int) -> Размещение плавильни на поле
    - create_robot(robot: ROBOTS) -> Создание робота
7. Виды роботов:
    - Разнорабочие:
        - MK0
            - Цена создания:
                - 100 энергии
            - Не может передвигаться по:
                - Горы
                - Все виды руд
            - Характеристика:
                - Урон > 0
                - Прочность > 100
                - Дальность перемещения > 1
                - Размер инвентаря > 50
                - Дальность передачи ресурсов > 1
        - MK1
            - Цена создания:
                - 150 энергии
            - Не может передвигаться по:
                - Горы
                - Все виды руд
            - Характеристика:
                - Урон > 0
                - Прочность > 130
                - Дальность перемещения > 1
                - Размер инвентаря > 150
                - Дальность передачи ресурсов > 1
        - MK2
            - Цена создания:
                - 200 энергии
                - 150 обработанной меди
                - 50 обработанного олова
                - 80 обработанного железа
            - Не может передвигаться по:
                - Горы
                - Все виды руд
            - Характеристика:
                - Урон > 0
                - Прочность > 100
                - Дальность перемещения > 2
                - Размер инвентаря > 300
                - Дальность передачи ресурсов > 1
        - MK3
            - Цена создания:
                - 200 энергии
                - 100 обработанной меди
                - 50 обработанного олова
                - 80 обработанного железа
                - 15 обработанной платины
            - Не может передвигаться по:
                - Горы
                - Все виды руд
            - Характеристика:
                - Урон > 0
                - Прочность > 200
                - Дальность перемещения > 3
                - Размер инвентаря > 400
                - Дальность передачи ресурсов > 2
8. Виды баз:
    - Стартовая:
        - MK0
9. Виды строений:
    - Плавильня
        - Foundry

---
