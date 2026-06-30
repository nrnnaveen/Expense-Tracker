import psycopg2

#Connect Your Postgres DB

conn = psycopg2.connect(
        host="YOUR_HOST",
        port=1234,                                            #replace it with Correct Port
        database="YOUR_DB_NAME",
        user="YOUR_USER_NAME",
        password="YOUR_PASSWORD",
        sslmode="require" #ssl mode is optional, i used it because i use an cloud DB(aiven) credentials
    )

# Create Table Expenses

cursor=conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS expenses(
    id SERIAL PRIMARY KEY,
    Name VARCHAR(20),
    Catagory VARCHAR(50),
    Amount INT
    )"""
)

choice=-1
while choice!=0 :
    print(
        """
      ===================
        EXPENSE TRACKER
      ===================
      0.Exit
      1.Add Expenses
      2.View Expense
      3.Monthly Summary
      4.Delete Expenses

"""
    )

    choice=int(input("Enter Your Preferance:"))

    #ADD EXPENSES
    if choice == 1:
        name=input("Enter Expense Name:")
        amount=int(input("Enter Expense Amount:"))
        print(
            """
        1.Travel
        2.Entertainment
        3.Shopping
        4.Rent

"""
        )
        typ=int(input("Choose Expense Type:"))
        catagories={
            1:"Travel",
            2:"Entertainment",
            3:"Shopping",
            4:"Rent"
        }
        if catagories:
            catagory=catagories.get(typ)
            cursor.execute(
                """INSERT INTO expenses (Name,Catagory,Amount) VALUES (%s,%s,%s)""",
                (name,catagory,amount)
            )
            conn.commit()
            print()
            print("Expense",name," Added Successfully")
        else:
            print("Invalid Choice Try Again")

    #VIEW EXPENSES
        
    elif choice == 2:
        print("All Expenses")
        print("""

id || Name || Catagory || Amount""")
        cursor.execute("SELECT * FROM expenses")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
            print()

    #MONTHLY SUMMARY

    elif choice ==3:
        print("Monthly Summary")
        print("""
Catagory || Amount """)
        cursor.execute("SELECT Catagory,SUM(Amount) FROM expenses GROUP BY Catagory")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
            print()
        cursor.execute("SELECT SUM(Amount) FROM expenses")
        row=cursor.fetchone()
        print("Total Expenses:",row)

    #DELETE EXPENSES

    elif choice==4:
        print("""

id || Name || Catagory || Amount""")
        print()
        cursor.execute("SELECT * FROM expenses")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
            print()
        iden=int(input("Enter Expense Id To Delete It :"))
        cursor.execute("DELETE FROM expenses WHERE id =%s ",(iden,))
        if cursor.rowcount >0 :
            conn.commit()
            print("Expense  No :",iden," Deleted SuccessFully ")
        else:
            print("NO Expenses Found With This Id ")

    #EXIT

    elif choice==0:
        print("Bye...")
    else:
        print("Invalid Choice , Try Again !!!")
        
conn.commit()
conn.close()