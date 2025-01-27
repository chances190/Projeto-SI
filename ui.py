# ui.py
import pygame
from config import (
    UI_FONT_SIZE,
    BUTTON_SIZE,
    BUTTON_SPACING,
    UI_BG_COLOR,
    UI_TEXT_COLOR,
    ALGORITHMS,
    WINDOW_WIDTH,
)


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.button_base_y = 10

    def draw_ui_elements(self, surface, debug_mode, selected_algorithm):
        debug_rect = self.draw_button(
            surface, f"Debug: {'ON' if debug_mode else 'OFF'}", (10, self.button_base_y)
        )

        algo_rect = self.draw_button(
            surface,
            f"Algorithm: {selected_algorithm}",
            (10, self.button_base_y + BUTTON_SIZE[1] + BUTTON_SPACING),
        )

        reset_rect = self.draw_button(
            surface, "Reset", (WINDOW_WIDTH - (BUTTON_SIZE[0] + 10), self.button_base_y)
        )

        return debug_rect, algo_rect, reset_rect

    def draw_button(self, surface, text, position):
        rect = pygame.Rect(position, BUTTON_SIZE)
        bg = pygame.Surface(BUTTON_SIZE, pygame.SRCALPHA)
        bg.fill(UI_BG_COLOR)
        surface.blit(bg, rect.topleft)

        text_surf = self.font.render(text, True, UI_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        return rect

    def draw_algorithm_options(self, surface):
        option_rects = []
        base_y = self.button_base_y + (BUTTON_SIZE[1] + BUTTON_SPACING) * 2
        for i, algorithm in enumerate(ALGORITHMS):
            pos = (10, base_y + i * (BUTTON_SIZE[1] + BUTTON_SPACING))
            rect = self.draw_button(surface, algorithm, pos)
            option_rects.append(rect)
        return option_rects
