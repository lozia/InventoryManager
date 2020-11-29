import MySQLdb

mydbconn = MySQLdb.connect("localhost", "root", "7586", "Inventory")
mycurs = mydbconn.cursor()


# User Functions:
def showAllP():
    sql = 'SELECT * FROM Product'
    mycurs.execute(sql)
    result = mycurs.fetchall()
    for product in result:
        print(product)


def showAllM():
    sql = 'SELECT * FROM Manufacturer'
    mycurs.execute(sql)
    result = mycurs.fetchall()
    for man in result:
        print(man)


def addProduct():
    c_pname = input('Product name: ')
    c_cost = input('Product cost: ')
    c_price = input('Product price: ')
    c_mname = input('Manufacturer: ')
    c_mid = findMid(c_mname)
    c_pid = pidGenerator()
    if confirmInput(c_pname) == 0:
        print('Abort modification.')
        return
    sql = 'INSERT INTO Product VALUES (%s, %s, %s, %s)'
    val = (c_pid, c_pname, c_cost, c_price)
    mycurs.execute(sql, val)
    mydbconn.commit()
    mycurs.execute('INSERT INTO Make VALUES ({mid}, {pid})'.format(mid=c_mid, pid=c_pid))
    mycurs.execute('SELECT * FROM Product WHERE pid = {pid}'.format(pid=c_pid))
    result1 = mycurs.fetchall()
    mycurs.execute('SELECT * FROM Make WHERE mid = {mid} AND pid = {pid}'.format(mid=c_mid, pid=c_pid))
    result2 = mycurs.fetchall()
    print('Added.\n', result1[0], '\n', result2[0])
    return c_pid


def addManufacture():
    c_mname = input('Manufacturer name: ')
    c_mid = midGenerator()
    print('MID is: ', c_mid)
    confirm = confirmInput(c_mname)
    if confirm == 0:
        print('Abort modification.')
        return
    sql = 'INSERT INTO Manufacturer VALUES (%s, %s)'
    val = (c_mid, c_mname)
    mycurs.execute(sql, val)
    mydbconn.commit()
    mycurs.execute('SELECT * FROM Manufacturer WHERE mid = {mid}'.format(mid=c_mid))
    print("Record added. ")
    result = mycurs.fetchall()
    print(result[0])
    return c_mid


def modifyProduct():
    product_identifier = input('Product name or product PID:')
    if product_identifier.isnumeric():
        c_pid = product_identifier
    else:
        c_pid = findPid(product_identifier)
    if pidChkr(c_pid) == 0:
        print('PID not found.')
        return
    cmd = input('n - modify name; c - modify cost; p - modify price.')
    col = 'pname'
    if cmd == 'n':
        col = 'pname'
    elif cmd == 'c':
        col = 'cost'
    elif cmd == 'p':
        col = 'price'
    par = input('New data:')
    if not par.isnumeric():
        par = '"' + par + '"'
    sql = 'UPDATE Product SET {column} = {new} WHERE pid = {pid}'.format(column=col, new=par, pid=c_pid)
    print(sql)
    try:
        mycurs.execute(sql)
    except MySQLdb.ProgrammingError:
        mydbconn.rollback()
        print('Operation Error. Check command carefully.')
        return
    finally:
        mydbconn.commit()
    print('Update successful.')


def updateStock():
    product_identifier = input('Product name or product PID:')
    if product_identifier.isnumeric():
        c_pid = product_identifier
    else:
        c_pid = findPid(product_identifier)
    if pidChkr(c_pid) == 0:
        print('PID not found.')
        return
    par = input('New amount: ')
    if not par.isnumeric():
        print('Numeric only.')
        return
    sql = 'UPDATE Stock SET amt = {new} WHERE pid = {pid}'.format(new=int(par), pid=c_pid)
    mycurs.execute(sql)
    mydbconn.commit()
    print('Update successful.')


def sell():
    product_identifier = input('Product name or product PID:')
    if product_identifier.isnumeric():
        c_pid = product_identifier
    else:
        c_pid = findPid(product_identifier)
    if pidChkr(c_pid) == 0:
        print('PID not found.')
        return
    par = input('Sales: ')
    if not par.isnumeric():
        print('Numeric only.')
        return
    mycurs.execute('SELECT amt FROM Sold WHERE pid = {pid}'.format(pid=c_pid))
    old = mycurs.fetchall()
    if len(old) == 0:
        c_amt = int(par)
        sql = 'INSERT INTO Sold Values ({pid}, {amt})'.format(pid=c_pid, amt=c_amt)
    else:
        c_amt = int(par) + int(old[0][0])
        sql = 'UPDATE Sold SET amt = {new} WHERE pid = {pid}'.format(new=c_amt, pid=c_pid)
    print(sql)
    mycurs.execute(sql)
    mydbconn.commit()
    print('Recorded.')


