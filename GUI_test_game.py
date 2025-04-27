import tkinter as tk
import random
from game import ChineseDarkChessEnv

class DarkChessGUI:
    def __init__(self, master, env):
        self.master = master
        self.env = env
        self.state = self.env.reset()
        self.buttons = []
        self.selected = None  
        self.info_label = None
        self.build_ui()

    def build_ui(self):
        self.master.title("Chinese Dark Chess")

        board_frame = tk.Frame(self.master)
        board_frame.pack()

        self.h, self.w = self.env.board_size
        for r in range(self.h):
            row = []
            for c in range(self.w):
                btn = tk.Button(board_frame, text='?', width=6, height=3,
                                command=lambda idx=r*self.w+c: self.click_cell(idx))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

        control_frame = tk.Frame(self.master)
        control_frame.pack()

        self.info_label = tk.Label(control_frame, text="Current player: You (Player 0)")
        self.info_label.pack()

        restart_btn = tk.Button(control_frame, text="Restart", command=self.restart)
        restart_btn.pack()

        self.refresh()

    def click_cell(self, idx):
        if self.env.current_player != 0:
            return  # 只允許你(玩家0)操作

        if self.selected is None:
            self.selected = idx
        else:
            action = (self.selected, idx)
            if action in self.env.get_legal_actions():
                self.play_action(action)
                self.master.after(500, self.computer_move)
            else:
                print("Illegal move!")
            self.selected = None

    def play_action(self, action):
        state, reward, done, info = self.env.step(action)
        self.refresh()
        if done:
            if 'winner' in info:
                if info['winner'] == -1:
                    self.info_label.config(text="Draw!")
                elif info['winner'] == 0:
                    self.info_label.config(text="You win!")
                else:
                    self.info_label.config(text="Computer wins!")
            else:
                self.info_label.config(text="Game Over!")
        else:
            turn = "You (Player 0)" if self.env.current_player == 0 else "Computer (Player 1)"
            self.info_label.config(text=f"Current player: {turn}")

    def computer_move(self):
        if self.env.current_player != 1:
            return
        actions = self.env.get_legal_actions()
        if actions:
            action = random.choice(actions) # Currently random choose action (Cuz it's a test :P)
            self.play_action(action)

    def refresh(self):
        board, revealed = self.state
        for r in range(self.h):
            for c in range(self.w):
                idx = r * self.w + c
                btn = self.buttons[r][c]
                if self.env.revealed[idx] == 1:
                    btn.config(text=self.env.board[idx])
                elif self.env.revealed[idx] == 0:
                    btn.config(text='?')
                else:
                    btn.config(text='.')

    def restart(self):
        self.state = self.env.reset()
        self.selected = None
        self.refresh()
        self.info_label.config(text="Current player: You (Player 0)")

if __name__ == "__main__":
    root = tk.Tk()
    env = ChineseDarkChessEnv()
    app = DarkChessGUI(root, env)
    root.mainloop()
