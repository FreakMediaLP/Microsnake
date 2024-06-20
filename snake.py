from machine import Pin, I2C, reset, PWM
import ssd1306
import random
import time
import json

# OLED display dimensions
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Pin definitions
NOTE_C6 = 1047
OLED_RESET = 4
SOUND_PIN = 21
buttonPins = [33, 25, 26, 27]  # LEFT, UP, RIGHT, DOWN


# Enums
class GameState:
    START = 0
    RUNNING = 1
    GAMEOVER = 2
    FINISHED = 3


class Direction:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


# Game constants
SNAKE_PIECE_SIZE = 3

# Initialize game variables
gameState = GameState.START

snake_length = 0
startDir = Direction.RIGHT
newDir = Direction.RIGHT
fruit = [0, 0]
moveTime = 0

# Initialize I2C and display
i2c = I2C(scl=Pin(23), sda=Pin(22))
display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# Initialize buttons
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in buttonPins]

# Setup settings arrays
difficultyLevels = [30, 20, 10, 5]
difficultyNames = ["Easy", "Medium", "Hard", "Ultra"]
mapSizes = [3, 5, 10, 20]  # Tiny, Small, Medium, Large
startingSizes = [2, 3, 4, 5]  # Corresponding to map sizes
soundOptions = [True, False]  # Yes, No

# Selected settings indices
try:
    with open("settings.json", "r") as file:
        data = json.load(file)
        selectedSetting = data["selectedSetting"]
        selectedDifficulty = data["selectedDifficulty"]
        selectedMapSize = data["selectedMapSize"]
        selectedSound = data["selectedSound"]
except (FileNotFoundError, KeyError):
    selectedSetting = 0
    selectedDifficulty = 1
    selectedMapSize = 2
    selectedSound = 0


def setup():
    for button in buttons:
        button.init(Pin.IN, Pin.PULL_UP)
    random.seed(time.ticks_ms())
    drawPressToStartGame()
    time.sleep(0.25)
    setupSettingsMenu()


def setupSettingsMenu():
    global selectedSetting, selectedDifficulty, selectedMapSize, selectedSound
    displaySettingsMenu()

    while True:
        if not buttons[1].value():  # UP button
            selectedSetting = (selectedSetting - 1) % 4
            displaySettingsMenu()
            time.sleep(0.2)
        elif not buttons[3].value():  # DOWN button
            selectedSetting = (selectedSetting + 1) % 4
            displaySettingsMenu()
            time.sleep(0.2)
        elif not buttons[0].value():  # LEFT button
            if selectedSetting == 0:
                selectedDifficulty = (selectedDifficulty - 1) % len(difficultyLevels)
            elif selectedSetting == 1:
                selectedMapSize = (selectedMapSize - 1) % len(mapSizes)
            elif selectedSetting == 2:
                selectedSound = (selectedSound - 1) % len(soundOptions)
            elif selectedSetting == 3:  # LEFT or RIGHT button to start game
                break
            displaySettingsMenu()
            time.sleep(0.2)
        elif not buttons[2].value():  # RIGHT button
            if selectedSetting == 0:
                selectedDifficulty = (selectedDifficulty + 1) % len(difficultyLevels)
            elif selectedSetting == 1:
                selectedMapSize = (selectedMapSize + 1) % len(mapSizes)
            elif selectedSetting == 2:
                selectedSound = (selectedSound + 1) % len(soundOptions)
            elif selectedSetting == 3:  # LEFT or RIGHT button to start game
                break
            displaySettingsMenu()
            time.sleep(0.2)
        time.sleep(0.01)

    # Apply selected settings
    global SNAKE_MOVE_DELAY, MAP_SIZE, STARTING_SNAKE_SIZE, BUZZER_PIN
    SNAKE_MOVE_DELAY = difficultyLevels[selectedDifficulty]
    MAP_SIZE = mapSizes[selectedMapSize]
    STARTING_SNAKE_SIZE = startingSizes[selectedMapSize]
    BUZZER_PIN = SOUND_PIN if soundOptions[selectedSound] else None

    # Save selected settings
    with open("settings.json", 'w') as outfile:
        data_out = {"selectedSetting": selectedSetting, "selectedDifficulty": selectedDifficulty,
                    "selectedMapSize": selectedMapSize, "selectedSound": selectedSound}
        json.dump(data_out, outfile)

    setupGame()


def displaySettingsMenu():
    display.fill(0)
    settings = ["Diffic:", "Map Size:", "Sound:", "Start Game"]
    values = [difficultyNames[selectedDifficulty], mapSizes[selectedMapSize],
              "Yes" if soundOptions[selectedSound] else "No", ""]

    for i, setting in enumerate(settings):
        if i == selectedSetting:
            display.text(f"> {setting}{values[i]}", 2, 10 + i * 10, 1)
        else:
            display.text(f"  {setting}{values[i]}", 2, 10 + i * 10, 1)

    display.show()


def drawPressToStartGame():
    display.fill(0)
    display.text("MICROSNAKE", 2, 10, 1)
    display.text("ON ESP32", 2, 20, 1)
    display.text("BY Joos_too", 2, 30, 1)
    display.text("PRESS BUTTON", 2, 50, 1)
    display.show()
    while not buttonPress():
        time.sleep(0.01)


