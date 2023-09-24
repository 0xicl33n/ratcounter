import board
import digitalio
from time import sleep
import lib.TM1637 as tm
import gc
import os
from adafruit_debouncer import Debouncer

# buttons
INPLAY_UP_IN = digitalio.DigitalInOut(board.GP16)
INPLAY_UP_IN.direction = digitalio.Direction.INPUT
INPLAY_UP_IN.pull = digitalio.Pull.UP
INPLAY_UP = Debouncer(INPLAY_UP_IN)

INPLAY_DOWN_IN = digitalio.DigitalInOut(board.GP17)
INPLAY_DOWN_IN.direction = digitalio.Direction.INPUT
INPLAY_DOWN_IN.pull = digitalio.Pull.UP
INPLAY_DOWN = Debouncer(INPLAY_DOWN_IN)

RESET_SCREENS_IN = digitalio.DigitalInOut(board.GP18)
RESET_SCREENS_IN.direction = digitalio.Direction.INPUT
RESET_SCREENS_IN.pull = digitalio.Pull.UP
RESET_SCREENS = Debouncer(RESET_SCREENS_IN)

ADD_RATS_IN = digitalio.DigitalInOut(board.GP19)
ADD_RATS_IN.direction = digitalio.Direction.INPUT
ADD_RATS_IN.pull = digitalio.Pull.UP
ADD_RATS = Debouncer(ADD_RATS_IN)

TOKENS_UP_IN = digitalio.DigitalInOut(board.GP20)
TOKENS_UP_IN.direction = digitalio.Direction.INPUT
TOKENS_UP_IN.pull = digitalio.Pull.UP
TOKENS_UP = Debouncer(TOKENS_UP_IN)

TOKENS_DOWN_IN = digitalio.DigitalInOut(board.GP21)
TOKENS_DOWN_IN.direction = digitalio.Direction.INPUT
TOKENS_DOWN_IN.pull = digitalio.Pull.UP
TOKENS_DOWN = Debouncer(TOKENS_DOWN_IN)

# activity led
ACT_LED = digitalio.DigitalInOut(board.GP22)
ACT_LED.direction = digitalio.Direction.OUTPUT

# screens
INPLAY_SCREEN = tm.TM1637(board.GP0, board.GP1)
TOKEN_SCREEN = tm.TM1637(board.GP14, board.GP15)

# global counts
INPLAY_COUNT = 0
TOKEN_COUNT = 0

# manage global counts
def inplay_up():
    global INPLAY_COUNT
    INPLAY_COUNT +=1

def inplay_down():
    global INPLAY_COUNT
    INPLAY_COUNT -=1

def tokens_up():
    global TOKEN_COUNT
    TOKEN_COUNT +=1

def tokens_down():
    global TOKEN_COUNT
    TOKEN_COUNT -=1

# write number to screen
def write_screen(screen,value):
    try:
        screen.number(value)
        return "ok"
    except: 
        print("failed to write to screen?")
    sleep(1)

# self explanitory
def blank_screen(screen):
    try:
        screen.number(0000)
        return "ok"
    except: 
        print("failed to write to screen?")
    sleep(1)

def blink_act_led():
    ACT_LED.value = False
    sleep(.5)
    ACT_LED.value = True

# add inplay to tokens
def inplay2tokens():
    global INPLAY_COUNT
    global TOKEN_COUNT
    TOKEN_COUNT = (INPLAY_COUNT * 2)  - 1
    INPLAY_COUNT = TOKEN_COUNT
    write_screen(TOKEN_SCREEN, TOKEN_COUNT)
    write_screen(INPLAY_SCREEN, TOKEN_COUNT)


blank_screen(INPLAY_SCREEN)
blank_screen(TOKEN_SCREEN)
print(os.uname())
gc.collect()


while True:

    INPLAY_UP.update()
    if INPLAY_UP.fell:
        print("@DEBUG: INPLAY UP")
        blink_act_led()   
        print(f"@DEBUG: INCR INPLAY_COUNT\n {INPLAY_COUNT}")     
        inplay_up()
        print(f"@DEBUG: RESULT INPLAY_COUNT\n {INPLAY_COUNT}")  
        write_screen(INPLAY_SCREEN, INPLAY_COUNT)

    INPLAY_DOWN.update()
    if INPLAY_DOWN.fell:
        print("\n@DEBUG: INPLAY DOWN")
        blink_act_led()
        print(f"@DEBUG: DEINCR INPLAY_COUNT \n {INPLAY_COUNT}")            
        inplay_down()
        print(f"@DEBUG: RESULT INPLAY_COUNT\n {INPLAY_COUNT}")
        write_screen(INPLAY_SCREEN, INPLAY_COUNT)

    TOKENS_UP.update()
    if TOKENS_UP.fell:
        print("\n@DEBUG: TOKEN UP")
        blink_act_led()
        print(f"@DEBUG: INCR TOKEN_COUNT\n {TOKEN_COUNT}") 
        tokens_up()
        inplay_up()
        print(f"@DEBUG: RESULT TOKEN_COUNT\n {TOKEN_COUNT}")
        print(f"@DEBUG: RESULT INPLAY_COUNT\n {INPLAY_COUNT}")  
        write_screen(TOKEN_SCREEN, TOKEN_COUNT)
        write_screen(INPLAY_SCREEN, INPLAY_COUNT)

    TOKENS_DOWN.update()
    if TOKENS_DOWN.fell:
        print("\n@DEBUG: TOKEN DOWN")
        blink_act_led()
        print(f"@DEBUG: DEINCR TOKEN_COUNT\n {TOKEN_COUNT}")
        tokens_down()
        inplay_down()
        print(f"@DEBUG: RESULT TOKEN_COUNT\n {TOKEN_COUNT}") 
        print(f"@DEBUG: RESULT INPLAY_COUNT\n {INPLAY_COUNT}")  
        write_screen(TOKEN_SCREEN, TOKEN_COUNT)
        write_screen(INPLAY_SCREEN, INPLAY_COUNT)
    
    RESET_SCREENS.update()
    if RESET_SCREENS.fell:
        print("\n@DEBUG: RESET")
        blink_act_led()
        blank_screen(INPLAY_SCREEN)
        blank_screen(TOKEN_SCREEN)
        INPLAY_COUNT = 0
        TOKEN_COUNT = 0
    
    ADD_RATS.update()
    if ADD_RATS.fell:
        blink_act_led()
        print(f"\n@DEBUG: RATS2TOKENS:\nINPLAY:\t{INPLAY_COUNT}\nTOKENS:\t{TOKEN_COUNT}")
        inplay2tokens()
        print(f"@DEBUG: RATS2TOKENS:\nINPLAY:\t{INPLAY_COUNT}\nTOKENS:\t{TOKEN_COUNT}")