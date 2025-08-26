from gui.interface import CubeSolverInterface
import tkinter as tk

def main():
    root = tk.Tk()
    app = CubeSolverInterface(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

if __name__ == "__main__":
    main()