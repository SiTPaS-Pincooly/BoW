import pygame


def print_text(screen, body, dest, color, size, font_):
    font = pygame.font.SysFont(font_, size)
    text_surface = font.render(body, True, color)
    screen.blit(text_surface, dest)


def text_frame(screen, dest, color, width, height):
    rect = pygame.rect.Rect(dest[0], dest[1], width, height)
    pygame.draw.rect(screen, color, rect)


log = []


def update_log(list_, text):
    if len(list_) >= 20:
        list_.pop(0)
    list_.append(text)


def warning(screen, body, monitor):
    center_x = monitor[0] // 2
    center_y = monitor[1] // 2

    font = pygame.font.SysFont("Arial", 60)
    text = font.render(body, True, "black")
    text_rect = text.get_rect()
    text_rect.center = (center_x, center_y)

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 10
    rect_x = center_x - rect_width // 2
    rect_y = center_y - rect_height // 2

    rect = pygame.Rect(rect_x, rect_y,
                       rect_width, rect_height)

    pygame.draw.rect(screen, "white", rect)
    screen.blit(text, text_rect)

    pygame.display.update()
    pygame.time.delay(750)
