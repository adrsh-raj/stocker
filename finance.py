from tkinter import *
from tkinter import messagebox
from datetime import datetime
from os import get_terminal_size
from colorama import Fore



root = Tk()
root.title(f'{datetime.today()} |    Value Calculator')
root.minsize(800,480)
root.maxsize(800,480)
root.configure(bg='#F3E8AD')


column = get_terminal_size()
column = column[0]
# print(column)

def FvCalculator():
    global list_append
    global sixth_term
    sixth_term = 0
    list_append = []
    for i in range(1,int(future_year_entry.get())+1):
        amount = float(amount_future.get())
        oppertunity_cost = float(opration_future.get())
        oppertunity_cost = oppertunity_cost/100
        formula = amount*((1+ oppertunity_cost)**i)
        list_append.append(formula)
        
        # ----------------

    # print(list_append)
    sixth_term = list_append[len(list_append)-1] * 1.1
    print(Fore.CYAN+str(sixth_term))
    print(Fore.GREEN + "Copy and paste in FC2 amount value")


def FvCalculator_b():
    global list_append_b
    list_append_b = []
    get_amount = amount_future_b.get()
    list_append_b.append(float(get_amount))
    for i in range(1,int(future_year_entry_b.get())+1):
        amount = float(amount_future_b.get())
        oppertunity_cost = float(opration_future_b.get())
        oppertunity_cost = oppertunity_cost/100
        formula = amount*((1+ oppertunity_cost)**i)
        list_append_b.append(formula)

    list_append_b.pop()
    # print(list_append_b)


    print(f'{Fore.CYAN} List of future value is {list_append+list_append_b}')
    print(Fore.CYAN + "-"*column + "\n")



def Nv():
    global new_list
    global sumofvalues
    try:
        percentage = 0.09
        amount_list = []
        new_list = list_append+list_append_b
        d = {}
        for i in range(len(new_list)):
            amount = (new_list)
            formula = amount[i]/((1+ percentage)**(i+1))
            amount_list.append(formula)
            d[(new_list[i])] = amount_list[i]
        print(Fore.CYAN +"{future value : current value }"+ str(d))
        print(Fore.CYAN + "-"*column +"\n")
        pvvaluelist = list(d.values())
        sumofvalues = sum(pvvaluelist)
    except:
        print("Couldn't get sufficient value")

      


def TerminalValue():
    global Terminal_VAlue
    fcashFlow = new_list[len(new_list)-1]
    getrate = 0.035
    discountrate = 0.09

    Terminal_VAlue = fcashFlow * (1+ float(getrate))/(discountrate-float(getrate))
    print(Fore.CYAN + "Terminal value is "+str(Terminal_VAlue))


def PVcalculate():
    global formula
    
    formula = Terminal_VAlue/((1+ 0.09)**len(new_list))
    messagebox.showinfo(title="Possible result", message=f"Present Value is {str(formula)}")



def netCash():
    global netcah
    global totalShare
    netcah = net_cash.get()
    totalShare =  shares.get()



def fairValue():

    valuation = formula + sumofvalues + float(netcah)
    FairValue = valuation/float(totalShare)

    possibleValuemin = FairValue*(1-0.1)
    possibleValuemax = FairValue*(1+0.1)
    messagebox.showinfo(title="Possible valuation", message=f"Fair Value is between {possibleValuemin} and {possibleValuemax}")


developer_label = Label(root, text='by source(github = adrsh-raj)',bg='#F3E8AD', fg='red', font=("Courier", 8))
developer_label.place(relx=0.01, rely=0.98)

amount_label = Label(root, text="*Amount value(CF)", bg='#F3E8AD', fg="red")
amount_label.place(relx=0.45, rely=0.05)

operation_label = Label(root, text="*Operational percentage", bg='#F3E8AD', fg="red")
operation_label.place(relx=0.65, rely=0.05)

_year = Label(root, text="*Year", bg="#F3E8AD", fg="red")
_year.place(relx=0.355, rely=0.05)

# future 1st
future_Value = Label(root, text="Future Cash Calculator: ", bg='#F3E8AD', font="7", fg='#000000')
future_Value.place(relx=0.1, rely=0.1)

amount_future = Entry(root, width=15,bg="#F3E8AD",fg='#000000')
amount_future.place(relx=0.45, rely=0.1)

