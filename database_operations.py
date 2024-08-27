import numpy as np


inserting_new_data = "INSERT INTO Encodings (name, encoding) VALUES (%s, %s)"
getting_name = "SELECT name FROM Encodings WHERE encoding = %s"
# val = ("John", "Highway 21")


def insert_new_data(encodings, name, mydb):
    mycursor = mydb.cursor()
    separator = ", "
    encodings = separator.join(map(str, encodings))
    # print(len(encodings))
    data = (name, encodings)
    mycursor.execute(inserting_new_data, data)
    mydb.commit()
    # print(mycursor.rowcount, "record inserted.")
    # print("Name : ", name, "Index : ")
    # return name

def get_name(encodings, mydb):
    mycursor = mydb.cursor()
    separator = ", "
    encodings = separator.join(map(str, encodings))
    # print("Encodings = ", encodings)
    data = (encodings,)
    mycursor.execute(getting_name, data)
    result = mycursor.fetchall()
    # encodings = [row[0] for row in result]
    print(result)
    mydb.commit()
    # return encodings

def get_all_encodings(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT encoding FROM Encodings")
    encodings = mycursor.fetchall()
    for i in range(len(encodings)):
        encodings[i] = encodings[i][0].split(", ")
        # print(f"type(encoding{i})", type(encodings[i]))
    # encodings = encodings.split(", ")
    # print("encodings[0]", encodings[0])
    encodings = np.array(encodings, dtype=float)
    mycursor.execute("SELECT name FROM Encodings")
    names = mycursor.fetchall()
    # print(names)
    mydb.commit()
    return names, encodings

def get_details(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name, position, company, access FROM Encodings")
    details = mycursor.fetchall()
    return details