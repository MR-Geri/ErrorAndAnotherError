# Крутое название
---
D:\PycharmProjects\projectPygame\Game_code  
![alt text](https://github.com/MR-Geri/projectPygame/blob/master/idea/menu.png)  
0. Возможности:
    - TextInput поддерживает:
        - Полное очищение (Shift + del | Shift + Backspace)
        - Перемещение курсора
        - Вставку (Ctrl + V)
    - Меню прокрутки поддерживает:
        - Прокрутку с помощью ползунка
        - Прокрутку с помощью колеса мыши
    - Игра поддерживает PLAY|PAUSE (Press Space)
    - Игра поддерживает воспроизведение ваших треков:
        - В папку ../Data/Sounds/background_music/ поместите ваши треки и они отобразятся в игре
1. Логика мира:
    - Сектор выглядит так:  
        ![alt text](https://github.com/MR-Geri/projectPygame/blob/master/idea/sector.png)
    -  В функции, которые пишет игрок передаётся:
        1. Статистика объекта, для которого пишется код
        2. Список списков с `название биома ячейки`, `стоимость перемещения в эту ячейку`
        3. Список списков с `статистикой всех объектов в секторе`
2. Логика роботов: 
    - Если робот (А) _наступает на ячейку_, где находится робот (В), то робот (В) **уничтожается**.
    - Если робот (А) _наступает на ячейку_, где находится база, то робот (А) **уничтожается**.
    - У робота есть permissions
     в котором указано может ли робот сейчас выполнять то или иное действие.
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
    - На permissions могут влиять другие объекты. 
     например **База** блокирует перемещение для **Робота**:
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
    - Функиции 
        - Перемещение:
            1. Называется **move**
            2. Должна вернуть позицию **(x, y)** -> **Tuple[int, int]** или ***None***
3. Логика баз:
    - База получает урон только от противников.
    - База создаёт роботов вокруг себя по кругу, если есть свободное место, инчае не создаёт.
    - База передаёт энергию лучом
        1. Если на ячейке, куда она передаёт энергию ничего нет, то энергия теряется.
        2. Если энергии у объекта, которому передаётся энергия, максимальное количество, то энергия теряется.
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
    - Функиции 
        - Передача энергии:
            1. Называется **energy_transfer**
            2. Должна вернуть количество энергии которое нужно передать, позицию куда нужно передать **(energy, (x, y))** -> **Tuple[int, Tuple[int, int]]** или ***None***
4. Разовые функции:
    - place_base(x: int, y: int) -> Размещение базы на поле
    - create_robot(robot: ALL_ROBOT) -> Создание робота
5. Виды роботов:
    - Разнорабочие:
        1. MK0
        2. MK1
6. 
---