opration_future = Entry(root, width=15,bg="#F3E8AD",fg='#000000')
opration_future.place(relx=0.65, rely=0.1)

future_button = Button(root, text="Get value",bg="#F3E8AD", command=FvCalculator, fg='#000000')
future_button.place(relx=0.89, rely=0.09)

future_year_entry = Entry(root, width=5,bg="#F3E8AD",fg='#000000')
future_year_entry.place(relx=0.36, rely=0.1)


# future 2nd

future_Value_b = Label(root, text="Future Cash Calculator 2: ", bg='#F3E8AD', font="7", fg='#000000')
future_Value_b.place(relx=0.1, rely=0.2)

amount_future_b = Entry(root, width=15,bg="#F3E8AD",fg='#000000')
# amount_future_b.insert(INSERT, sixth_term)
amount_future_b.place(relx=0.45, rely=0.2)

opration_future_b = Entry(root, width=15,bg="#F3E8AD",fg='#000000',)
opration_future_b.place(relx=0.65, rely=0.2)

future_button_b = Button(root, text="Get value", bg="#F3E8AD", command=FvCalculator_b, fg='#000000')
future_button_b.place(relx=0.89, rely=0.2)

future_year_entry_b = Entry(root, width=5,bg="#F3E8AD",fg='#000000')
future_year_entry_b.place(relx=0.36, rely=0.2)


# npv
net_present_value = Label(root, text="NPV Calculator: ",font="7", bg='#F3E8AD', fg='#000000')
net_present_value.place(relx=0.1, rely=0.33)

net_Button = Button(root, text="submit", bg="#F3E8AD", command=Nv, fg='#000000')
net_Button.place(relx=0.89, rely=0.32)

# Terminal Value
terminal_value = Label(root, text="Terminal  CF: ", bg='#F3E8AD', font="7", fg='#000000')
terminal_value.place(relx=0.1, rely=0.44)

present_button = Button(root, text="submit", bg="#F3E8AD",command=TerminalValue, fg='#000000')
present_button.place(relx=0.89, rely=0.42)

# present
present_Tvalue = Label(root, text="Present T Calculator: ", bg='#F3E8AD', font="7", fg='#000000')
present_Tvalue.place(relx=0.1, rely=0.55)

present_button = Button(root, text="Submit", bg="#F3E8AD",command=PVcalculate, fg='#000000')
present_button.place(relx=0.89, rely=0.55)


# debt
final_value = Label(root, text="Net cash eq | No. of shares:  ", bg='#F3E8AD', font="7", fg='#000000')
final_value.place(relx=0.1, rely=0.66)

net_cash = Entry(root,width=15,bg='#F3E8AD', fg='#000000')
net_cash.insert(END, "Net cash(in cr.)")
net_cash.place(relx=  0.4, rely=0.66)

shares = Entry(root,width=15,bg='#F3E8AD', fg='#000000')
shares.insert(END, "shares(in cr.)")
shares.place(relx=  0.6, rely=0.66)

final_button = Button(root, text="submit", bg="#F3E8AD",command=netCash, fg='#000000')
final_button.place(relx=0.89, rely=0.66)


# Net Value
final_value = Label(root, text="Get Fair Value: ", bg='#F3E8AD', font="7", fg='#000000')
final_value.place(relx=0.1, rely=0.76)

final_button = Button(root, text="Get value", bg="#F3E8AD",command=fairValue, fg='#000000')
final_button.place(relx=0.89, rely=0.76)


def exit_btn():root.destroy()

exit_Button = Button(root, text="Exit", bg='#F3E8AD', command=exit_btn, width=30, font=('Bold '), fg='#000000')
exit_Button.place(rely=0.9, relx=0.55)



def reset_button():
    amount_future.delete(0,END)
    opration_future.delete(0,END)
    future_year_entry.delete(0,END)
    future_year_entry_b.delete(0,END)
    amount_future_b.delete(0,END)
    opration_future_b.delete(0,END)
    net_cash.delete(0,END)
    shares.delete(0,END)

reset_Button = Button(root, text="Reset", bg='#F3E8AD', command=reset_button, width=30, font=('Bold '), fg='#000000')
reset_Button.place(rely=0.9, relx=0.1)

root.mainloop()

