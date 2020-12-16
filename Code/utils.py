import pygame as pg


def print_text(display, message, x, y, font_color=(255, 0, 0), font_size=20) -> None:
    font_type = pg.font.Font(None, font_size)
    text = font_type.render(message, True, font_color)
    text_rect = text.get_rect(center=(x, y))
    display.blit(text, text_rect)
