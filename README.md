# 🎨 Pastel Watercolor Expense Tracker

A visually stunning, traditional Python desktop application built with `Tkinter` and `Matplotlib`. This expense tracker brings a soft, calming pastel watercolor aesthetic to personal finance management, complete with gradient backgrounds, colorful icons, and dynamic charts.

## ✨ Features

- **Aesthetic Desktop UI**: A fully functional Tkinter interface overlaying programmatically generated pastel gradients and rounded containers (bypassing Tkinter's native graphical limitations using the `Pillow` library).
- **Interactive Visualizations**: Embedded `Matplotlib` charts displaying your financial data in soft pastel colors (`#FFB3BA`, `#BAFFC9`, `#BAE1FF`, `#FFFFBA`).
  - **Category Breakdown**: A beautiful Bar Chart categorizing your spending.
  - **Expense Trends**: A Line Graph tracking your daily expenses with a smooth pastel gradient fill.
- **Colorful CLI Startup**: A vibrant watercolor-themed ASCII art header that greets you in the terminal using true-color ANSI escape sequences via `Colorama`.
- **Data Persistence**: Your expenses and customized budget are automatically saved and loaded from a local `expenses.json` file.
- **Budget Tracking**: Instantly compare your total monthly spending against a customizable monthly budget limit.

## 🛠️ Technology Stack

- **Python 3.x**
- **Tkinter**: Standard GUI library for Python.
- **Matplotlib**: For plotting data and displaying charts.
- **Pillow (PIL)**: For generating custom watercolor assets (gradients, rounded rectangles, colored circles).
- **Colorama**: For vibrant, true-color terminal output.

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rutujakharode6-max/EXPENSE-TRACKER.git
   cd EXPENSE-TRACKER
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed, then install the necessary libraries using `pip`:
   ```bash
   pip install matplotlib pillow colorama
   ```

3. **Run the Application:**
   Launch the app from your terminal:
   ```bash
   python main.py
   ```
   *You'll see the colorful ASCII art pop up in your terminal, followed immediately by the graphical Tkinter dashboard!*

## 📁 Project Structure

- `main.py` - The entry point of the application.
- `app.py` - Contains the main `Tkinter` GUI logic and layout.
- `charts.py` - Handles the generation of `Matplotlib` visualizations.
- `cli.py` - Responsible for the `Colorama` terminal header.
- `utils.py` - Utility functions for generating images and colors using `Pillow`.
- `data_manager.py` - Manages JSON data reading, writing, and calculations.
- `expenses.json` - Your local database (created automatically upon first run).