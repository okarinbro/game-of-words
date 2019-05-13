# GLOBAL PARAMETERS
# view parameters - width 1000 px.  , height 700 px.

import pygame

import config
import controller
import model


class FieldSprite(pygame.sprite.Sprite):
    def __init__(self, field, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.field = field
        self.image = pygame.Surface(config.FIELD_RECTANGLE)
        if field.is_active:
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((0, 255, 255))

        if field.state is model.FieldState.FIXED:
            self.image.fill((200, 50, 0))
            font = pygame.font.Font(None, config.FIELD_RECTANGLE[0])
            text = field.tile.__str__()
            text_img = font.render(text, 1, (255, 255, 255))
            text_rec = text_img.get_rect(center=(config.FIELD_RECTANGLE[0] // 2, config.FIELD_RECTANGLE[0] // 2))
            self.image.blit(text_img, text_rec)
        elif field.state is model.FieldState.TEMPORARY:
            if field.is_active:
                self.image.fill((255, 255, 0))
            else:
                self.image.fill((55, 55, 0))
            font = pygame.font.Font(None, config.FIELD_RECTANGLE[0])
            text = field.tile.__str__()
            text_img = font.render(text, 1, (255, 255, 255))
            text_rec = text_img.get_rect(center=(config.FIELD_RECTANGLE[0] // 2, config.FIELD_RECTANGLE[0] // 2))
            self.image.blit(text_img, text_rec)


class GameView:
    # def __init__(self, evManager):
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register(self)

        pygame.init()
        self.window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption('Word of Games')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        font = pygame.font.Font(None, 150)
        text = "Game of Words"
        text_img = font.render(text, 1, (255, 255, 255))
        text_rec = text_img.get_rect(center=(config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2))
        self.background.blit(text_img, text_rec)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()
        self.board_sprites = pygame.sprite.RenderUpdates()

        # pygame.time.delay(2000)
        pygame.time.delay(200)

    def show_board(self, board):
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        field_rect = pygame.Rect(
            (config.LEFT_EDGE_BOARD_OFFSET - config.FIELD_RECTANGLE_WIDTH, config.TOP_EDGE_BOARD_OFFSET, config.FIELD_RECTANGLE[0],
             config.FIELD_RECTANGLE[0]))

        column = 0

        for row in board.fields:
            for field in row:
                if column < config.BOARD_SIZE:
                    field_rect = field_rect.move(config.FIELD_RECTANGLE_WIDTH, 0)
                else:
                    column = 0
                    field_rect = field_rect.move(-(config.BOARD_SIZE - 1) * config.FIELD_RECTANGLE_WIDTH,
                                                 config.FIELD_RECTANGLE_WIDTH)
                column += 1
                new_field_sprite = FieldSprite(field, self.back_sprites)
                new_field_sprite.rect = field_rect
                new_field_sprite = None

    def show_tilebox(self, tilebox):

        field_rect = pygame.Rect(
            (config.LEFT_EDGE_TILEBOX_OFFSET - config.FIELD_RECTANGLE_WIDTH, config.TOP_EDGE_TILEBOX_OFFSET, config.FIELD_RECTANGLE[0],
             config.FIELD_RECTANGLE[0]))

        column = 0
        for field in tilebox.fields:
            field_rect = field_rect.move(config.FIELD_RECTANGLE_WIDTH, 0)
            new_field_sprite = FieldSprite(field, self.back_sprites)
            new_field_sprite.rect = field_rect
            new_field_sprite = None

    def draw_everything(self):
        self.back_sprites.clear(self.window, self.background)
        self.front_sprites.clear(self.window, self.background)
        self.board_sprites.clear(self.window, self.background)

        self.back_sprites.update()
        self.front_sprites.update()

        dirty_rects1 = self.back_sprites.draw(self.window)
        dirty_rects2 = self.front_sprites.draw(self.window)

        dirty_rects = dirty_rects1 + dirty_rects2
        pygame.display.update(dirty_rects)

    def notify(self, event):
        if isinstance(event, controller.TickEvent):
            self.draw_everything()
        elif isinstance(event, controller.BoardBuildEvent):
            self.show_board(event.board)
        elif isinstance(event, controller.TileBoxBuildEvent):
            self.show_tilebox(event.tilebox)

