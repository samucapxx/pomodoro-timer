#!/usr/bin/env python3
import curses
import time
import subprocess
import signal

FONT = {
    '0': [" #### ", "#    #", "#    #", "#    #", " #### "],
    '1': ["  #   ", " ##   ", "  #   ", "  #   ", " ###  "],
    '2': [" #### ", "     #", "  ### ", " #    ", " #####"],
    '3': [" #### ", "     #", "  ### ", "     #", " #### "],
    '4': [" #  # ", " #  # ", " #### ", "    # ", "    # "],
    '5': [" #####", " #    ", " #### ", "     #", " #### "],
    '6': [" #### ", " #    ", " #### ", " #  # ", " #### "],
    '7': [" #####", "     #", "    # ", "   #  ", "  #   "],
    '8': [" #### ", "#    #", " #### ", "#    #", " #### "],
    '9': [" #### ", "#    #", " #### ", "    # ", " #### "],
    ':': ["      ", "  ##  ", "      ", "  ##  ", "      "],
    ' ': ["      ", "      ", "      ", "      ", "      "]
}

STATES = {
    'WORK': {'time': 25 * 60, 'label': 'WORK', 'color_id': 3},
    'BREAK': {'time': 5 * 60, 'label': 'BREAK', 'color_id': 2},
    'LONG_BREAK': {'time': 15 * 60, 'label': 'LONG BREAK', 'color_id': 4}
}

class PomoClock:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.state = 'WORK'
        self.time_left = STATES[self.state]['time']
        self.running = False
        self.pomo_count = 0
        
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        curses.start_color()
        curses.use_default_colors()
        
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, 3 if curses.COLORS >= 8 else curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)

    def notify(self, title, message):
        try:
            subprocess.run(['notify-send', title, message], check=False)
        except:
            pass

    def draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        
        mins, secs = divmod(self.time_left, 60)
        time_str = f"{mins:02}:{secs:02}"
        
        char_h = 5
        char_w = 6
        total_w = len(time_str) * char_w
        
        start_y = (h - char_h) // 2
        start_x = (w - total_w) // 2
        
        color = curses.color_pair(STATES[self.state]['color_id'])
        
        try:
            if start_y > 0 and start_x > 0:
                for i, char in enumerate(time_str):
                    glyph = FONT.get(char, FONT[' '])
                    for row_idx, line in enumerate(glyph):
                        self.stdscr.addstr(start_y + row_idx, start_x + (i * char_w), line, color)
                
                label = f"[{self.state}]"
                self.stdscr.addstr(start_y + char_h + 1, max(0, (w - len(label)) // 2), label, color)
            
            status = "RUNNING" if self.running else "PAUSED"
            info = f"{status} | Pomo: {self.pomo_count} | Space: Play/Pause | R: Reset | Q: Quit"
            self.stdscr.addstr(h - 1, max(0, (w - len(info)) // 2), info[:w-1], curses.A_DIM)
        except curses.error:
            pass
            
        self.stdscr.refresh()

    def next_state(self):
        if self.state == 'WORK':
            self.pomo_count += 1
            if self.pomo_count % 4 == 0:
                self.state = 'LONG_BREAK'
            else:
                self.state = 'BREAK'
            self.notify("Work Block Done!", f"Time for a {self.state.replace('_', ' ').lower()}")
        else:
            self.state = 'WORK'
            self.notify("Break Over!", "Back to work!")
            
        self.time_left = STATES[self.state]['time']
        self.running = False

    def run(self):
        last_tick = time.time()
        while True:
            self.draw()
            
            try:
                key = self.stdscr.getch()
            except:
                key = -1
                
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord(' '):
                self.running = not self.running
            elif key == ord('r') or key == ord('R'):
                self.state = 'WORK'
                self.time_left = STATES[self.state]['time']
                self.running = False
                self.pomo_count = 0
            
            if self.running:
                now = time.time()
                if now - last_tick >= 1:
                    self.time_left -= 1
                    last_tick = now
                    if self.time_left <= 0:
                        self.next_state()
            else:
                last_tick = time.time()
                
            time.sleep(0.05)

def main():
    def signal_handler(sig, frame):
        exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    curses.wrapper(lambda stdscr: PomoClock(stdscr).run())

if __name__ == "__main__":
    main()
