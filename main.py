import cli
import app

def main():
    # 1. Show the pastel watercolor-themed ASCII art header and CLI messages
    cli.show_startup_message()
    
    # 2. Launch the Tkinter Main Interface
    expense_app = app.ExpenseApp()
    expense_app.mainloop()

if __name__ == "__main__":
    main()
