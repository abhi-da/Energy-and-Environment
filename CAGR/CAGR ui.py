import math
import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        # Read input values
        P = float(entry_principal.get())
        r = float(entry_rate.get()) / 100
        t = float(entry_time.get())

        # Annual Compounding (n = 1)
        n_annual = 1
        A_annual = P * (1 + r/n_annual) ** (n_annual * t)
        result_annual.set(f"The amount after {t} years with annual compounding (n = 1) is: {A_annual:.2f}")

        # User-Defined Compounding
        n_user_defined = int(entry_n.get())
        A_user_defined = P * (1 + r/n_user_defined) ** (n_user_defined * t)
        result_user_defined.set(f"The amount after {t} years with compounding {n_user_defined} times per year is: {A_user_defined:.2f}")

        # Continuous Compounding
        A_continuous = P * math.exp(r * t)
        result_continuous.set(f"The amount after {t} years with continuous compounding is: {A_continuous:.2f}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except OverflowError:
        messagebox.showerror("Overflow Error", "The result is too large to compute. Try smaller values.")

def clear_entries():
    entry_principal.delete(0, tk.END)
    entry_rate.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    entry_n.delete(0, tk.END)
    result_annual.set("")
    result_user_defined.set("")
    result_continuous.set("")

# Create the main window
root = tk.Tk()
root.title("Compound Interest Calculator")

# Principal
tk.Label(root, text="Principal Amount (P):").grid(row=0, column=0, padx=10, pady=10)
entry_principal = tk.Entry(root)
entry_principal.grid(row=0, column=1, padx=10, pady=10)

# Rate
tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=10, pady=10)
entry_rate = tk.Entry(root)
entry_rate.grid(row=1, column=1, padx=10, pady=10)

# Time
tk.Label(root, text="Time in Years (t):").grid(row=2, column=0, padx=10, pady=10)
entry_time = tk.Entry(root)
entry_time.grid(row=2, column=1, padx=10, pady=10)

# Compounding Periods per Year
tk.Label(root, text="Compounding Periods per Year (n):").grid(row=3, column=0, padx=10, pady=10)
entry_n = tk.Entry(root)
entry_n.grid(row=3, column=1, padx=10, pady=10)

# Results
result_annual = tk.StringVar()
result_user_defined = tk.StringVar()
result_continuous = tk.StringVar()

tk.Label(root, textvariable=result_annual).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
tk.Label(root, textvariable=result_user_defined).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
tk.Label(root, textvariable=result_continuous).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Buttons
tk.Button(root, text="Calculate", command=calculate).grid(row=7, column=0, padx=10, pady=20)
tk.Button(root, text="Clear", command=clear_entries).grid(row=7, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
