import math


from Map import *
from Utilities import *
from Player import Player
from Stat import Stat

clock = pygame.time.Clock()

fullscreen = (0, 0)
pygame.init()
screen = pygame.display.set_mode(fullscreen, pygame.FULLSCREEN)
start_window = pygame.display.set_mode(fullscreen, pygame.FULLSCREEN)
log_in_window = pygame.display.set_mode(fullscreen, pygame.FULLSCREEN)
game_window = pygame.display.set_mode(fullscreen, pygame.FULLSCREEN)

casual_font = "arial"
board_font = None
casual_color = "black"

list_of_colors = ["blue", "red", "green", "purple"]


def update_start():
    start_window.fill("white")

    font = pygame.font.SysFont("times new roman", 36)
    text = font.render("Number of players (max 4): ", True, "black")
    text_rect = text.get_rect()
    text_rect.center = (monitor[0] // 2, monitor[1] // 2 - 20)
    start_window.blit(text, text_rect)

    input_rect = pygame.Rect(100, 100, 0, 0)
    pygame.draw.rect(start_window, "white", input_rect, 0)
    text_surface = font.render(input_text, True, "black")
    text_x = (monitor[0] - text_surface.get_width()) // 2
    text_y = (monitor[1] - text_surface.get_height()) // 2 + 20
    start_window.blit(text_surface, (text_x, text_y))


def update_player(number):
    log_in_window.fill("white")

    font = pygame.font.SysFont("times new roman", 36)
    text = font.render("Player's " + str(number + 1) + " name: ", True, "black")
    text_rect = text.get_rect()
    text_rect.center = (monitor[0] // 2, monitor[1] // 2 - 20)
    log_in_window.blit(text, text_rect)

    input_rect = pygame.Rect(100, 100, 0, 0)
    pygame.draw.rect(start_window, "white", input_rect, 0)
    text_surface = font.render(input_text, True, "black")
    text_x = (monitor[0] - text_surface.get_width()) // 2
    text_y = (monitor[1] - text_surface.get_height()) // 2 + 20
    log_in_window.blit(text_surface, (text_x, text_y))


monitor = pygame.display.get_window_size()
width_matrix = 10
height_matrix = 10
matrix = create_map(width_matrix, height_matrix)
width_sq = math.ceil(monitor[1] / height_matrix)
stat_width = math.ceil((monitor[0] - width_matrix * width_sq - 2) / 2)


def make_icon(image_):
    smth = pygame.image.load(image_)
    icon_ = pygame.transform.scale(smth, (width_sq, width_sq))
    return icon_


def draw_border(start_pos, end_pos, line_width):
    pygame.draw.line(game_window, "black", start_pos, end_pos, line_width)


def update_map():
    no = 0
    background = pygame.image.load("Icons\Background.jpg")
    game_window.blit(background, (0, 0))
    for q in range(height_matrix):
        ctrl = 0
        if q % 2 == 1:
            ctrl = width_matrix - 1
        for r in range(width_matrix):
            no += 1
            matrix[no - 1].append((abs(ctrl - r) * width_sq, q * width_sq))
            if matrix[no - 1][1].image is None:
                pass
            else:
                icon = make_icon(matrix[no - 1][1].image)
                game_window.blit(icon, (abs(ctrl - r) * width_sq, q * width_sq))
            Utilities.print_text(game_window, str(no), (abs(ctrl - r) * width_sq + 2, q * width_sq + 2),
                                 casual_color, 17, board_font)
            for s in range(width_matrix + 1):
                draw_border((s * width_sq, 0),
                            (s * width_sq, monitor[1]), 2)

            for t in range(height_matrix):
                draw_border((0, t * width_sq),
                            (width_matrix * width_sq, t * width_sq), 2)
            draw_border((0, monitor[0]),
                        (width_matrix * width_sq, monitor[0]), 2)


def update_player_position():
    used_colors = list_of_colors[:number_of_players]
    radius = 15
    for x in range(len(list_of_players)):
        position = list_of_players[x].position
        player_center = (matrix[position - 1][2][0] + width_sq // 4 * (2 * (x % 2) + 1),
                         matrix[position - 1][2][1] + width_sq // 4 + (width_sq // 2) * (x // 2))
        pygame.draw.circle(game_window, used_colors[x],
                           player_center, radius)


log_x = width_matrix * width_sq + 3
log_y = stat_width / 9 * 8
width_log = monitor[0] - log_x
height_log = monitor[1] - log_y
manual = ["Press \"H\" to equip Heal spell (costs 4 mana)",
          "Press \"S\" to equip Shield spell (costs 2 mana)",
          "Press \"F\" to equip Fireball spell (costs 3 mana)",
          "Use numbers 1-4 to choose your target",
          "Press \"U\" to use the chosen spell",
          "Press \"Enter\" to roll the dice and end your turn",
          "Press \"Esc\" to exit the guide play and continue the game"]
log_state = 0
text_height = 22


def show_log():
    text_frame(game_window, (log_x - 1, log_y), casual_color, width_log, height_log)
    if log_state == 0:
        print_text(game_window, "Turns: " + str(turns), (log_x + 1, log_y),
                   "white", 20, casual_font)
        for text in range(len(log)):
            print_text(game_window, log[text],
                       (log_x, log_y + text_height * (text + 1)),
                       "white", 20, casual_font)

        print_text(game_window, "Press \"i\" to see the guide play",
                   (log_x, monitor[1] - text_height - 3),
                   "white", 20, casual_font)
    elif log_state == 1:
        for x in range(len(manual)):
            print_text(game_window, manual[x], (log_x, log_y + text_height * x),
                       "white", 20, casual_font)


def update_all():
    update_map()
    for stat in range(number_of_players):
        current_stat = list_of_stats[stat]
        current_stat.show_stat(list_of_players[stat], game_window,
                               width_matrix * width_sq + 2 + (stat_width * (stat % 2)),
                               current_stat.height * (stat // 2))
    for blank in range(stat + 1, 4):
        pygame.draw.rect(screen, "gray",
                         pygame.Rect(width_matrix * width_sq + 2 + (stat_width * (blank % 2)),
                                     current_stat.height * (blank // 2),
                                     stat_width, current_stat.height))
    update_player_position()
    show_log()
    screen.blit(game_window, (0, 0))


def cast_healing_spell(player):
    if player.mana >= 4:
        if player.hp + 1 <= player.maxhp:
            player.mana -= 4
            player.hp += 1
            return True, player.name + " got +1 hp"
        else:
            return False, "HP has reached the limit"
    else:
        return False, "Not enough mana to cast Heal spell"


def cast_shield_spell(player):
    if player.mana >= 2:
        if not player.shield:
            player.mana -= 2
            player.shield_up()
            return True, player.name + " got his shield up"
        else:
            return False, "Shield is already up"
    else:
        return False, "Not enough mana to cast Shield spell"


def cast_fireball_spell(player, target_):
    player.mana -= 3
    message_ = target_.lost_hp(1)
    return message_


list_of_players = []
list_of_stats = []
number_of_players = 0
current_player = 0
set_name = 0
running = True
fireball = False
input_text = ""
game_state = 0
turns = 1
target_selection = False
success = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == 0:
                if event.key == pygame.K_RETURN:
                    try:
                        int(input_text)
                    except ValueError:
                        print("Invalid syntax")
                    else:
                        if 1 < int(input_text) < 5:
                            number_of_players = int(input_text)
                            game_state = 1
                            print("Stage 1 done")
                        else:
                            print("Invalid number")
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            elif game_state == 1:
                if event.key == pygame.K_RETURN:
                    list_of_players.append(Player(input_text, set_name + 1))
                    list_of_stats.append(Stat(stat_width, list_of_colors[set_name]))
                    input_text = ""
                    set_name += 1
                    if set_name == number_of_players:
                        game_state = 2
                        print("Stage 2 done")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            elif game_state == 2:
                if log_state == 0:
                    current = list_of_players[current_player]
                    if not target_selection:
                        if event.key == pygame.K_RETURN:
                            switch = False
                            current = list_of_players[current_player]
                            distance = current.roll_dice(10, 10, checkpoints)
                            current.get_mana(distance)
                            update_log(log, current.name + " rolled a " + str(distance))
                            if current.position == width_matrix * height_matrix:
                                running = False
                                print("You won!")
                                break
                            if matrix[current.position - 1][1].image == "Icons\GreenPortal.jpg":
                                update_all()
                                pygame.display.update()
                                pygame.event.wait(300)
                                old_position = current.position
                                switch = True
                            matrix[current.position - 1][1].activate(current)
                            if switch:
                                matrix[old_position - 1][1] = Tiles(0, 0)
                            current_player = (current_player + 1) % len(list_of_players)
                            if current_player == 0:
                                turns += 1
                            current = list_of_players[current_player]
                        elif event.key == pygame.K_h:
                            message = cast_healing_spell(current)
                            if message[0]:
                                update_log(log, message[1])
                            else:
                                warning(game_window, message[1], monitor)
                        elif event.key == pygame.K_s:
                            message = cast_shield_spell(current)
                            if message[0]:
                                update_log(log, message[1])
                            else:
                                warning(game_window, message[1], monitor)
                        elif event.key == pygame.K_f:
                            if current.mana < 3:
                                warning(game_window, "Not enough mana to cast Fireball spell",
                                        monitor)
                            else:
                                update_log(log, current.name + " uses Fireball spell")
                                target_selection = True
                        elif event.key == pygame.K_i:
                            log_state = 1
                    else:
                        message = None
                        if event.key == pygame.K_1:
                            message = cast_fireball_spell(current, list_of_players[0])
                            target_selection = False
                        elif event.key == pygame.K_2:
                            message = cast_fireball_spell(current, list_of_players[1])
                            target_selection = False
                        elif event.key == pygame.K_3 and number_of_players >= 3:
                            message = cast_fireball_spell(current, list_of_players[2])
                            target_selection = False
                        elif event.key == pygame.K_4 and number_of_players >= 4:
                            message = cast_fireball_spell(current, list_of_players[3])
                            target_selection = False
                        if message is not None:
                            for abc in range(len(message)):
                                update_log(log, message[abc])
                elif event.key == pygame.K_ESCAPE:
                    log_state = 0
    if game_state == 0:
        update_start()
        screen.blit(start_window, (0, 0))
    if game_state == 1:
        update_player(set_name)
    if game_state == 2:
        update_all()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
