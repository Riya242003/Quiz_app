import re
import mysql.connector as my
import random
import datetime

db =my.connect(host="localhost",user="root",password="root",database="quiz",auth_plugin='mysql_native_password')
cur = db.cursor()  

user=""

print("#"*15 , " QUIZ APPLICATION " ,"#"*15)

def main():
    while True :
        print("\n")
        print('*'*15, " WELCOME TO LOGIN PAGE " ,'*'*15)
        print('\n')
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        ch=input("Please!, Enter your choice : ")
        print()

        if ch=="1":
            register_new()
        
        elif ch=="2":
            login()

        elif ch=="3":
            exit()

# PASSWORD VALIDATION----------------------

def validate_password(password):

    if len(password) < 8 or len(password) > 20:
        print("Password must be between 8 and 20 characters.")
        return False
    
    if not re.search("[a-z]", password):
        print("Password must contain at least one lowercase letter.")
        return False
        
    if not re.search("[A-Z]", password):
        print("Password must contain at least one uppercase letter.")
        return False
        
    if not re.search("[0-9]", password):
        print("Password must contain at least one numeric digit.")
        return False
    
    if not re.search("[@#$%*^!]", password):
        print("Password must contain at least one special character.")
        return False
        
    return True

# REGISTRATION-------------------------

def register_new():

    print("ENTER YOUR DETAILS BELLOW----------")

    name=input("ENTER YOUR NAME : ").upper()
    
    password=input("ENTER PASSWORD : ")

    if not validate_password(password):
            
            return False
    
    contact=input("ENTER YOUR CONTACT NUMBER : ")
    if len(contact)!=10:
        print("Invalid Contact Number!, Please Try Again")
        contact=input("ENTER YOUR CONTACT NUMBER : ")

    email=input("ENTER EMAILADDRESS : ")


    cur.execute("SELECT * FROM registration_new WHERE name= %s",(name,))
    users = cur.fetchone()


    if users:
        print("Username already exists, please choose another one.")

    cur.execute("INSERT INTO registration_new(name,password,contact,email) values(%s,%s,%s,%s) ",(name,password,contact,email))
    db.commit()
    
    print("REGISTRATION SUCCESSFUL!")

# LOGIN----------------------------

def login():
    global user
    name=input("ENTER YOUR USERNAME : ")
    
    password=input("ENTER YOUR PASSWORD : ")
    user=name
    
    cur.execute("SELECT * FROM registration_new WHERE name = %s AND password = %s", (name, password))
    user1 = cur.fetchone()

    if user1:
        print("LOGIN SUCCESSFUL !")
        inside_login()
        
    else:
        print("INVALID USERNAME OR PASSWORD !")
        return False

# AFTER LOGIN---------------------

def inside_login():
    c=input("Select One Option----------\n\n 1. Attemp Quiz \n 2. View Profile \n 3. Result  \n 4. Exit  \n Enter Your Choice Here : " ) 
    print("\n") 
    if c == '1':
        Attempt_quiz()
    elif c == '2':
        profile()
    elif c == '3':
        Result()
    elif c == '4':
        exit()
    else:
        print("INVALID OPTION! ,SELECT CORRECT OPTION ")
        inside_login()

# PROFILE----------------------

def profile():
    
    global user
    
    print("#"*10," YOUR PROFILE " ,'#'*10)
    print()

    cur.execute("SELECT * FROM registration_new WHERE name = %s",(user,))
    user1 = cur.fetchone()
    print("USER_NAME  : ",user1[0])
    print("CONTACT    : ",user1[2])
    print("EMAIL      : ",user1[3])
   
#  ATTEMPT QUIZ-----------------------

def Attempt_quiz():
    print("#"*10 , " WELCOME IN THE WORLD OF QUIZ, HOPE YOU ENJOY IT ","#"*10)
    print()
    c=input(" SELECT TOPIC ---- \n\n1 1. PYTHON \n 2. DBMS \n 3. OPERATING SYSTEM \n 4. Exit  \n Enter Your Choice Here : " )  
    print()  
    if c == '1':
        python_q()
    elif c == '2':
        dbms_q()
    elif c == '3':
        os_q()
    elif c == '4':
        exit()
    else:
        print("INVALID OPTION! ,SELECT CORRECT OPTION ")
        Attempt_quiz()

# PYTHON QUIZ----------------------
        
