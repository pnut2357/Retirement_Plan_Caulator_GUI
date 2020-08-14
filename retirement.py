###############################################################################
# FILE: hw4.py
# AUTHOR: Jaehyuk Choi (1215326372)
# CONTACT INFO: jchoi154@asu.edu
#
# COURSE INFO
# EEE591 Fall 2019
# Homework3 09-19-2019 / Time: 9:40am - 10:30am MWF
#
# DESCRIPTION
# The program reads user's prompt into a GUI: 1) Mean Return (%) as an average
# annual return of the investment above inflation, 2) Std Dev Return (%) as a
# measure of the annual volatility of the investment, 3) Yearly Contribution ($)
# as the amount of money that you want to invest, 4) No. of Years of Contribution
# as how long you want to anually invest, 5) No. of Years to Retirement as many
# years later you want to retire, and 6) Annual Spend in Retirementnet as the
# amount of money you will anually spend once the your retirement starts.
#
# After inserting those inputs, as soon as the user clicks the calculation
# button, the program calculates and outputs the average balance in your retire-
# ment bank account out of 10 repeats at the time when you would retire, showing
# 10 plots of the balances as functions of number of years. A User can clicks
# the calculation button multiple times. Then, the plots vary depending on a
# measure of annual volatility of the investment (Std Dev).
###############################################################################
import tkinter as tk
from tkinter import *
import numpy as np

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
# Constant for setting the entire year in the wealthy retirement plan.
# 70 years were set up.
YEAR_NEED = 70

# Constant number of iteration was determined as 10.
ITER = 10

# 6 inputs and 1 output should be displayed in the GUI.
fields = ('Mean Return (%)', 'Std Dev Return (%)', 'Yearly Contribution ($)', 'No. of Years of Contribution', 'No. of Years to Retirement', 'Annual Spend in Retirement ($)', 'Ave. Amount at Retirement ($)' )

# Calculates the balance in your retirement bank account passed by those 6
# parameters (the inputs) in the fields.
def wealth_calc(mean, stdev, num_yr_Con, num_yr_Ret, yr_Con, yr_Spend, num_iter):

    num_year = np.linspace(0, 70, 70)           # 70 points as years from 0 to 69.
    wealth_history = np.zeros((YEAR_NEED))      # Initializes 0s for wealth values in a vector.
    noise = (stdev / 100) * np.random.randn(YEAR_NEED)  # Noise for annual volatility of the investment
    #print(noise)
    for index in range(1, YEAR_NEED):
        #print(index)
        # Wealth calculation in general over 70 years.
        wealth_history[index] = wealth_history[index - 1] * (1 + mean / 100 + noise[index])

        # Case1: from the beginning to the year of contribution.
        if index < num_yr_Con:
            wealth_history[index] += yr_Con

        # case2 is already counted from the year of contribution to the year
        # to retirement.

        # case3: from the year to retirement to the end of the entire year.
        elif index >= num_yr_Ret:
            wealth_history[index] -= yr_Spend

        # Once the value of wealth_history is lower than zero (running out of
        # the money you had in your retirement account), its value stays zero
        # and breaks the loop.
        if wealth_history[index] < 0:
            wealth_history[index] = 0
            break

    # Collects all positive values of wealth_histroy.
    graph = wealth_history[ wealth_history > 0 ]

    # Matches x points with the size of the graph for plotting.
    x = np.linspace(0, (graph.size), (graph.size))

    # Plots graph from 0 to wealth
    plt.plot(x, graph, label = str(num_iter+1))

    # Returns the balance at the year to retirement so that later in the
    # calculator function, we can store and calculate the mean of them out of
    # 10 repetition.
    return wealth_history[num_yr_Ret]


# Represents the button in the GUI. Calculates the average balance at the
# year to retirement and Plots iteratively 10 times.
def calculator(entries, label):
    # Gets the prompts from the GUI
    r = float ( entries ['Mean Return (%)'].get() )
    std = float ( entries ['Std Dev Return (%)'].get() )
    yr_con = float ( entries ['Yearly Contribution ($)'].get() )
    num_yr_con = int ( entries ['No. of Years of Contribution'].get() )
    num_yr_ret = int ( entries ['No. of Years to Retirement'].get() )
    yr_spend = float ( entries ['Annual Spend in Retirement ($)'].get() )

    # A vector to store all the wealth values at the year to retirement.
    wealth_ret = np.zeros((ITER), float)

    # Plots in one figure.
    plt.figure()
    for idx in range(ITER):         # Iterates 10 times to plot by calling the
                                    # wealth_calc function.
        wealth_ret[idx] = wealth_calc(r, std, num_yr_con, num_yr_ret, yr_con, yr_spend, idx)

    # Calculates the mean of all the wealth values at the year to retirement.
    mean_ret = np.mean(wealth_ret)
    # Converts it as str to display with 2 precisions.
    mean_ret = ("%8.2f" % mean_ret).strip()

    # Displays the mean value in the GUI and prints it to the console.
    label.configure(text="Ave. Amount at Retirement ($): "+ mean_ret)
    #label.configure(mean_ret)

    #entries['Ave. Amount at Retirement ($)'].delete(0, END)
    #entries['Ave. Amount at Retirement ($)'].insert(0, mean_ret)
    print("Ave. Amount at Retirement ($): %f" % float(mean_ret))

    # Displays the plots with its title, x-axis, and y-axis.
    plt.legend()
    plt.title('Wealth Calculation Plot')
    plt.xlabel('Number of Years')
    plt.ylabel('Balance in a Retirement Account')
    plt.show()

    return mean_ret

# Forms and Designs the GUI.
def makeform(root, fields):
    entries = {}                             # Creates an empty dictionary
    for field in fields:                     # For each of the fields to create
        # Separates the Ave. Avmount at Retirement from the rest of the fields
        # to make it a label instead of having an entry.
        if field == 'Ave. Amount at Retirement ($)':
            row = Frame(root)
            wthlab = Label(row, text=field+":",anchor='w')
            row.pack(side=TOP,fill=X, padx=5,pady=5)      # Places it in the GUI.
            wthlab.pack(side=LEFT, fill=X)
        else:
            row = Frame(root)                     # get the row and create the label
            lab = Label(row, width=22, text=field+": ", anchor='w')

            ent = Entry(row)                      # Creates the entry and init to 0.
            ent.insert(0,"0")

            row.pack(side=TOP, fill=X, padx=5, pady=5)   # Places it in the GUI.
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)

            entries[field] = ent                  # Adds those fields to the dictionary.

    return entries, wthlab


# Start the main program.
root = Tk()                                        # Creates a GUI.
ents, wlab  = makeform(root, fields)               # Makes the fields.

# Adds Calculation button.
b1 = Button( root, text='Calculation', command = (lambda e = ents, l = wlab: calculator(e,l)) )
b1.pack(side=LEFT, padx=5, pady=5)

# Adds Quit button.
b2 = Button(root, text='Quit', command=root.destroy)
b2.pack(side=LEFT, padx=5, pady=5)

root.mainloop()                              # Terminates the program.
