import tkinter as tk
from tkinter import ttk, messagebox
import data_manager
import utils
import charts

class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pastel Expense Tracker")
        self.geometry("1000x700")
        self.configure(bg=utils.COLORS["bg_start"])
        
        # We can't easily set a gradient for the root background in Tkinter natively 
        # unless we put a Canvas at the back, but standard styling is sufficient if we use pastel bg.
        
        # Create Main Layout
        self.create_header()
        self.create_main_content()
        self.update_dashboard()

    def create_header(self):
        header_frame = tk.Frame(self, bg=utils.COLORS["pink"], height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Pastel Watercolor Tracker", 
                               font=("Helvetica", 20, "bold"), bg=utils.COLORS["pink"], fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Budget info
        self.budget_var = tk.StringVar(value=f"Budget: ${data_manager.get_budget():.2f}")
        budget_label = tk.Label(header_frame, textvariable=self.budget_var,
                                font=("Helvetica", 14, "bold"), bg=utils.COLORS["pink"], fg="white")
        budget_label.pack(side=tk.RIGHT, padx=20, pady=25)
        
        set_budget_btn = tk.Button(header_frame, text="Set Budget", command=self.set_budget,
                                   bg=utils.COLORS["blue"], fg="white", relief=tk.FLAT, 
                                   font=("Helvetica", 10, "bold"))
        set_budget_btn.pack(side=tk.RIGHT, padx=10, pady=25)

    def create_main_content(self):
        content_frame = tk.Frame(self, bg=utils.COLORS["bg_start"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column (Form & List)
        left_col = tk.Frame(content_frame, bg=utils.COLORS["bg_start"], width=300)
        left_col.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(0, 10))
        
        # Right column (Charts)
        self.right_col = tk.Frame(content_frame, bg=utils.COLORS["bg_start"])
        self.right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # --- Add Expense Form ---
        form_frame = tk.LabelFrame(left_col, text="Add Expense", bg=utils.COLORS["bg_start"], 
                                   fg=utils.COLORS["text"], font=("Helvetica", 12, "bold"))
        form_frame.pack(fill=tk.X, pady=(0, 20), ipady=10)
        
        tk.Label(form_frame, text="Description:", bg=utils.COLORS["bg_start"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.desc_entry = tk.Entry(form_frame, relief=tk.FLAT, highlightthickness=1, highlightcolor=utils.COLORS["blue"])
        self.desc_entry.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(form_frame, text="Amount ($):", bg=utils.COLORS["bg_start"]).pack(anchor=tk.W, padx=10)
        self.amount_entry = tk.Entry(form_frame, relief=tk.FLAT, highlightthickness=1, highlightcolor=utils.COLORS["blue"])
        self.amount_entry.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(form_frame, text="Category:", bg=utils.COLORS["bg_start"]).pack(anchor=tk.W, padx=10)
        self.cat_var = tk.StringVar(value="Food")
        cats = list(utils.CATEGORY_COLORS.keys())
        self.cat_menu = ttk.Combobox(form_frame, textvariable=self.cat_var, values=cats, state="readonly")
        self.cat_menu.pack(fill=tk.X, padx=10, pady=5)
        
        add_btn = tk.Button(form_frame, text="Add Expense", command=self.add_expense,
                            bg=utils.COLORS["green"], fg=utils.COLORS["text"], relief=tk.FLAT,
                            font=("Helvetica", 10, "bold"))
        add_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # --- Expense List ---
        list_frame = tk.LabelFrame(left_col, text="Recent Expenses", bg=utils.COLORS["bg_start"], 
                                   fg=utils.COLORS["text"], font=("Helvetica", 12, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Custom Treeview styling for pastel colors
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", fieldbackground="white", 
                        foreground=utils.COLORS["text"], rowheight=30)
        style.map("Treeview", background=[("selected", utils.COLORS["blue"])])
        
        columns = ("desc", "amount", "cat", "date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("desc", text="Description")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("cat", text="Category")
        self.tree.heading("date", text="Date")
        
        self.tree.column("desc", width=100)
        self.tree.column("amount", width=60)
        self.tree.column("cat", width=80)
        self.tree.column("date", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<Delete>", self.delete_expense)
        
        delete_btn = tk.Button(list_frame, text="Delete Selected (Press Del)", command=self.delete_expense,
                            bg=utils.COLORS["pink"], fg=utils.COLORS["text"], relief=tk.FLAT)
        delete_btn.pack(fill=tk.X, padx=10, pady=(0, 10))

    def add_expense(self):
        desc = self.desc_entry.get()
        amount = self.amount_entry.get()
        cat = self.cat_var.get()
        
        if not desc or not amount:
            messagebox.showerror("Error", "Description and amount are required.")
            return
            
        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
            
        data_manager.add_expense(desc, amount_float, cat)
        
        # Reset form
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        self.update_dashboard()

    def delete_expense(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get expense ID (stored in item tags or we can fetch by index)
        # We stored the ID as the iid in the treeview
        item_id = selected[0]
        data_manager.delete_expense(int(item_id))
        self.update_dashboard()

    def set_budget(self):
        # Simple dialog
        top = tk.Toplevel(self)
        top.title("Set Budget")
        top.geometry("300x150")
        top.configure(bg=utils.COLORS["bg_start"])
        
        tk.Label(top, text="Enter New Monthly Budget:", bg=utils.COLORS["bg_start"]).pack(pady=(20, 5))
        budget_entry = tk.Entry(top)
        budget_entry.pack(pady=5)
        budget_entry.insert(0, str(data_manager.get_budget()))
        
        def save():
            try:
                amt = float(budget_entry.get())
                data_manager.set_budget(amt)
                self.budget_var.set(f"Budget: ${amt:.2f}")
                self.update_dashboard()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")
                
        tk.Button(top, text="Save", command=save, bg=utils.COLORS["blue"], fg="white", relief=tk.FLAT).pack(pady=10)

    def update_dashboard(self):
        # Update List
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        expenses = data_manager.get_expenses()
        # Sort descending by date/id
        expenses.sort(key=lambda x: x["id"], reverse=True)
        
        total = 0
        for exp in expenses:
            total += exp["amount"]
            self.tree.insert("", tk.END, iid=exp["id"], 
                             values=(exp["desc"], f"${exp['amount']:.2f}", exp["category"], exp["date"]))
                             
        # Update budget label to show progress
        budget = data_manager.get_budget()
        self.budget_var.set(f"Budget: ${budget:.2f} | Spent: ${total:.2f}")

        # Refresh Charts
        for widget in self.right_col.winfo_children():
            widget.destroy()
            
        # Bar Chart Frame
        bar_frame = tk.Frame(self.right_col, bg=utils.COLORS["bg_start"])
        bar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        cat_totals = data_manager.get_category_totals()
        bar_canvas = charts.create_bar_chart(bar_frame, cat_totals)
        bar_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Line Chart Frame
        line_frame = tk.Frame(self.right_col, bg=utils.COLORS["bg_start"])
        line_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 0))
        
        line_canvas = charts.create_line_chart(line_frame, expenses)
        line_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
