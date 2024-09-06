import tkinter as tk
from tkinter import messagebox
import math

# Define calculation functions
def calculate_future_value(principal, cagr, years, n=1):
    """Calculate future value with n compounding periods per year."""
    return principal * (1 + cagr / n) ** (n * years)

def calculate_principal(future_value, cagr, years, n=1):
    """Calculate principal when moving backwards in time with n compounding periods per year."""
    return future_value / (1 + cagr / n) ** (n * years)

def calculate_continuous_future_value(principal, cagr, years):
    """Calculate future value using continuous compounding."""
    return principal * math.exp(cagr * years)

def calculate_continuous_principal(future_value, cagr, years):
    """Calculate principal using continuous compounding when moving backwards in time."""
    return future_value / math.exp(cagr * years)

def calculate_emissions_intensity(co2_emissions, electricity_output):
    """Calculate CO₂ emissions intensity of electricity."""
    return co2_emissions / electricity_output

def calculate_interest_rate(initial_intensity, final_intensity, years, method='annual', n=1):
    """Calculate interest rate for CO₂ emissions intensity."""
    if method == 'annual':
        return (final_intensity / initial_intensity) ** (1 / years) - 1
    elif method == 'compound':
        return n * ((final_intensity / initial_intensity) ** (1 / (n * years)) - 1)
    elif method == 'continuous':
        return math.log(final_intensity / initial_intensity) / years
    else:
        raise ValueError("Invalid method")

# Define the function for the button click
def calculate_results():
    try:
        # Get inputs from user
        initial_electricity_output = float(entry_initial_electricity_output.get())
        initial_year_electricity = int(entry_initial_year_electricity.get())
        cagr_electricity = float(entry_cagr_electricity.get())
        
        initial_co2_emissions = float(entry_initial_co2_emissions.get())
        initial_year_co2 = int(entry_initial_year_co2.get())
        cagr_co2 = float(entry_cagr_co2.get())
        
        target_year = int(entry_target_year.get())
        
        # Handle compounding frequency input
        compounding_frequency_str = entry_compounding_frequency.get()
        if compounding_frequency_str:
            compounding_frequency = int(compounding_frequency_str)
            if compounding_frequency <= 0:
                raise ValueError("Compounding frequency must be a positive integer.")
        else:
            compounding_frequency = 1  # Default to annual compounding
        
        # Calculate the number of years between initial and target year
        years_electricity = target_year - initial_year_electricity
        years_co2 = target_year - initial_year_co2
        
        # Calculate future values or principal amounts
        if years_electricity >= 0:
            final_electricity_output_annual = calculate_future_value(initial_electricity_output, cagr_electricity, years_electricity, 1)
            final_electricity_output_user_defined = calculate_future_value(initial_electricity_output, cagr_electricity, years_electricity, compounding_frequency)
            final_electricity_output_continuous = calculate_continuous_future_value(initial_electricity_output, cagr_electricity, years_electricity)
        else:
            final_electricity_output_annual = calculate_principal(initial_electricity_output, cagr_electricity, abs(years_electricity), 1)
            final_electricity_output_user_defined = calculate_principal(initial_electricity_output, cagr_electricity, abs(years_electricity), compounding_frequency)
            final_electricity_output_continuous = calculate_continuous_principal(initial_electricity_output, cagr_electricity, abs(years_electricity))
        
        if years_co2 >= 0:
            final_co2_emissions_annual = calculate_future_value(initial_co2_emissions, cagr_co2, years_co2, 1)
            final_co2_emissions_user_defined = calculate_future_value(initial_co2_emissions, cagr_co2, years_co2, compounding_frequency)
            final_co2_emissions_continuous = calculate_continuous_future_value(initial_co2_emissions, cagr_co2, years_co2)
        else:
            final_co2_emissions_annual = calculate_principal(initial_co2_emissions, cagr_co2, abs(years_co2), 1)
            final_co2_emissions_user_defined = calculate_principal(initial_co2_emissions, cagr_co2, abs(years_co2), compounding_frequency)
            final_co2_emissions_continuous = calculate_continuous_principal(initial_co2_emissions, cagr_co2, abs(years_co2))
        
        # Calculate initial and final CO2 emissions intensity
        initial_intensity = calculate_emissions_intensity(initial_co2_emissions, initial_electricity_output)
        final_intensity_annual = calculate_emissions_intensity(final_co2_emissions_annual, final_electricity_output_annual)
        final_intensity_user_defined = calculate_emissions_intensity(final_co2_emissions_user_defined, final_electricity_output_user_defined)
        final_intensity_continuous = calculate_emissions_intensity(final_co2_emissions_continuous, final_electricity_output_continuous)
        
        # Calculate the interest rates based on emissions intensity
        number_of_years = abs(target_year - initial_year_electricity)
        annual_interest_rate = calculate_interest_rate(initial_intensity, final_intensity_annual, number_of_years, method='annual')
        compound_interest_rate = calculate_interest_rate(initial_intensity, final_intensity_user_defined, number_of_years, method='compound', n=compounding_frequency)
        continuous_interest_rate = calculate_interest_rate(initial_intensity, final_intensity_continuous, number_of_years, method='continuous')
        
        # Display results
        result_text.set(f"CO2 emissions intensity for the initial year: {initial_intensity:.4f}\n"
                        f"CO2 emissions intensity for the target year (Annual Compounding): {final_intensity_annual:.4f}\n"
                        f"CO2 emissions intensity for the target year ({compounding_frequency} times per year): {final_intensity_user_defined:.4f}\n"
                        f"CO2 emissions intensity for the target year (Continuous Compounding): {final_intensity_continuous:.4f}\n\n"
                        f"Interest Rate (Annual Compounding): {annual_interest_rate:.4f}\n"
                        f"Interest Rate ({compounding_frequency} times per year): {compound_interest_rate:.4f}\n"
                        f"Interest Rate (Continuous Compounding): {continuous_interest_rate:.4f}")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("CO2 Emissions Intensity Calculator")

