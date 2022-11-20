# Four Screenshots
# 1) Program Menu
# 2) Listing of a selection of your menu
# 3) Display the results of a SELECT statement 
# 4) Display the results of a INSERT statement

import datetime
import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

class Customer:
    def addCustomer(self, name, phoneno):
        cursor.execute("INSERT INTO Customer (name, phoneno) VALUES ('{}', '{}');".format(name, phoneno))
        connection.commit()
        print("\n\n=====================================================================")
        print("\t\t\tCUSTOMERS TABLE UPDATED")
        print("=====================================================================")
        print("ID\tNAME\t\t\tPHONE NO.\t\tTOTAL BILL($)")
        print("=====================================================================")
        cursor.execute("SELECT * FROM Customer")
        for row in cursor.fetchall():
            print("{}\t{}\t\t{}\t\t{}".format(row[0], row[1], row[2], row[3]))

    def getPeopleID(self, name, phoneno):
        cursor.execute("SELECT id FROM Customer where name='{}' AND phoneno='{}'".format(name, phoneno))
        return cursor.fetchall()[0][0]

    def getName(self, id):
        cursor.execute("SELECT name FROM Customer where id={}".format(id))
        return cursor.fetchall()[0][0]

    def getPhoneNumber(self, id):
        cursor.execute("SELECT phoneno FROM Customer where id={}".format(id))
        return cursor.fetchall()[0][0]

    def getBillAmount(self, id):
        cursor.execute("SELECT totalBill FROM Customer WHERE id={}".format(id))
        return cursor.fetchall()[0][0]

    def updateBillAmount(self, id, amount):
        cursor.execute("UPDATE Customer SET totalBill={} WHERE id={}".format(amount, id))
        connection.commit()

class Reservation:
    def doReservation(self, customerid, arrivaldate, departuredate):
        cursor.execute("INSERT INTO Reservation (id, arrivaldate, departuredate) VALUES ({}, '{}', '{}')".format(customerid, arrivaldate, departuredate))
        connection.commit()
        print("\n\n==============================================================")
        print("\t\tRESERVATION TABLE UPDATED")
        print("==============================================================")
        print("ID\tROOM NO.\tARRIVAL DATE\t\tDEPARTURE DATE")
        print("==============================================================")
        cursor.execute("SELECT * FROM Reservation")
        for row in cursor.fetchall():
            print("{}\t{}\t\t{}\t\t{}".format(row[0], row[1], row[2],row[3]))

    def getRoomNo(self, customerid):
        cursor.execute("SELECT roomno FROM Reservation WHERE id={}".format(customerid))
        return cursor.fetchall()[0][0]

    def getArrivalDate(self, customerid):
        cursor.execute("SELECT arrivaldate FROM Reservation WHERE id={}".format(customerid))
        return cursor.fetchall()[0][0]

    def getDepartureDate(self, customerid):
        cursor.execute("SELECT departuredate FROM Reservation WHERE id={}".format(customerid))
        return cursor.fetchall()[0][0]

class Restaurant:
    def getMenu(self):
        print("===============================================")
        print("\t\tRESTAURANT MENU")
        print("===============================================")
        print("S.NO\tITEM\t\t\t\tCOST($)")
        print("===============================================")
        cursor.execute("SELECT id, fooditem, cost FROM Restaurant")
        for row in cursor.fetchall():
            print("{}\t{}\t\t\t${}".format(row[0], row[1], row[2]))
        print("===============================================")

    def getFoodDetails(self, id):
        cursor.execute("SELECT fooditem, cost FROM Restaurant WHERE id={}".format(id))
        return cursor.fetchall()[0]

class Service:
    def getServices(self):
        print("===============================================")
        print("\t\tADITIONAL SERVICES")
        print("===============================================")
        print("S.NO\tSERVICE\t\t\t\tCOST($)")
        print("===============================================")
        cursor.execute("SELECT * FROM Service")
        for row in cursor.fetchall():
            print("{}\t{}\t\t\t\t${}".format(row[0], row[1], row[2]))

    def getServiceDetails(self, id):
        cursor.execute("SELECT servicename, cost FROM Service WHERE id={}".format(id))
        return cursor.fetchall()[0]


