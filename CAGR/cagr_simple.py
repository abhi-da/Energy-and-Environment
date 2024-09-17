import math

def calculate():
    while True:
        p= float(input("Enter the Principle Amount: "))
        r=float(input('Enter the annual interest rate(in %): '))
        t=float(input("enter the number of years for which you want to compound: "))
        n=float(input("number of times you want to compound in a year: "))

        cia= p*(1+(r/100))**t
        cin= p*((1+(r/(100*n)))**(n*t))
        cic= p*(math.exp((r/100)*t))

        print(f"The Annual Compunded Future Value is {cia} ")
        print(f"The n times Compunded Future Value is {cin} ")
        print(f"The Continuous Compunded Future Value is {cic} ")

        again= input('Do you want to calculate again, press Y for yes, N for No: ')
        if again!="Y":
            print('Thanks for using this calculator')
            break

calculate()