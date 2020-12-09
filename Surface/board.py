class Sector:
    def __init__(self) -> None:
        self.width, self.height = 0, 0  # Длина и высота секрора
        self.board = None

    def gen_board(self) -> None:
        """
        Генерация поля (карты) в секторе.

        :return:
        """
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