def modifyManufacture():
    man_identifier = input('Manufacturer name or MID:')
    if man_identifier.isnumeric():
        c_mid = man_identifier
    else:
        c_mid = findMid(man_identifier)
    if midChkr(c_mid) == 0:
        print('MID not found.')
        return
    c_mname = input('New name:')
    c_mname = '"' + c_mname + '"'
    sql = 'UPDATE Manufacturer SET mname = %s WHERE mid = %s'
    val = (c_mname, c_mid)
    mycurs.execute(sql, val)
    mydbconn.commit()
    print('Update successful.')


def PIDFinder():
    c_pname = input('Product name:')
    print(findPid(c_pname))


def MIDFinder():
    c_mname = input('Manufacturer name:')
    print(findMid(c_mname))


def insertNote():
    c_pid = input('Please provide Product PID: ')
    if pidChkr(c_pid) == 1:
        testsql = 'SELECT note FROM Note WHERE pid = {pid}'.format(pid=c_pid)
        mycurs.execute(testsql)
        test = mycurs.fetchall()
        if len(test) != 0:
            print('Note exists.')
            return
        note = input('Note: ')
        sql = 'INSERT INTO Note VALUES (%s, %s)'
        val = (c_pid, note)
        mycurs.execute(sql, val)
        mydbconn.commit()
        print('Note added.')
    else:
        print('Invalid PID. Try again.')


def lookupNote():
    c_pid = input('Please provide Product PID:')
    if pidChkr(c_pid) == 1:
        mycurs.execute('SELECT note FROM Note WHERE pid = {pid}'.format(pid=c_pid))
        result = mycurs.fetchall()
        for note in result:
            print(note[0])
    else:
        print('Bad PID.')


def deleteProduct():
    prod_identifier = input('Product name or PID:')
    if prod_identifier.isnumeric():
        c_pid = prod_identifier
    else:
        c_pid = findPid(prod_identifier)
    if pidChkr(c_pid) == 0:
        print('PID not found.')
        return
    mycurs.execute('DELETE FROM Note WHERE pid = {pid}'.format(pid=c_pid))
    mydbconn.commit()
    mycurs.execute('DELETE FROM Make WHERE pid = {pid}'.format(pid=c_pid))
    mydbconn.commit()
    deleteSold(c_pid)
    deleteStock(c_pid)
    mycurs.execute('DELETE FROM Product WHERE pid = {pid}'.format(pid=c_pid))
    mydbconn.commit()
    print('Successfully deleted.')


def deleteManufacturer():
    man_identifier = input('Manufacturer name or MID:')
    if man_identifier.isnumeric():
        c_mid = man_identifier
    else:
        c_mid = findMid(man_identifier)
    if midChkr(c_mid) == 0:
        print('MID not found.')
        return
    mycurs.execute('DELETE FROM Make WHERE mid = {mid}'.format(mid=c_mid))
    mydbconn.commit()
    mycurs.execute('DELETE FROM Manufacturer WHERE mid = {mid}'.format(mid=c_mid))
    mydbconn.commit()
    print('Successfully deleted.')


def deleteNote():
    prod_identifier = input('Product name or PID:')
    if prod_identifier.isnumeric():
        c_pid = prod_identifier
    else:
        c_pid = findPid(prod_identifier)
    if pidChkr(c_pid) == 0:
        print('PID not found.')
        return
    mycurs.execute('DELETE FROM Note WHERE pid = {pid}'.format(pid=c_pid))
    mydbconn.commit()
    print('Successfully deleted.')


def calCost():
    mycurs.execute('SELECT SUM(C.costs) FROM (SELECT price*amt AS costs FROM Product P, Stock S WHERE P.pid = S.pid) C')
    result = mycurs.fetchall()
    cost = result[0][0]
    print(cost)
    return cost


def calRevenue():
    revenue = calIncome() - calCost()
    print(revenue)
    return revenue


def calIncome():
    mycurs.execute('SELECT SUM(S.sales) FROM (SELECT price*amt AS sales FROM Product P, Sold S WHERE P.pid = S.pid) S')
    result = mycurs.fetchall()
    income = result[0][0]
    print(income)
    return income


# Helper Functions:
def confirmInput(string):
    print('Your input is: ', string)
    confirm = input('(Y/N)?')
    if confirm == 'Y' or confirm == 'y':
        return 1
    else:
        return 0


