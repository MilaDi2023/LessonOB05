# ИГРА ЗМЕЙКА.
# Этот код помог сгенерировать ИИ-помощник с плагином Code Interpreter

import pygame
import time
import random

# Инициализация всех импортированных модулей pygame
pygame.init()

# Определение цветов для использования в игре
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
blue = (50, 153, 213)
# Цвета для кнопок в их активном и неактивном состояниях
bright_green = (0, 255, 0)
bright_red = (255, 0, 0)
dark_green = (0, 200, 0)
dark_red = (200, 0, 0)
green = (0, 255, 0)
red = (213, 50, 80)

# Установка размеров игрового окна
dis_width = 600
dis_height = 400

# Создание игрового окна
dis = pygame.display.set_mode((dis_width, dis_height))
# Установка заголовка окна
pygame.display.set_caption('Змейка')

# Создание объекта для отслеживания времени
clock = pygame.time.Clock()

# Определение размеров блока змейки и скорости игры
snake_block = 10
snake_speed = 7

# Создание шрифтов для отображения текста
font_style = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Функция для отрисовки змейки
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Функция для отображения сообщений
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])

# Функция для создания кнопок
def button(msg, x, y, w, h, ic, ac, tc, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("Arial", 20)
    textSurf, textRect = text_objects(msg, smallText, tc)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(textSurf, textRect)

# Функция для создания текстовых объектов
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Функция для выхода из игры
def quitgame():
    pygame.quit()
    quit()

# Функция для центрирования сообщений
def message(msg, color, y):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, y))
    dis.blit(mesg, mesg_rect)

# Размеры и расстояние между кнопками
button_width = 150
button_height = 50
button_spacing = 150

# Расчет расположения кнопок
total_buttons_width = (2 * button_width) + button_spacing
first_button_x = (dis_width - total_buttons_width) / 2
second_button_x = first_button_x + button_width + button_spacing

# Основной игровой цикл
def gameLoop():
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Начальные изменения координат змейки
    x1_change = 0
    y1_change = 0

    # Список, содержащий сегменты змейки и начальная длина змейки
    snake_List = []
    Length_of_snake = 1

    # Расположение первой еды
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Цикл, пока игра не закончится
    while not game_over:

        # Если игра закрыта, показать сообщение о проигрыше и кнопки
        while game_close == True:
            dis.fill(blue)
            message("Вы проиграли!", white, dis_height / 3)
            button("Играть заново", first_button_x, dis_height / 2, button_width, button_height, dark_green,
                   bright_green, black, gameLoop)
            button("Выйти", second_button_x, dis_height / 2, button_width, button_height, dark_red, bright_red, white,
                   quitgame)
            pygame.display.update()

            # Обработка событий выхода из игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Обработка событий нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка столкновения змейки со стенами
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка столкновения головы змейки с ее телом
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Отрисовка змейки
        our_snake(snake_block, snake_List)

        # Обновление экрана
        pygame.display.update()

        # Проверка съедания еды змейкой
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Контроль скорости игры
        clock.tick(snake_speed)

    # Выход из игры после окончания игрового цикла
    pygame.quit()
    quit()

# Запуск игрового цикла
gameLoop()