def main():
    today = datetime.datetime.now()

    print("======================================================")
    print("\tCUSTOMER RESERVATION RESTAURANT SERVICE")  
    print("======================================================")

    # Check if the user is an existing customer
    existingCustomer = input("Are you already an existing customer(Y/N)? ")

    # If not, get the details (name, phoneno, departuredate)
    # Customer id and arrival date are calculated automatically
    if(existingCustomer == "N"):
        name = input("Enter your name: ")
        phoneno = input("Enter your phone number: ")
        arrivaldate = "{}/{}/{}".format(today.day, today.month, today.year)
        departuredate = input("Enter your departure date(dd/mm/yyyy): ")
        
        # Adding a new customer to the DB
        customer = Customer()
        customer.addCustomer(name, phoneno)
        customerid = customer.getPeopleID(name, phoneno)

        # Adding reservation entry to the DB
        reservation = Reservation()
        reservation.doReservation(customerid, arrivaldate, departuredate)
        print("\n\nCustomer and reservation entries into the DB are SUCCESSFUL! ")
        print("Please note that your CUSTOMER ID is {} and ROOM NUMBER is {}".format(customerid, reservation.getRoomNo(customerid)))
        print("Thank you for chosing us :)")

    elif existingCustomer == "Y":
        try:
            customerid = input("Enter your customer id: ")

            # Check if customer with that ID exists. If yes, fetch his/her details. Else warn!
            customer = Customer()
            customername = customer.getName(customerid)
            print("\nWelcome {}\n".format(customername.upper()))

            print("Have a look at the below menu\n")
            print("Enter 1 for Restaurant menu")
            print("Enter 2 for additional services")
            print("Enter Q to QUIT")
            option = input("Please provide your choice: ")

            # Loop until user provides a valid input
            while True:

                # Display restaurant menu (fetch food items and cost from the DB)
                # Update the customer bill after he/she chose a valid item from the menu
                # And make changes to the DB regarding updated bill
                if option == "1":
                    restaurant = Restaurant()
                    restaurant.getMenu()
                    foodOption = input("Please enter your choice: ")
                    try:
                        foodname, foodcost = restaurant.getFoodDetails(foodOption)
                        print("{} which costs ${} will be delivered to your desk in 5 mins :)".format(foodname.upper(), foodcost))
                        oldBillAmount = customer.getBillAmount(customerid)
                        customer.updateBillAmount(customerid, oldBillAmount + foodcost)
                        print("{}'s updated BILL AMOUNT: ${}\n".format(customername.upper(), customer.getBillAmount(customerid)))
                    except:
                        print("Invalid Choice :(")
                    break

                # Display Service menu (fetch service names and cost from DB)
                # Update the customer bill after he/she chose a valid item from the menu
                # And make changes to the DB regarding updated bill
                elif option == "2":
                    service = Service()
                    service.getServices()
                    serviceOption = input("Please enter your choice: ")
                    try:
                        servicename, servicecost = service.getServiceDetails(serviceOption)
                        print("{} which costs ${} will be at your doorsteps in 5 mins :)".format(servicename.upper(), servicecost))
                        oldBillAmount = customer.getBillAmount(customerid)
                        customer.updateBillAmount(customerid, oldBillAmount + servicecost)
                        print("{}'s updated BILL AMOUNT: ${}".format(customername.upper(), customer.getBillAmount(customerid)))
                    except:
                        print("Invalid Choice :(")
                    break

                elif option == "Q":
                    print("Thank you. Please come again :)")
                    break

                else:
                    option = input("Please provide a valid choice(1/2/Q): ")
        except:
            print("Sorry! A customer with that ID doesn't exist")
    
    else:
        print("Invalid Choice :(")
  
if __name__ == "__main__":
    main()
    