def python_q():
    global user
    marks=0
    sub="PYTHON"
    print("!"*20,"WELCOME IN PYTHON QUIZ","!"*20)
    print()
    
    with open('python.txt','r') as file:
        line = file.readlines()
        ques = random.sample(line,10)
        q = 1
    t=datetime.datetime.now()
    for i in range(len(ques)):

        l=ques[i].split(',')
    
        print(f"Que.{q}: {l[0]}")

        print(f" A. {l[1]}\n B. {l[2]}\n C. {l[3]}\n D. {l[4]}")
        ans=input("ENTER YOUR ANSWER (A/B/C/D) : ").upper()
        res = l[5].replace("\n","")
        
        if ans==res:
            print("GREAT! CORRECT ANSWER ")
            marks+=1
        else:
            print("OOPS! INCORRECT ANSWER " ,"CORRECT ANSWER IS : ",res)
        print()
        q+=1  

    print()   
    print("#"*5," RESULT " ,"#"*5)
    correct=marks
    incorrect=10-marks
    print(f"CORRECT ANSWERS - {correct}")
    print(f"INCORRECT ANSWERS - {incorrect}")
    
    cur.execute("INSERT INTO result(name,subject,marks,time) values(%s,%s,%s,%s) ",(user,sub,marks,t))
    db.commit()

# DBMS QUIZ--------------------
    
def dbms_q():
    global user
    marks=0
    sub="DBMS"
    print("!"*20,"WELCOME IN DBMS QUIZ","!"*20)
    print()
    print("user mane is :", user)
    with open('dbms.txt','r') as file:
        line = file.readlines()
        ques = random.sample(line,10)
        
    n=1
    t=datetime.datetime.now()
    for i in range(len(ques)):
        l=ques[i].split(',')
    
        print(f"Que.{n}: {l[0]}")
        print(f" A. {l[1]}\n B. {l[2]}\n C. {l[3]}\n D. {l[4]}")
        ans=input("ENTER YOUR ANSWER (A/B/C/D) : ").upper()
        res = l[5].replace("\n",'')

        if ans==res:
            print("GREAT! CORRECT ANSWER ")
            marks+=1
        else:
            print("OOPS! INCORRECT ANSWER " ,"CORRECT ANSWER IS :",res)
        print()
        n+=1  

    print()   
    print("#"*5," RESULT " ,"#"*5)
    correct=marks
    incorrect=10-marks
    print(f"CORRECT ANSWERS - {correct}")
    print(f"INCORRECT ANSWERS - {incorrect}")
    
    cur.execute("INSERT INTO result(name,subject,marks,time) values(%s,%s,%s,%s) ",(user,sub,marks,t))
    db.commit()
   
# OPERATING SYSTEM QUIZ-----------------

def os_q():
    global score
    marks=0
    sub="OPERATING_SYSTEM"
    print("!"*20,"WELCOME IN OPERATING SYSTEM QUIZ","!"*20)
    print()
    
    with open('os.txt','r') as file:
        line = file.readlines()
        ques = random.sample(line,10)
        
    n=1
    t=datetime.datetime.now()
    for i in range(len(ques)):
        l=ques[i].split(',')
        
        print(f"Que.{n}: {l[0]}")
        print(f" A. {l[1]}\n B. {l[2]}\n C. {l[3]}\n D. {l[4]}")
        ans=input("ENTER YOUR ANSWER (A/B/C/D) : ").upper()
        res = l[5].replace("\n",'')

        if ans==res:
            print("GREAT! CORRECT ANSWER ")
            marks+=1
        else:
            print("OOPS! INCORRECT ANSWER " ,"CORRECT ANSWER IS :",res)
        print()
        n+=1

    print() 
  
    print("#"*5," RESULT " ,"#"*5)
    correct=marks
    incorrect=10-marks
    print(f"CORRECT ANSWERS - {correct}")
    print(f"INCORRECT ANSWERS - {incorrect}")

    cur.execute("INSERT INTO result(name,subject,marks,time) values(%s,%s,%s,%s) ",(user,sub,marks,t))
    db.commit()

# OVERALL RESULT------------------------

def Result():
    global user 
    print("#"*10,"RESULT","#"*10)
    print()

    cur.execute("SELECT * FROM result WHERE name = %s", (user,))
    user1 = cur.fetchall()

    for row in user1:
        print("NAME    : ", row[0])
        print("SUBJECT : ", row[1])
        print("MARKS   : ", row[2])
        print("TIME    : ", row[3])
        print("\n")

# LOGOUT---------------------------------------

def Logout():
    global login_st
    try:
        c=input("Do you want to exit press y ,otherwise n : ").lower()

        if c=="n":
            main()

        elif c=="y":
            print("THANKS TO VISIT HERE , PLEASE VISIT AGAIN")
            login_st=False
            exit()
            
    except Exception as e:
        print(e)
        print("Invalid Input ! Try Again  ")
        Logout()


if __name__ == "__main__":
    main()