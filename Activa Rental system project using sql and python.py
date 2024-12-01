import mysql.connector as myc


conn = myc.connect(user = 'root',
                  password= 'Qwert',
                  host= 'localhost',
                  database= 'Activa_rental_management_system')

cur= conn.cursor()

def main_menu():
    while True:
        print("\nWelcome to Cyber Success Activa Rental House")
        available_activa = get_available_activa()
        print(f"No of Activa Available: {available_activa}")
        print("1. Rent\n2. Return\n3. Owner\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            rent_activa()
        elif choice == '2':
            return_activa()
        elif choice == '3':
            owner_access()
        elif choice == '4':
            print("Thank you for visiting!")
            break
        else:
            print("Invalid choice. Please try again.")

def get_available_activa():
    cur.execute("SELECT available_activa FROM activa_status WHERE id = 1")
    result = cur.fetchone()
    return result[0] if result else 0

def rent_activa():
    print("\nWelcome to Rent")
    print("T&C:\n1. Aadhaar Card is Mandatory.\n2. Driving Licence is Mandatory.\n3. One Activa for One Day: 500/-")
    conform = input("Conform (Y/N): ").upper()
    if conform != 'Y':
        return

    num_activa = int(input("Enter No of Activa: "))
    available_activa = get_available_activa()
    
    if num_activa > available_activa:
        print("Not enough Activa available for rent.")
        return

    name = input("Enter Your Name: ")
    phone_number = input("Enter Your Phone No: ")
    address = input("Enter Your Address: ")
    aadhaar_no = input("Enter Your Aadhaar No: ")
    driving_license_no = input("Enter Your Driving Licence No: ")
    days = int(input("Enter No of Day for Booking: "))
    total_bill = 500 * days

    print(f"Bill: {total_bill}")
    conform = input("Conform (Y/N): ").upper()
    if conform != 'Y':
        return

    try:
        cur.execute('''
            INSERT INTO rental_info (name, phone_number, address, aadhaar_no, driving_license_no, num_activa, days, total_bill, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        ''', (name, phone_number, address, aadhaar_no, driving_license_no, num_activa, days, total_bill))
        cur.execute("UPDATE activa_status SET available_activa = available_activa - %s WHERE id = 1", (num_activa,))
        conn.commit()
        print("Successful Booking")

        # Save the bill in a text file
        with open(f"{name}_bill.txt", "w") as file:
            file.write(f"Customer: {name}\nTotal Bill: {total_bill}\nDays: {days}\nActiva Rented: {num_activa}")
    except myc.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

def return_activa():
    print("\nWelcome to Return")
    aadhaar_no = input("Enter Your Aadhaar No: ")
    
    cur.execute("SELECT num_activa FROM rental_info WHERE aadhaar_no = %s AND status = 'Pending'", (aadhaar_no,))
    result = cur.fetchone()
    
    if not result:
        print("No active rental found for this Aadhaar number.")
        return
    
    num_rented_activa = result[0]
    num_return = int(input("No Of Activa Return: "))
    
    if num_return > num_rented_activa:
        print("You cannot return more Activa than you rented.")
        return

    try:
        cur.execute("UPDATE activa_status SET available_activa = available_activa + %s WHERE id = 1", (num_return,))
        cur.execute("UPDATE rental_info SET status = 'Closed' WHERE aadhaar_no = %s", (aadhaar_no,))
        conn.commit()
        print("Successful Return")
    except myc.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    
def owner_access():
    print("\nOwner Access")
    secure_code = input("Owner Secure Code: ")
    
    if secure_code != "1234":  # Replace with your actual secure code
        print("Invalid Secure Code")
        return

    cur.execute("SELECT * FROM rental_info")
    rows = cur.fetchall()
    
    for row in rows:
        print(f"\nName: {row[1]}\nPhone Number: {row[2]}\nAddress: {row[3]}\nAadhaar No: {row[4]}")
        print(f"Driving Licence No: {row[5]}\nNo Of Activa Booking: {row[6]}\nNo Of Day Booking: {row[7]}")
        print(f"Status: {row[8]}")

main_menu()