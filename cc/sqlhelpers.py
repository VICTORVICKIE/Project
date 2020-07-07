from cc import mysql
from cc.routes import session
from cc.Blockchain import Block,Blockchain,update_hash


class InvalidTranscationException(Exception):
    pass


class InsufficientCCException(Exception):
    pass


class Table():
    def __init__(self, table_name,*args,**kwargs):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args
        primary_key = kwargs.get('primary_key')
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column

            cur = mysql.connection.cursor()
            #print("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            if primary_key == 'roll':
            	cur.execute("ALTER TABLE %s ADD PRIMARY KEY (%s)"%(self.table,primary_key))
            	mysql.connection.commit();cur.close()
            else:
                cur.close()

    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    def getone(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data

    def replace(self,name,email,roll,password):
    	cur = mysql.connection.cursor()
    	cur.execute("REPLACE INTO  %s(name,email,roll,password) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")"%(self.table,name,email,roll,password))
    	mysql.connection.commit(); cur.close()



    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()


    def deleteall(self):
        self.drop()
        self.__init__(self.table,*self.columnsList)


    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

    def insert(self, *args):
        data = ""
        for arg in args:
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()

def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()


def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * from %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

def isnewuser(roll):
    users = Table("users", "name", "email", "roll", "password")
    data = users.getall()
    rolls = [user.get('roll') for user in data]

    return False if roll in rolls else True

def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain","number","hash","previous","data","nonce")
    for b in blockchain_sql.getall():
        blockchain.add_block(Block(int(b.get('number')),b.get('previous'),b.get('data'),int(b.get('nonce'))))

    return blockchain

def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain","number","hash","previous","data","nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(), block.previous_hash, block.data, block.nonce)


def send_campus_coins(sender, recipient, amount,time):
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTranscationException("Invalid Transcation.")

    if amount > get_balance(sender) and sender != "BANK":
        raise InsufficientCCException("Insufficient Campus Coins")

    elif sender == recipient or amount <= 0.00:
        raise InvalidTranscationException("Invalid Transcation.")
    elif isnewuser(recipient):
        raise InvalidTranscationException("User Does Not Exist")

    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = f"{sender}-->{recipient}-->{amount}-->{time}"
    blockchain.mine(Block(number,data=data))
    sync_blockchain(blockchain)

def get_balance(roll):
    balance = 0
    blockchain = get_blockchain()
    for block in blockchain.chain:
        data = block.data.split("-->")
        if roll == data[0]:
            balance -= float(data[2])

        elif roll == data[1]:
            balance += float(data[2])
            
    return balance


#get the last copy of the blockchain
def getLastBlockchain():
    blockchain = Table("blockchain")
    unsorted = list(blockchain.getall())
    sorted = []
    for block in unsorted:
        if block.get('number') is not None:
            sorted.insert(int(block.get('number'))-1,block)

    return sorted

def verifyBlockchain():
    blockchain = getLastBlockchain()#; print(blockchain)

    for n in range(len(blockchain)):
        block_hash = update_hash(
            blockchain[n].get('previous'),
            blockchain[n].get('number'),
            blockchain[n].get('data'),
            blockchain[n].get('nonce')
        )

        if block_hash != blockchain[n].get('hash'):
            return False
        elif block_hash[:4] != "0000":
            return False

        if n < len(blockchain)-1:
            if block_hash != blockchain[n+1].get('previous'):
                return False

    return True







"""def test():
    blockchain = Blockchain()
    database = ["VICTOR","Y","rs.x","6pm"]

    n = 0
    
    for data in database:
        n += 1
        blockchain.mine(Block(number=n,data=data))
    sync_blockchain(blockchain)
    #blockchain_sql = Table("blockchain","number","hash","previous","data","nonce")
    #blockchain_sql.deleteall()"""






