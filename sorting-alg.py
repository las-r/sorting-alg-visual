import pygame
import random

# sorting alg visualizer
# v2.0
# made by las-r on github

# init
pygame.init()
clk = pygame.time.Clock()
font = pygame.font.Font(None, 16)

# settings
WIDTH, HEIGHT = 600, 600
MAXOPC = 480

# colors
BGCOL = (0, 0, 0)
ARRCOL = (255, 255, 255)
TXCOL = (0, 255, 255)

# helpers
def updateDisp(c = False):
    global opc
    if c: 
        opc += 1
    scr.fill(BGCOL)
    for i, a in enumerate(arr):
        pygame.draw.rect(scr, ARRCOL, pygame.Rect(i * iw, HEIGHT - a * ih, iw, a * ih))
    scr.blit(font.render(f"Array length: {arrlen}", True, TXCOL), (5, 5))
    scr.blit(font.render(f"Operations per second: {ops}", True, TXCOL), (5, 20))
    scr.blit(font.render(f"Sorting: {sorting}", True, TXCOL), (5, 35))
    scr.blit(font.render(f"Algorithm: {algs[algi]}", True, TXCOL), (5, 50))
    scr.blit(font.render(f"Operations: {opc}", True, TXCOL), (5, 65))
    pygame.display.flip()
    pygame.event.pump()
    clk.tick(ops)

def swap(i, j):
    global opc
    arr[i], arr[j] = arr[j], arr[i]

def isSorted():
    for i in range(1, arrlen):
        if arr[i] < arr[i - 1]:
            return
    return True

def reset():
    global arr, iw, ih
    arr = [i for i in range(1, arrlen + 1)]
    iw, ih = WIDTH // arrlen, HEIGHT // arrlen

# sorting algorithms
def bubble():
    global opc
    while True:
        swapped = False
        for i in range(arrlen - 1):
            if arr[i] > arr[i + 1]:
                swap(i, i + 1)
                swapped = True
                updateDisp(True)
                yield
        if not swapped:
            return

def gnome():
    global opc
    pos = 0
    while pos < len(arr):
        if pos == 0 or arr[pos] >= arr[pos - 1]:
            pos += 1
            opc += 1
        else:
            swap(pos, pos - 1)
            pos -= 1
            updateDisp(True)
            yield

def selection():
    global opc
    for i in range(arrlen):
        jmin = i
        for j in range(i + 1, arrlen):
            if arr[j] < arr[jmin]:
                jmin = j
            opc += 1
        if jmin != i:
            swap(i, jmin)
            updateDisp(True)
            yield

def merge():
    global opc
    def topDownMerge(src, begin, mid, end, dest):
        i = begin
        j = mid
        for k in range(begin, end):
            if i < mid and (j >= end or src[i] <= src[j]):
                dest[k] = src[i]
                i += 1
            else:
                dest[k] = src[j]
                j += 1
            updateDisp(True)
            yield
    def topDownSplitMerge(src, begin, end, dest):
        if end - begin <= 1:
            return
        mid = (begin + end) // 2
        yield from topDownSplitMerge(dest, begin, mid, src)
        yield from topDownSplitMerge(dest, mid, end, src)
        yield from topDownMerge(src, begin, mid, end, dest)
    b = arr.copy()
    yield from topDownSplitMerge(b, 0, arrlen, arr)
    
def comb():
    global opc
    gap = arrlen
    shrink = 1.3
    done = False
    while not done:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            done = True
        elif gap in (9, 10):
            gap = 11
        opc += 1
        i = 0
        while i + gap < arrlen:
            if arr[i] > arr[i + gap]:
                swap(i, i + gap)
                done = False
                updateDisp(True)
                yield
            i += 1

def bogo():
    global opc
    while not isSorted():
        random.shuffle(arr)
        updateDisp(True)
        yield

def bozo():
    global opc
    while not isSorted():
        swap(random.randint(0, arrlen - 1), random.randint(0, arrlen - 1))
        updateDisp(True)
        yield

# sorting algorithm dictionary
algs = ["Bubble", "Gnome", "Selection", "Merge", "Comb", "Bogo", "Bozo"]
algfs = [bubble, gnome, selection, merge, comb, bogo, bozo]

# display
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Playground")

# variables
arrlen = 40
iw, ih = WIDTH // arrlen, HEIGHT // arrlen
ops = 60
algi = 0

arr = [i for i in range(1, arrlen + 1)]
sorting = False
cur = None
opc = 0

# main loop
run = True
while run:
    # refresh rate
    clk.tick(ops)
    
    # events
    for e in pygame.event.get():
        # quit event
        if e.type == pygame.QUIT:
            run = False

        # key events
        if e.type == pygame.KEYDOWN:
            # control
            if e.key == pygame.K_r:
                if not sorting:
                    reset()
            if e.key == pygame.K_s:
                if not sorting: 
                    random.shuffle(arr)
            if e.key == pygame.K_SPACE:
                sorting = not sorting
                if sorting:
                    cur = algfs[algi]()
                else:
                    cur = None

            # sorting alg chooser
            if e.key == pygame.K_RIGHT:
                if not sorting:
                    algi = (algi + 1) % len(algs)
                    opc = 0
            if e.key == pygame.K_LEFT:
                if not sorting:
                    algi = (algi - 1) % len(algs)
                    opc = 0

        # scroll event
        elif e.type == pygame.MOUSEWHEEL:
            ops = max(1, min(ops + e.y, MAXOPC))
                
    # key held list
    keys = pygame.key.get_pressed()
    if keys[pygame.K_EQUALS]:
        arrlen += 1
        reset()
    if keys[pygame.K_MINUS]:
        arrlen = max(1, arrlen - 1)
        reset()

    # sorting algorithm
    if sorting:
        try:
            next(cur)
        except StopIteration:
            sorting = False

    # update display
    updateDisp()

# quit
pygame.quit()
