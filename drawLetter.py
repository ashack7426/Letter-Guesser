import installReqs
import pygame
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import messagebox
from sklearn.model_selection import train_test_split
import pandas as pd
from PIL import Image
import cv2


class pixel(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.neighbors = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y,
                         self.x + self.width, self.y + self.height))

    def getNeighbors(self, g):
        # Get the neighbours of each pixel in the grid, this is used for drawing thicker lines
        j = self.x // 20  # the var i is responsible for denoting the current col value in the grid
        i = self.y // 20  # the var j is responsible for denoting thr current row value in the grid
        rows = 28
        cols = 28

        # Horizontal and vertical neighbors
        if i < cols - 1:  # Right
            self.neighbors.append(g.pixels[i + 1][j])
        if i > 0:  # Left
            self.neighbors.append(g.pixels[i - 1][j])
        if j < rows - 1:  # Up
            self.neighbors.append(g.pixels[i][j + 1])
        if j > 0:  # Down
            self.neighbors.append(g.pixels[i][j - 1])

        # Diagonal neighbors
        if j > 0 and i > 0:  # Top Left
            self.neighbors.append(g.pixels[i - 1][j - 1])

        if j + 1 < rows and i > -1 and i - 1 > 0:  # Bottom Left
            self.neighbors.append(g.pixels[i - 1][j + 1])

        if j - 1 < rows and i < cols - 1 and j - 1 > 0:  # Top Right
            self.neighbors.append(g.pixels[i + 1][j - 1])

        if j < rows - 1 and i < cols - 1:  # Bottom Right
            self.neighbors.append(g.pixels[i + 1][j + 1])


class grid(object):
    pixels = []

    def __init__(self, row, col, width, height):
        self.rows = row
        self.cols = col
        self.len = row * col
        self.width = width
        self.height = height
        self.generatePixels()
        pass

    def draw(self, surface):
        for row in self.pixels:
            for col in row:
                col.draw(surface)

    def generatePixels(self):
        x_gap = self.width // self.cols
        y_gap = self.height // self.rows
        self.pixels = []
        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(
                    pixel(x_gap * c, y_gap * r, x_gap, y_gap))

        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].getNeighbors(self)

    def clicked(self, pos):  # Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            g1 = int(t) // self.pixels[0][0].width
            g2 = int(w) // self.pixels[0][0].height

            return self.pixels[g2][g1]
        except:
            pass

    def get_img(self):
        li = self.pixels
        pixels = [[] for x in range(len(li))]

        for i in range(len(li)):
            for j in range(len(li[i])):
                if li[i][j].color == (255, 255, 255):
                    pixels[i].append((255, 255, 255))
                else:
                    pixels[i].append((0, 0, 0))

        A = np.array(pixels, dtype=np.uint8)
        im = Image.fromarray(A)
        im.save('new.jpg')

        img = cv2.imread(r'new.jpg')
        img_copy = img.copy()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 440))

        img_copy = cv2.GaussianBlur(img_copy, (7, 7), 0)
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(
            img_gray, 100, 255, cv2.THRESH_BINARY_INV)
        img_final = cv2.resize(img_thresh, (28, 28))
        img_final = np.reshape(img_final, (1, 28, 28, 1))

        return img_final


def guess(li):
    word_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
                 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

    model = tf.keras.models.load_model('model.h5')
    letter = word_dict[np.argmax(model.predict(li))]

    predictions = model.predict(li)
    print(letter)
    print("I predict this letter is:", letter)
    window = Tk()
    window.withdraw()
    messagebox.showinfo("Prediction", "I predict this letter is: " + letter)
    window.destroy()
    #plt.imshow(li[0], cmap=plt.cm.binary)
    # plt.show()


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    li = g.get_img()
                    guess(li)
                    g.generatePixels()

                if event.key == pygame.K_c:
                    g.generatePixels()

            if pygame.mouse.get_pressed()[0]:

                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)
                clicked.color = (0, 0, 0)
                for n in clicked.neighbors:
                    n.color = (0, 0, 0)

            if pygame.mouse.get_pressed()[2]:
                try:
                    pos = pygame.mouse.get_pos()
                    clicked = g.clicked(pos)
                    clicked.color = (255, 255, 255)
                except:
                    pass

        g.draw(win)
        pygame.display.update()


pygame.init()
width = height = 560
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Letter Guesser")
g = grid(28, 28, width, height)
main()


pygame.quit()
quit()