# Create input fields and labels
tk.Label(root, text="Initial Electricity Output (in thousands):").grid(row=0, column=0)
entry_initial_electricity_output = tk.Entry(root)
entry_initial_electricity_output.grid(row=0, column=1)

tk.Label(root, text="Initial Year for Electricity Output:").grid(row=1, column=0)
entry_initial_year_electricity = tk.Entry(root)
entry_initial_year_electricity.grid(row=1, column=1)

tk.Label(root, text="CAGR for Electricity Output (as a decimal):").grid(row=2, column=0)
entry_cagr_electricity = tk.Entry(root)
entry_cagr_electricity.grid(row=2, column=1)

tk.Label(root, text="Initial CO2 Emissions (in gigatonnes):").grid(row=3, column=0)
entry_initial_co2_emissions = tk.Entry(root)
entry_initial_co2_emissions.grid(row=3, column=1)

tk.Label(root, text="Initial Year for CO2 Emissions:").grid(row=4, column=0)
entry_initial_year_co2 = tk.Entry(root)
entry_initial_year_co2.grid(row=4, column=1)

tk.Label(root, text="CAGR for CO2 Emissions (as a decimal):").grid(row=5, column=0)
entry_cagr_co2 = tk.Entry(root)
entry_cagr_co2.grid(row=5, column=1)

tk.Label(root, text="Target Year:").grid(row=6, column=0)
entry_target_year = tk.Entry(root)
entry_target_year.grid(row=6, column=1)

tk.Label(root, text="Number of times per year to compound (optional):").grid(row=7, column=0)
entry_compounding_frequency = tk.Entry(root)
entry_compounding_frequency.grid(row=7, column=1)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.grid(row=10, column=0, columnspan=2)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_results)
calculate_button.grid(row=8, column=0, columnspan=2)

# Run the application
root.mainloop()
