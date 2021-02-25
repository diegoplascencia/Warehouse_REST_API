import sqlite3

def create_db():
	connection = sqlite3.connect('warehouse_inventory.db')
	cursor = connection.cursor()
	print("\n......................................")
	print("Creating DB...")
	print("......................................\n")
	create_table = """CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, item text, 
						price real, existance int)"""
	cursor.execute(create_table)
	print("\n......................................")
	print("DB created...")
	print("......................................\n")
	connection.commit()
	connection.close()