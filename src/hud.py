import pygame as pg

from asset_manager import AssetManager


a = AssetManager()

def blit_handle_text(screen: pg.Surface, text: str):
    font = pg.font.Font(a.get_file_path("HUD/Font/Font.ttf"), 20)
    surface = font.render(text, 0, [255, 255, 255])
    screen.blit(surface, (screen.get_width() / 2 - surface.get_width() / 2, screen.get_height() - round(surface.get_height() * 1.5)))
