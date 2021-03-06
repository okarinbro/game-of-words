import pygame
from enum import Enum
import controller_events as events
import config
import model


class FieldSprite(pygame.sprite.Sprite):
    def __init__(self, field, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.field = field
        self.image = pygame.Surface(config.FIELD_RECTANGLE)
        self.update()

    def __field_colouring(self):
        font = pygame.font.Font(config.FONT_PATH, config.FIELD_RECTANGLE[0] -
                                10)
        text = self.field.tile.__str__()
        text_img = font.render(text, 1, (0, 0, 0))
        text_rec = text_img.get_rect(center=(config.FIELD_RECTANGLE[0] // 2,
                                             config.FIELD_RECTANGLE[0] // 2))
        self.image.blit(text_img, text_rec)

        font = pygame.font.Font(config.FONT_PATH, 9)
        text = str(self.field.tile.get_value())
        text_img = font.render(text, 1, (0, 0, 0))
        text_rec = text_img.get_rect(center=(config.FIELD_RECTANGLE[0] // 2 +
                                             13,
                                             config.FIELD_RECTANGLE[0] // 2 +
                                             13))
        self.image.blit(text_img, text_rec)

    def update(self):
        if self.field.is_active:
            self.image.fill((255, 0, 208))
        else:
            self.image.fill((158, 168, 186))

        if self.field.state is model.FieldState.FIXED:
            self.image.fill((112, 165, 120))
            self.__field_colouring()
        elif self.field.state is model.FieldState.TEMPORARY:
            if not self.field.is_active:
                self.image.fill((88, 226, 109))
            self.__field_colouring()
        else:
            text = ""
            font = pygame.font.Font(config.FONT_PATH, config.FIELD_RECTANGLE[0]
                                    - 15)
            if self.field.bonus == model.Bonus.NO_BONUS:
                return
            elif self.field.bonus == model.Bonus.BONUS_2L:
                if not self.field.is_active:
                    self.image.fill((249, 240, 152))
                text = "2L"
            elif self.field.bonus == model.Bonus.BONUS_2W:
                if not self.field.is_active:
                    self.image.fill((242, 167, 82))
                text = "2W"
            elif self.field.bonus == model.Bonus.BONUS_3L:
                if not self.field.is_active:
                    self.image.fill((249, 237, 112))
                text = "3L"
            elif self.field.bonus == model.Bonus.BONUS_3W:
                if not self.field.is_active:
                    self.image.fill((221, 112, 48))
                text = "3W"
            text_img = font.render(text, 1, (140, 140, 140))
            text_rec = text_img.get_rect(center=(
                config.FIELD_RECTANGLE[0] // 2,
                config.FIELD_RECTANGLE[0] // 2))
            self.image.blit(text_img, text_rec)


class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, button, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.button = button
        self.image = pygame.Surface(self.button.shape)
        self.update()

    def __blit(self):
        font = pygame.font.Font(config.FONT_PATH, self.button.font_size)
        text_img = font.render(self.button.text, 1, (255, 255, 255))
        text_rec = text_img.get_rect(center=(self.button.shape[0] // 2,
                                             self.button.shape[1] // 2))
        self.image.blit(text_img, text_rec)

    def update(self):
        if self.button.type is ButtonShapeType.RECTANGLE:
            self.image.fill(self.button.bg_color)
            self.__blit()

        elif self.button.type is ButtonShapeType.CIRCLE:
            pygame.draw.circle(self.image, self.button.bg_color,
                               (self.button.shape[0] // 2,
                                self.button.shape[0] // 2),
                               self.button.shape[0] // 2)
            self.__blit()


class BannerSprite(pygame.sprite.Sprite):
    def __init__(self, banner, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.banner = banner
        self.image = pygame.Surface(self.banner.shape)
        self.update()

    def __blit(self):
        font = pygame.font.Font(config.FONT_PATH, self.banner.font_size)
        text_img = font.render(self.banner.text, 1, (255, 255, 255))
        text_rec = text_img.get_rect(center=(self.banner.shape[0] // 2,
                                             self.button.shape[1] // 2))
        self.image.blit(text_img, text_rec)

    def update(self):
        self.image.fill(self.banner.bg_color)
        self.__blit()


class ScoreBoardSprite(pygame.sprite.Sprite):
    def __init__(self, score_board, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.players = score_board.players
        self.shape = score_board.shape
        self.image = pygame.Surface(self.shape)
        self.update()

    def __blit(self):
        font = pygame.font.Font(config.FONT_PATH, 25)
        score_text = "SCOREBOARD"
        text_img = font.render(score_text, 1, (250, 250, 250))
        text_rec = text_img.get_rect(center=(self.shape[0] // 2,
                                             self.shape[1] // 6))
        self.image.blit(text_img, text_rec)

        font = pygame.font.Font(config.FONT_PATH, 20)
        score_text = self.players[0].name + " : " + str(self.players[0].score)
        text_img = font.render(score_text, 1, (250, 250, 250))
        text_rec = text_img.get_rect(center=(self.shape[0] // 2 - 20,
                                             self.shape[1] // 2 - 10))
        self.image.blit(text_img, text_rec)

        font = pygame.font.Font(config.FONT_PATH, 20)
        score_text = self.players[1].name + " : " + str(self.players[1].score)
        text_img = font.render(score_text, 1, (250, 250, 250))
        text_rec = text_img.get_rect(center=(self.shape[0] // 2 - 20,
                                             2 * self.shape[1] // 3 + 10))
        self.image.blit(text_img, text_rec)

    def update(self, *args):
        self.image.fill((80, 80, 80))
        self.__blit()


class DifficultyDashSprite(pygame.sprite.Sprite):
    def __init__(self, difficulty_level, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.shape = config.DIFFICULTY_DASH_SHAPE
        self.image = pygame.Surface(self.shape)
        self.difficulty_level = difficulty_level
        self.update()

    def __blit(self):
        font = pygame.font.Font(config.FONT_PATH, 20)
        score_text = "Difficulty level"
        text_img = font.render(score_text, 1, (250, 250, 250))
        text_rec = text_img.get_rect(center=(self.shape[0] // 2,
                                             self.shape[1] // 5))
        self.image.blit(text_img, text_rec)

        font = pygame.font.Font(config.FONT_PATH, 30)
        if self.difficulty_level == model.DifficultyLevel.EASY:
            text = "EASY"
        elif self.difficulty_level == model.DifficultyLevel.MEDIUM:
            text = "MEDIUM"
        else:
            text = "HARD"

        text_img = font.render(text, 1, (250, 250, 250))
        text_rec = text_img.get_rect(center=(self.shape[0] // 2 - 5,
                                             self.shape[1] // 2 + 10))
        self.image.blit(text_img, text_rec)

    def update(self, *args):
        self.image.fill((80, 80, 80))
        self.__blit()


class ButtonShapeType(Enum):
    RECTANGLE = 0
    CIRCLE = 1


class Button:
    def __init__(self, type, text, font_size, bg_color, shape,
                 left_edge_offset, top_edge_offset):
        self.type = type
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.shape = shape
        self.left_edge_offset = left_edge_offset
        self.top_edge_offset = top_edge_offset


class Banner:
    def __init__(self, text, font_size, bg_color, shape,
                 left_edge_offset, top_edge_offset):
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.shape = shape  # (dimensions of rectangle)
        self.left_edge_offset = left_edge_offset
        self.top_edge_offset = top_edge_offset


class GameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register(self)

        pygame.init()
        self.window = pygame.display.set_mode((config.WINDOW_WIDTH,
                                               config.WINDOW_HEIGHT))
        pygame.display.set_caption('Game of Words')
        self.background = pygame.Surface(self.window.get_size())

        self.clean('images/main_background.jpg')
        pygame.time.delay(1650)
        self.print_line("Game", (config.WINDOW_WIDTH / 2,
                                 config.WINDOW_HEIGHT / 2 - 200),
                        150, (0, 0, 0))
        pygame.time.delay(1200)
        self.print_line("of", (config.WINDOW_WIDTH / 2,
                               config.WINDOW_HEIGHT / 2),
                        150, (0, 0, 0))
        pygame.time.delay(1200)
        self.print_line("Words", (config.WINDOW_WIDTH / 2,
                                  config.WINDOW_HEIGHT / 2 + 200),
                        150, (0, 0, 0))

        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()

        pygame.time.delay(1000)

    def show_board(self, board):
        pygame.display.flip()
        column = 0

        field_rect = pygame.Rect(
            (config.LEFT_EDGE_BOARD_OFFSET - config.FIELD_RECTANGLE_WIDTH,
             config.TOP_EDGE_BOARD_OFFSET,
             config.FIELD_RECTANGLE[0], config.FIELD_RECTANGLE[0]))

        for row in board.fields:
            for field in row:
                if column < config.BOARD_SIZE:
                    field_rect = field_rect.move(
                        config.FIELD_RECTANGLE_WIDTH, 0)
                else:
                    column = 0
                    field_rect = field_rect.move(-(config.BOARD_SIZE - 1) *
                                                 config.FIELD_RECTANGLE_WIDTH,
                                                 config.FIELD_RECTANGLE_WIDTH)
                column += 1
                new_field_sprite = FieldSprite(field, self.back_sprites)
                new_field_sprite.rect = field_rect

    def show_tilebox(self, tilebox):
        field_rect = pygame.Rect(
            (config.LEFT_EDGE_TILEBOX_OFFSET - config.FIELD_RECTANGLE_WIDTH,
             config.TOP_EDGE_TILEBOX_OFFSET,
             config.FIELD_RECTANGLE[0],
             config.FIELD_RECTANGLE[0]))

        for field in tilebox.fields:
            field_rect = field_rect.move(config.FIELD_RECTANGLE_WIDTH, 0)
            new_field_sprite = FieldSprite(field, self.back_sprites)
            new_field_sprite.rect = field_rect

    def show_button(self, button):
        button_rect = pygame.Rect((button.left_edge_offset,
                                   button.top_edge_offset,
                                   button.shape[0], button.shape[1]
                                   if button.type == ButtonShapeType.RECTANGLE
                                   else button.shape[0]))
        new_button_sprite = ButtonSprite(button, self.front_sprites)
        new_button_sprite.rect = button_rect

    def show_buttons(self, buttons):
        for button in buttons:
            self.show_button(button)

    def draw_everything(self):
        self.back_sprites.clear(self.window, self.background)
        self.front_sprites.clear(self.window, self.background)

        self.back_sprites.update()
        self.front_sprites.update()

        dirty_rects1 = self.back_sprites.draw(self.window)
        dirty_rects2 = self.front_sprites.draw(self.window)

        dirty_rects = dirty_rects1 + dirty_rects2
        pygame.display.update(dirty_rects)

    def clean(self, image_path=None):
        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()
        if image_path is not None:
            image = pygame.image.load(image_path)
            rect = image.get_rect()
            rect.left, rect.top = (0, 0)
            self.background.fill([255, 255, 255])
            self.background.blit(image, rect)
        else:
            self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def show_other_player_move_banner(self):
        self.clean('images/background.jpg')
        self.print_line("Brace", (config.WINDOW_WIDTH // 2 - 300, 200),
                        100, (0, 0, 0))
        self.print_line("yourself!", (config.WINDOW_WIDTH // 2 - 200, 350),
                        100, (0, 0, 0))
        pygame.time.delay(1000)

    def print_line(self, text, position, font_size,
                   font_colour=(255, 255, 255)):

        font = pygame.font.Font(config.FONT_PATH, font_size)
        text_img = font.render(text, 1, font_colour)
        text_rec = text_img.get_rect(center=position)
        self.background.blit(text_img, text_rec)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def show_about_banner(self):
        self.clean('images/main_background.jpg')
        self.print_line("About", (config.WINDOW_WIDTH / 2, 100),
                        100, (0, 0, 0))
        self.print_line("\"That's what we do.", (config.WINDOW_WIDTH / 2, 250),
                        50, (0, 0, 0))
        self.print_line("We  code  and  we  know  things.\"",
                        (config.WINDOW_WIDTH / 2, 320), 50, (0, 0, 0))

        self.print_line("Created by", (config.WINDOW_WIDTH / 2, 450),
                        25, (0, 0, 0))
        self.print_line("PRZEMYSLAW  JABLECKI", (config.WINDOW_WIDTH / 2,
                                                 480), 28, (0, 0, 0))
        self.print_line("FILIP  SLAZYK", (config.WINDOW_WIDTH / 2, 510),
                        28, (0, 0, 0))
        self.print_line("2019", (config.WINDOW_WIDTH / 2, 600), 32, (0, 0, 0))

    def get_field_sprite(self, field):
        for sprite in self.back_sprites:
            if hasattr(sprite, "field") and sprite.field == field:
                return sprite

    def show_score_board(self, score_board):
        score_board_rect = pygame.Rect(config.LEFT_EDGE_SCOREBOARD_OFFSET,
                                       config.TOP_EDGE_SCOREBOARD_OFFSET,
                                       *config.SCOREBOARD_SHAPE)
        new_score_board_sprite = ScoreBoardSprite(score_board,
                                                  self.front_sprites)
        new_score_board_sprite.rect = score_board_rect

    def show_title(self):
        self.print_line('Game of Words', (config.WINDOW_WIDTH / 2, 60),
                        50, (0, 0, 0))

    def show_difficulty_dash(self, difficulty_level):
        dash_rect = pygame.Rect(config.LEFT_EDGE_DIFFICULTY_DASH_OFFSET,
                                config.TOP_EDGE_DIFFICULTY_DASH_OFFSET,
                                *config.DIFFICULTY_DASH_SHAPE)
        new_score_board_sprite = DifficultyDashSprite(difficulty_level,
                                                      self.front_sprites)
        new_score_board_sprite.rect = dash_rect

    def build_menu_event(self, buttons):
        self.clean('images/main_background.jpg')
        self.print_line('Game of Words', (config.WINDOW_WIDTH / 2, 180),
                        100, (0, 0, 0))
        self.show_buttons(buttons)

    def build_difficulty_menu_event(self, buttons):
        self.clean('images/main_background.jpg')
        self.print_line('Select level of difficulty', (config.WINDOW_WIDTH / 2,
                                                       180), 50, (0, 0, 0))
        self.show_buttons(buttons)

    def build_edit_dashboard(self, buttons, board):
        self.clean('images/main_background.jpg')
        self.print_line('Edit  fields  on  board', (config.WINDOW_WIDTH / 2,
                                                    50), 50, (0, 0, 0))
        self.show_buttons(buttons)
        self.show_board(board)

    def game_end(self, event):
        if event.players[0].score > event.players[1].score:
            self.clean("images/win_view.jpg")
            self.print_line("You", (config.WINDOW_WIDTH / 4 - 70, 120), 100)
            self.print_line("WIN!", (config.WINDOW_WIDTH / 2 + 230, 300), 100)

        else:
            self.clean("images/surrender_screen.jpg")
            self.print_line("You", (config.WINDOW_WIDTH / 4 - 70, 90), 70,
                            (0, 0, 0))
            self.print_line("have", (config.WINDOW_WIDTH / 2 + 200, 120), 70,
                            (0, 0, 0))
            self.print_line("been", (config.WINDOW_WIDTH / 4 - 50, 200), 70,
                            (0, 0, 0))
            self.print_line("DEFEATED!", (config.WINDOW_WIDTH / 2 + 230, 280),
                            70, (0, 0, 0))

    def surrender(self):
        print("DONE")
        self.clean("images/surrender_screen.jpg")
        self.print_line("You", (config.WINDOW_WIDTH / 4 - 70, 90), 70,
                        (0, 0, 0))
        self.print_line("have", (config.WINDOW_WIDTH / 2 + 200, 120), 70,
                        (0, 0, 0))
        self.print_line("been", (config.WINDOW_WIDTH / 4 - 50, 200), 70,
                        (0, 0, 0))
        self.print_line("DEFEATED!", (config.WINDOW_WIDTH / 2 + 230, 280), 70,
                        (0, 0, 0))

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            self.draw_everything()
        elif isinstance(event, events.BoardBuildEvent):
            self.show_board(event.board)
        elif isinstance(event, events.TileBoxBuildEvent):
            self.show_tilebox(event.tilebox)
        elif isinstance(event, events.UpdateFieldEvent):
            self.get_field_sprite(event.field)
        elif isinstance(event, events.DrawGameButtonsEvent):
            self.show_buttons(event.buttons)
        elif isinstance(event, events.OtherPlayerTurnEvent):
            self.show_other_player_move_banner()
        elif isinstance(event, events.ScoreBoardBuildEvent):
            self.show_score_board(event.score_board)
        elif isinstance(event, events.MenuBuildEvent):
            self.build_menu_event(event.buttons)
        elif isinstance(event, events.ClearScreenEvent):
            self.clean(event.image_path)
        elif isinstance(event, events.AboutBannerShowEvent):
            self.clean()
            self.show_about_banner()
            pygame.time.wait(5000)
            self.clean()
            self.evManager.post(events.MenuBuildEvent())
        elif isinstance(event, events.EndGameEvent):
            self.game_end(event)
        elif isinstance(event, events.SurrenderEvent):
            self.surrender()
        elif isinstance(event, events.MenuDifficultyBuildEvent):
            self.build_difficulty_menu_event(event.buttons)
        elif isinstance(event, events.DifficultyLevelDash):
            self.show_difficulty_dash(event.difficulty_level)
        elif isinstance(event, events.TitleBuildEvent):
            self.show_title()
        elif isinstance(event, events.EditDashboardBuildEvent):
            self.clean()
            self.build_edit_dashboard(event.buttons, event.board)
