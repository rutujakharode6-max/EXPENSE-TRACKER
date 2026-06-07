import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Pastel Palette
COLORS = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#E6B3FF", "#FFDFBA"]
TEXT_COLOR = "#7A7A7A"
BG_COLOR = "#FFF0F5" # Or transparent

def create_bar_chart(parent_frame, category_totals):
    fig = Figure(figsize=(5, 4), dpi=100, facecolor=BG_COLOR)
    ax = fig.add_subplot(111)
    
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    
    if not categories:
        ax.text(0.5, 0.5, "No Expense Data", ha='center', va='center', color=TEXT_COLOR)
        ax.axis('off')
    else:
        # Match colors to categories if possible, or just cycle
        colors = COLORS[:len(categories)]
        
        bars = ax.bar(categories, amounts, color=colors, edgecolor="white", linewidth=1.5)
        
        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(TEXT_COLOR)
        ax.spines['bottom'].set_color(TEXT_COLOR)
        ax.tick_params(axis='x', colors=TEXT_COLOR, rotation=45)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        ax.set_facecolor(BG_COLOR)
        
        # Title
        ax.set_title("Category Breakdown", color=TEXT_COLOR, pad=15)
        
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    return canvas

def create_line_chart(parent_frame, expenses):
    fig = Figure(figsize=(5, 4), dpi=100, facecolor=BG_COLOR)
    ax = fig.add_subplot(111)
    
    if not expenses:
        ax.text(0.5, 0.5, "No Expense Data", ha='center', va='center', color=TEXT_COLOR)
        ax.axis('off')
    else:
        # Group by date
        date_totals = {}
        for exp in expenses:
            date_totals[exp['date']] = date_totals.get(exp['date'], 0) + exp['amount']
            
        sorted_dates = sorted(list(date_totals.keys()))
        amounts = [date_totals[d] for d in sorted_dates]
        
        # Plot line
        ax.plot(sorted_dates, amounts, color="#B0E0E6", marker='o', markerfacecolor="#FFB6C1", 
                markeredgecolor="white", linewidth=2.5, markersize=8)
        
        # Add gradient fill (simulated by filling to 0)
        ax.fill_between(sorted_dates, amounts, 0, color="#B0E0E6", alpha=0.3)
        
        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(TEXT_COLOR)
        ax.spines['bottom'].set_color(TEXT_COLOR)
        ax.tick_params(axis='x', colors=TEXT_COLOR, rotation=45)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        ax.set_facecolor(BG_COLOR)
        
        ax.set_title("Expense Trends", color=TEXT_COLOR, pad=15)
        
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    return canvas
