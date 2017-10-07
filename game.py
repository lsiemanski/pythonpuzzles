import pygame
import random
import math
import sys
from PIL import Image

class FullImage():
    def __init__(self, path):
        self.original_path = path
        self.original_img = Image.open(self.original_path)
        self.original_width, self.original_height = self.original_img.size
        self.image = self.original_img.resize(self.set_width_and_height())
        self.cropped_images = []

    def set_width_and_height(self):
        width = self.original_width - self.original_width % 4
        height = self.original_height - self.original_height % 4
        return (width, height)

    def get_width_and_height(self):
        return self.image.size

    def get_piece_width_and_height(self):
        width, height = self.get_width_and_height()
        return int(width/4), int(height/4)

    def crop_images_into_pieces(self, piece_width, piece_height):
        for i in range(16):
            startX = i % 4 * piece_width
            startY = math.floor(i / 4) * piece_height
            cropped = self.image.crop((startX, startY, piece_width + startX, piece_height + startY))
            self.cropped_images.append(cropped)
        return self.cropped_images

class Piece():
    def __init__(self, img, posX, posY, number, width, height):
        self.image = pygame.image.fromstring(img, (width, height), 'RGB')
        self.rect = self.image.get_rect()
        self.rect.topleft = posX, posY
        self.number = number
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def good_position(self):
        good_position = (self.number % 4 * self.width, math.floor(self.number / 4) * self.height)
        if good_position == self.rect.topleft:
            return True
        else:
            return False

class Game():
    def __init__(self, full_image):
        pygame.init()

        self.screen = pygame.display.set_mode((full_image.original_width, full_image.original_height))
        pygame.display.set_caption('Slide puzzles!')

        self.pieces = []

        self.piece_width, self.piece_height = full_image.get_piece_width_and_height()
        self.create_pieces(full_image, self.piece_width, self.piece_height)

    def create_pieces(self, full_image, piece_width, piece_height):
        cropped_images = full_image.crop_images_into_pieces(piece_width, piece_height)
        pieces_numbers = list(range(15))
        pieces_order = list()
        while pieces_numbers:
            choice = random.choice(pieces_numbers)
            pieces_order.append(choice)
            pieces_numbers.remove(choice)

        for i in range(15):
            image = cropped_images[pieces_order[i]].tobytes("raw", 'RGB')
            posX = i % 4 * piece_width
            posY = math.floor(i / 4) * piece_height
            self.pieces.append(Piece(image, posX, posY, pieces_order[i], self.piece_width, self.piece_height))

        self.last_piece = self.create_last_piece(cropped_images[15].tobytes("raw", 'RGB'))

    def win(self, order):
        winning_order = []
        for i in range(15):
            winning_order.append(True)
        if set(order) == set(winning_order):
            return True
        else:
            return False

    def create_last_piece(self, image):
        return Piece(image, self.piece_width*3, self.piece_height*3, 15, self.piece_width, self.piece_height)

    def run(self):
        won = False
        fpsController = pygame.time.Clock()
        blank_space = [self.piece_width*3, self.piece_height*3]
        move = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and won == False:
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        if blank_space[0] != 0:
                            move = 'Right'
                            blank_space[0] -= self.piece_width
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        if blank_space[0] != self.piece_width*3:
                            move = 'Left'
                            blank_space[0] += self.piece_width
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        if blank_space[1] != self.piece_height*3:
                            move = 'Up'
                            blank_space[1] += self.piece_height
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        if blank_space[1] != 0:
                            move = 'Down'
                            blank_space[1] -= self.piece_height

            self.screen.fill(pygame.Color(255, 255, 255))

            order = []

            for piece in self.pieces:
                pos = list(piece.rect.topleft)
                if pos == blank_space:
                    if move == 'Up':
                        pos[1] -= self.piece_height
                    elif move == 'Down':
                        pos[1] += self.piece_height
                    elif move == 'Right':
                        pos[0] += self.piece_width
                    elif move == 'Left':
                        pos[0] -= self.piece_width
                piece.rect.topleft = tuple(pos)
                order.append(piece.good_position())
                piece.draw(self.screen)

            if self.win(order) == True:
                self.last_piece.draw(self.screen)
                won = True

            pygame.display.flip()
            fpsController.tick(24)

original_path = 'kobe.jpg'
full_image = FullImage(original_path)

Game(full_image).run()