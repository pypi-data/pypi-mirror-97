# 绘制棋盘
def draw_chess_board(position: tuple = (-200, 200), width: int = 400, height: int = 400, row: int = 5,
                     col: int = 5) -> None:
    """
    绘制棋盘

    Args:
        position: 棋盘左上角位置
        width: 棋盘宽度
        height: 棋盘高度
        row: 棋盘行数
        col: 棋盘列数

    Returns:
        None: 绘制棋盘，没有返回值
    """
    import turtle as t
    t.speed(0)
    x, y = position
    for i in range(row + 1):
        t.penup()
        t.goto(x, y - i * height / row)
        t.pendown()
        t.goto(x + width, y - i * height / row)
    for i in range(col + 1):
        t.penup()
        t.goto(x + i * width / col, y)
        t.pendown()
        t.goto(x + i * width / col, y - height)
    t.done()


if __name__ == '__main__':
    draw_chess_board()