def resetSnake():
    global snake_length
    snake_length = STARTING_SNAKE_SIZE
    for i in range(snake_length):
        snake[i][0] = MAP_SIZE // 2 - i
        snake[i][1] = MAP_SIZE // 2


def setupGame():
    global startDir, newDir, gameState, moveTime, snake, MAX_SNAKE_LENGTH

    # Calculate values
    MAX_SNAKE_LENGTH = MAP_SIZE * MAP_SIZE
    snake = [[0, 0] for _ in range(MAX_SNAKE_LENGTH)]

    gameState = GameState.START
    startDir = Direction.RIGHT
    newDir = Direction.RIGHT
    moveTime = 0

    resetSnake()
    generateFruit()
    display.fill(0)

    drawMap()
    drawScore()
    drawPressToStart()
    display.show()


def loop():
    global gameState, startDir, newDir, moveTime
    while True:
        if gameState == GameState.START:
            if buttonPress():
                gameState = GameState.RUNNING

        elif gameState == GameState.RUNNING:
            moveTime += 1
            readDirection()
            if moveTime >= SNAKE_MOVE_DELAY:
                startDir = newDir
                display.fill(0)
                if moveSnake():
                    gameState = GameState.GAMEOVER
                    drawGameover()
                    time.sleep(1)
                drawMap()
                drawScore()
                display.show()
                checkFruit()
                moveTime = 0
        elif gameState == GameState.GAMEOVER or gameState == GameState.FINISHED:
            if buttonPress():
                time.sleep(0.5)
                setupGame()
                gameState = GameState.START
        time.sleep(0.01)


def buttonPress():
    for button in buttons:
        if not button.value():
            return True
    return False


def readDirection():
    global newDir
    for i, button in enumerate(buttons):
        if not button.value() and i != (startDir + 2) % 4:
            newDir = i
            return


def moveSnake():
    global snake_length
    x, y = snake[0]

    if startDir == Direction.LEFT:
        x -= 1
    elif startDir == Direction.UP:
        y -= 1
    elif startDir == Direction.RIGHT:
        x += 1
    elif startDir == Direction.DOWN:
        y += 1

    if collisionCheck(x, y):
        return True

    for i in range(snake_length - 1, 0, -1):
        snake[i] = list(snake[i - 1])

    snake[0] = [x, y]
    return False


def checkFruit():
    global snake_length, gameState
    if fruit == snake[0]:
        if BUZZER_PIN:
            # Play the note and stop the tone after 0.1s
            buzzer = PWM(Pin(BUZZER_PIN))
            buzzer.freq(NOTE_C6)
            buzzer.duty_u16(32768)
            time.sleep(0.05)
            buzzer.duty_u16(0)
        else:
            print("No Sound Mode activated")

        if snake_length + 1 <= MAX_SNAKE_LENGTH:
            snake_length += 1
        else:
            gameState = GameState.FINISHED
            drawWin()
            display.show()
        generateFruit()


def generateFruit():
    while True:
        fruit[0] = random.randint(0, MAP_SIZE - 1)
        fruit[1] = random.randint(0, MAP_SIZE - 1)
        if not any(fruit == part for part in snake[:snake_length]):
            break


def collisionCheck(x, y):
    if x < 0 or y < 0 or x >= MAP_SIZE or y >= MAP_SIZE:
        return True
    if any([x, y] == part for part in snake[1:snake_length]):
        return True
    return False


def drawMap():
    offset_map_x = SCREEN_WIDTH - SNAKE_PIECE_SIZE * MAP_SIZE - 2
    offset_map_y = 2

    display.rect(fruit[0] * SNAKE_PIECE_SIZE + offset_map_x, fruit[1] * SNAKE_PIECE_SIZE + offset_map_y,
                 SNAKE_PIECE_SIZE,
                 SNAKE_PIECE_SIZE, 1)
    display.rect(offset_map_x - 2, 0, SNAKE_PIECE_SIZE * MAP_SIZE + 4, SNAKE_PIECE_SIZE * MAP_SIZE + 4, 1)
    for part in snake[:snake_length]:
        display.fill_rect(part[0] * SNAKE_PIECE_SIZE + offset_map_x, part[1] * SNAKE_PIECE_SIZE + offset_map_y,
                          SNAKE_PIECE_SIZE, SNAKE_PIECE_SIZE, 1)


def drawScore():
    display.text(f"PTS:{snake_length - STARTING_SNAKE_SIZE}", 2, 2, 1)


def drawPressToStart():
    display.text("PRESS", 2, 10, 1)
    display.text("BUTTON", 2, 20, 1)
    display.text("TO", 2, 30, 1)
    display.text("START", 2, 40, 1)
    display.text("GAME!", 2, 50, 1)


def drawGameover():
    display.fill(0)
    display.text("GAME", 2, 30, 1)
    display.text("OVER", 2, 40, 1)


def drawWin():
    display.text("YOU", 2, 30, 1)
    display.text("WON", 2, 40, 1)


# Run the setup function
setup()

# Start the game loop
loop()
