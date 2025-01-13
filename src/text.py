import pygame as pg


ANIM_INTERVAL = 15


class Text(pg.sprite.Sprite):
    def __init__(self, font: pg.font.Font, text: str, pos: tuple, color: pg.Color, animated=False):
        self.font = font
        self.text = text
        self.color = color
        self.animated = animated
        self.text_index = 0
        self.anim_interval = 0

        self.image = self.font.render(self.text, 0, self.color)
        self.rect = self.image.get_rect().move(pos)
        self.current_char = self.image

        self.char_width = self.image.get_width() / len(self.text)
        self.current_char_pos = [self.rect.x - self.char_width, self.rect.y]

    def set_animated(self):
        self.animated = not self.animated

    def load_current_char(self):
        self.current_char = self.font.render(self.text[self.text_index], 0, self.color)

    def update(self) -> None:
        if self.animated:
            self.anim_interval += 1

            if self.anim_interval >= ANIM_INTERVAL:
                self.load_current_char()
                self.current_char_pos[0] += self.char_width

                self.anim_interval = 0
                self.text_index += 1

                if self.text_index > len(self.text) - 1:
                    self.text_index = 0
                    self.current_char_pos[0] = self.rect.x
                    self.set_animated()

    def draw(self, screen: pg.Surface):
        if self.animated:
            screen.blit(self.current_char, (self.current_char_pos[0], self.current_char_pos[1]))
        else:
            screen.blit(self.image, self.rect)

