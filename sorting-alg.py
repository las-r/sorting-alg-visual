import pygame
import random
import time

# initialize
pygame.init()
font = pygame.font.Font(None, 20)

# settings
WIDTH, HEIGHT = 500, 500
BARWIDTH = 5
BACKGROUNDCOLOR = (0, 0, 0)
TEXTCOLOR = (0, 255, 255)
BARSCOLORMAIN = (255, 255, 255)
BARSCOLORSORTED = (0, 255, 0)
SORTSPEED = 0.01

# update / draw bars on screen
def drawBars(bars):
    screen.fill(BACKGROUNDCOLOR)
    max_height = max(bars) if bars else 1
    
    # renders bars
    for i, value in enumerate(bars):
        bar_height = (value / max_height) * HEIGHT
        x = i * BARWIDTH
        pygame.draw.rect(screen, barsColor, (x, HEIGHT - bar_height, BARWIDTH, bar_height))
        
    # render step count
    stepText = font.render(str(steps), True, TEXTCOLOR)
    screen.blit(stepText, (10, 10))
    
    # update display
    pygame.display.flip()

# quicksort algorithm
def quicksort(arr, low, high):
    if low < high:
        pivot = partition(arr, low, high)
        quicksort(arr, low, pivot - 1)
        quicksort(arr, pivot + 1, high)

# partition algorithm
def partition(arr, low, high):
    global steps

    # select pivot as median of first, middle, and last
    mid = (low + high) // 2
    first = arr[low]
    middle = arr[mid]
    last = arr[high]

    # find median
    pivotVal = sorted([first, middle, last])[1]

    # swap pivot with last element
    if pivotVal == first:
        arr[low], arr[high] = arr[high], arr[low]
    elif pivotVal == middle:
        arr[mid], arr[high] = arr[high], arr[mid]
    pivot = arr[high]

    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            drawBars(bars)
            time.sleep(SORTSPEED)
            steps += 1
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    drawBars(bars)
    time.sleep(SORTSPEED)
    steps += 1
    return i + 1

# setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sorting algorithm visualizer")

# initialize list of bars
bars = [i + 1 for i in range(WIDTH // BARWIDTH)]
random.shuffle(bars)

# sorting variables
steps = 0
paused = True
running = True
barsSorted = False
barsColor = BARSCOLORMAIN

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # toggle pause
                paused = not paused
            if event.key == pygame.K_r:
                # reset
                random.shuffle(bars)
                paused = True
                barsSorted = False
                barsColor = (255, 255, 255)
                steps = 0
    
    # update bars
    drawBars(bars)

    # perform sorting when not paused
    if not paused and not barsSorted:
        quicksort(bars, 0, len(bars) - 1)
        barsSorted = True
    
    # change bars color when sorted
    if barsSorted:
        barsColor = BARSCOLORSORTED

pygame.quit()
