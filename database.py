import tkinter as tk
from tkinter.messagebox import showinfo, showerror
import pymysql
from tabulate import tabulate

con=None
db=None
def connection():
    def connect():
        global con, db
        host = tx1.get()
        user = tx2.get()
        password = tx3.get()
        db_name = tx4.get()

        try:
            con = pymysql.connect(host=host, user=user, password=password, database=db_name)
            db = con.cursor()
            showinfo("Success", f"Connected to {db_name} database successfully!")
            if con:
                def search():
                    def search_id():
                        inp = tx5.get()
                        db.execute("SELECT * FROM emp_details WHERE Name LIKE %s OR PhNo LIKE %s",
                                   (f"%{inp}%", f"%{inp}%"))
                        results = db.fetchall()

                        tx6.delete("1.0", tk.END)

                        if results:
                            header = [i[0] for i in db.description]
                            output = tabulate(results, headers=header, tablefmt="grid")
                            tx6.insert(tk.END, "\nSearch Results:\n" + output)
                        else:
                            tx6.insert(tk.END, '\nNo results found.')

                    tk.Label(z, text="Search by Name or Phone:", font=("Arial", 12)).place(x=300, y=60)
                    tx5 = tk.Entry(z, font=("Arial", 12))
                    tx5.place(x=300, y=90)
                    tk.Button(z, text="Search", font=("Arial", 12), bg="yellow", fg="black", command=search_id).place(x=480,y=85)


                    from tkinter import Scrollbar
                    tx6 = tk.Text(z, height=10, width=70)
                    tx6.place(x=50, y=150)

                    scrollbar = tk.Scrollbar(z, command=tx6.yview)
                    scrollbar.place(x=620, y=150, height=165)
                    tx6.config(yscrollcommand=scrollbar.set)

                def insert_data():
                    def insert():

                        name=tx7.get()
                        address=tx8.get()
                        ph=tx9.get()
                        email=tx10.get()
                        if not name or not address or not ph or not email:
                            showinfo("Info..!", "Enter all details first")
                        else:
                            try:
                                db.execute("INSERT INTO emp_details (Name, Address, PhNo,Email_id) VALUES (%s, %s, %s,%s)",
                                           ( name, address, ph, email)
                                )
                                con.commit()
                                showinfo("Info..!",f"{name}'s Data is inserted successfully")
                            except Exception as ee:
                                showerror("Error..!",f"insert failed{str(ee)}")
                    def delete():
                        tx7.delete(0,tk.END)
                        tx8.delete(0,tk.END)
                        tx9.delete(0,tk.END)
                        tx10.delete(0,tk.END)
                    win=tk.Tk()
                    win.geometry("700x500")
                    tk.Label(win, text="DATA INSERT..!", font=("times new roman", 20, "bold", "italic")).pack(pady=20)
                    tk.Label(win, text="Name:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=100)
                    tx7 = tk.Entry(win, font=("Arial", 12))
                    tx7.place(x=300, y=100)

                    tk.Label(win, text="Address:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=150)
                    tx8 = tk.Entry(win, font=("Arial", 12))
                    tx8.place(x=300, y=150)

                    tk.Label(win, text="PhNo:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=200)
                    tx9 = tk.Entry(win, font=("Arial", 12))
                    tx9.place(x=300, y=200)

                    tk.Label(win, text="Email_id:", font=("times new roman", 14, "bold", "italic")).place(x=100,y=250)
                    tx10 = tk.Entry(win, font=("Arial", 12))
                    tx10.place(x=300, y=250)
                    tk.Button(win,text="Insert",font=("times new roman", 14, "bold", "italic"),command=insert).place(x=400,y=300)
                    tk.Button(win, text="Clear", font=("times new roman", 14, "bold", "italic"), command=delete).place(x=100, y=300)

                def update_data():
                    def all_field():
                        pass
                    def one_field():
                        def update():
                            def new_update():
                                upf = e1.get()
                                new_up = e2.get()
                                old = tx11.get()
                                db.execute("select * from emp_details")
                                db.fetchall()
                                headers = (i[0] for i in db.description)
                                if upf in headers:
                                    db.execute(f"UPDATE emp_details set {upf}= %s WHERE Name= %s", (new_up, old))
                                    showinfo("Info", f"new update for {old} updated successfully")
                                    con.commit()
                                else:
                                    showerror("Error..!", "Invalid input")
                            tk.Label(win2, text="Updating filed",font=("times new roman", 14, "bold", "italic"),bg="blue",fg="white").place(x=500, y=100)
                            e1 = tk.Entry(win2, font="Arial")
                            e1.place(x=700, y=100)
                            tk.Label(win2, text="New_update",font=("times new roman", 14, "bold", "italic"),bg="blue",fg="white").place(x=500, y=150)
                            e2 = tk.Entry(win2, font="Arial")
                            e2.place(x=700, y=150)
                            tk.Button(win2, text="Update", font=("times new roman", 14, "bold", "italic"),command=new_update).place(x=700, y=300)

                        win2=tk.Tk()
                        win2.title("Update data")
                        tk.Label(win2,text="Emp_Name",font=("times new roman", 14, "bold", "italic"),bg="blue",fg="white").place(x=100,y=100)
                        tx11=tk.Entry(win2,font="Arial")
                        tx11.place(x=200,y=100)
                        tk.Button(win2,text="Update",font=("times new roman", 14, "bold", "italic"),command=update).pack()

                    tk.Button(z,text="One field",font=("times new roman", 14, "bold", "italic"),command=one_field).place(x=250,y=200)
                    tk.Button(z, text="All field", font=("times new roman", 14, "bold", "italic"),command=all_field).place(x=400, y=200)


                def del_data():
                    showinfo("info","delete functionality is not implemented yet")
                z = tk.Tk()
                z.geometry("700x500")
                z.title(f"{db_name}")
                tk.Button(z, text="Search", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
                          activebackground="blue", activeforeground='white', command=search).place(x=100, y=100)
                tk.Button(z, text="Insert data", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
                          activebackground="blue", activeforeground='white', command=insert_data).place(x=100, y=150)
                tk.Button(z, text="Update data", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
                          activebackground="blue", activeforeground='white', command=update_data).place(x=100, y=200)
                tk.Button(z, text="Delete data", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
                          activebackground="blue", activeforeground='white', command=del_data).place(x=100, y=250)
            else:
                showerror("Error", "Connection failed!")



        except Exception as e:
            showerror("Error", f"Connection failed!\n{str(e)}")






    def clear():
        tx1.delete("0",tk.END)
        tx2.delete("0",tk.END)
        tx3.delete("0",tk.END)
        tx4.delete("0",tk.END)
    y = tk.Tk()
    y.geometry("700x500")
    tk.Label(y, text="DATA WORKBENCH..!", font=("times new roman", 20, "bold", "italic")).pack(pady=20)
    tk.Label(y, text="Host Name:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=100)
    tx1 = tk.Entry(y, font=("Arial", 12))
    tx1.place(x=300, y=100)

    tk.Label(y, text="Username:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=150)
    tx2 = tk.Entry(y, font=("Arial", 12))
    tx2.place(x=300, y=150)

    tk.Label(y, text="Password:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=200)
    tx3 = tk.Entry(y, font=("Arial", 12), show='*')
    tx3.place(x=300, y=200)

    tk.Label(y, text="Database Name:", font=("times new roman", 14, "bold", "italic")).place(x=100, y=250)
    tx4 = tk.Entry(y, font=("Arial", 12))
    tx4.place(x=300, y=250)
    tk.Button(y, text="Connect", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
              command=connect).place(x=100, y=320)
    tk.Button(y, text="Clear", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
              command=clear).place(x=420, y=320)









def creation():
    showinfo("Info", "Database creation functionality is not implemented yet.")
# Close connection and app
def on_closing():
    global con
    if con:
        con.close()
    x.destroy()


# GUI setup
x = tk.Tk()
x.geometry("700x500")
x.title("Database Connector")

tk.Label(x, text="DATABASE CONNECTION..!", font=("times new roman", 20, "bold", "italic")).pack(pady=20)
tk.Button(x, text="data base Connection", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
              command=connection).place(x=100, y=320)
tk.Button(x, text="Data base creation", font=("times new roman", 14, "bold", "italic"), bg="blue", fg="white",
              command=creation).place(x=420, y=320)



x.mainloop()