def pidChkr(pid):
    c_pid = int(pid)
    exist = 0
    mycurs.execute('SELECT pid FROM Product')
    id_checker = mycurs.fetchall()
    for ids in id_checker:
        if c_pid == int(ids[0]):
            exist = 1
    return exist


def midChkr(mid):
    c_mid = int(mid)
    exist = 0
    mycurs.execute('SELECT mid FROM Manufacturer')
    id_checker = mycurs.fetchall()
    for ids in id_checker:
        if c_mid == int(ids[0]):
            exist = 1
    return exist


def findPid(c_pname):
    sql = 'SELECT pid, pname FROM Product WHERE pname LIKE "%{string}%"'.format(string=c_pname)
    mycurs.execute(sql)
    result = mycurs.fetchall()
    if len(result) == 0:
        print('No product found.')
        return -1
    else:
        print(result)
    c_pid = input('PID: ')
    return c_pid


def findMid(c_mname):
    sql = 'SELECT mid, mname FROM Manufacturer WHERE mname LIKE "%{string}%"'.format(string=c_mname)
    mycurs.execute(sql)
    result = mycurs.fetchall()
    if len(result) == 0:
        askAdd = input('No matching manufacturer found. Add new? (Y/N)')
        if askAdd == 'Y' or askAdd == 'y':
            mid = addManufacture()
            return mid
        else:
            return -1
    else:
        print(result)
    c_mid = input('MID:')
    return c_mid


def pidGenerator():
    mycurs.execute('SELECT max(P.pid) FROM Product P')
    result = mycurs.fetchall()
    c_pid = result[0][0] + 1
    return c_pid


def midGenerator():
    mycurs.execute('SELECT max(M.mid) FROM Manufacturer M')
    result = mycurs.fetchall()
    c_mid = result[0][0] + 1
    return c_mid


def deleteStock(c_pid):
    sql = 'DELETE FROM Stock WHERE pid = {pid}'.format(pid=c_pid)
    try:
        mycurs.execute(sql)
    except MySQLdb.IntegrityError:
        # print('Error:', err, '. Please try again.')
        mydbconn.rollback()
        return
    finally:
        mydbconn.commit()


def deleteSold(c_pid):
    sql = 'DELETE FROM Sold WHERE pid = {pid}'.format(pid=c_pid)
    try:
        mycurs.execute(sql)
    except MySQLdb.IntegrityError:
        mydbconn.rollback()
        return
    finally:
        mydbconn.commit()


#######################################################################

def main():
    print('Thank you for choosing Inventory Manager.')

    while True:
        print('The following items are instructions.')
        cmd = input("""
allP -- List all listing products.
allM -- List all Manufacturers.
AP -- Add a product.
AM -- Add a manufacturer
MP -- Modify a product.
MM -- Modify a Manufacturer
US -- Update product availability
sell -- Record a sell event
PID -- Find Product ID.
MID -- Find Manufacturer ID
AN -- Add note to a product.
N -- Show a product's note.
DP -- Delete a product. Warning: All records related to this product will be deleted as well.
DM -- Delete a manufacturer. Warning: All records related to this manufacturer will be deleted as well.
DN -- Delete a note of a product.
CC -- Calculate total Cost
CR -- Calculate total Revenue.
CI -- Calculate total Income.
end-- quit Inventory Manager.

""")

        if cmd == 'X':
            return
        elif cmd == 'allP':
            print(' ')
            showAllP()
        elif cmd == 'allM':
            print(' ')
            showAllM()
        elif cmd == 'AP':
            print(' ')
            addProduct()
        elif cmd == 'AM':
            print(' ')
            addManufacture()
        elif cmd == 'MP':
            print(' ')
            modifyProduct()
        elif cmd == 'MM':
            print(' ')
            modifyManufacture()
        elif cmd == 'US':
            print(' ')
            updateStock()
        elif cmd == 'sell':
            print(' ')
            sell()
        elif cmd == 'AN':
            print(' ')
            insertNote()
        elif cmd == 'PID':
            print('  ')
            PIDFinder()
        elif cmd == 'MID':
            print('  ')
            MIDFinder()
        elif cmd == 'DP':
            print('  ')
            deleteProduct()
        elif cmd == 'DM':
            print('  ')
            deleteManufacturer()
        elif cmd == 'DN':
            print('  ')
            deleteNote()
        elif cmd == 'N':
            print(' ')
            lookupNote()
        elif cmd == 'CC':
            print('  ')
            calCost()
        elif cmd == 'CR':
            print('  ')
            calRevenue()
        elif cmd == 'CI':
            print('  ')
            calIncome()
        elif cmd == 'end':
            break
        else:
            print("Please follow instructions.")
        input('\nPress ENTER to continue.')

    mydbconn.close()


if __name__ == "__main__":
    main()
