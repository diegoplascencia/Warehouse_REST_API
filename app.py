from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
import sqlite3 

from create_database import create_db

create_db()

app = Flask(__name__)
api = Api(app)

@app .route('/')
def index():
	return render_template("base.html")

class ItemList(Resource):
	def get(self):
		all_items = []
		connection = sqlite3.connect('warehouse_inventory.db')
		cursor = connection.cursor()

		query_all_items = "SELECT * FROM inventory"
		for result in cursor.execute(query_all_items):
			all_items.append(result)
		connection.commit()
		connection.close()

		return all_items

class Item(Resource):
	parser= reqparse.RequestParser()
	parser.add_argument('price', type = float, required = True,
		help = "This field can not be left blank!")
	parser.add_argument('existance',type = int,required = True,
		help = "This field can not be left blank!")

	def get(self, item_name):
		connection = sqlite3.connect('warehouse_inventory.db')
		cursor = connection.cursor()
		get_item = "SELECT * FROM inventory WHERE item=?"
		result = cursor.execute(get_item,(item_name,))
		row = result.fetchone()
		if row:
			return row
		else:
			return {'message': 'The item {} does not exist!'.format(item_name)}, 400

	def post(self, item_name):
		data = Item.parser.parse_args()
		connection = sqlite3.connect('warehouse_inventory.db')
		cursor = connection.cursor()

		look_for_duplicates = "SELECT * FROM inventory WHERE item=?"
		apply_query = cursor.execute(look_for_duplicates, (item_name,))
		item_exist = apply_query.fetchone() 
		if item_exist:
			return {'message': 'The item {} already exists!'.format(item_name)}, 400
		else:
			insert_query = "INSERT INTO inventory VALUES (NULL, ?, ?, ?)"
			cursor.execute(insert_query,(item_name, data['price'], data['existance']))

			connection.commit()
			connection.close()
			return {"message": "Item: {} added to the db.".format(item_name)}

	def put(self,item_name):
		data = Item.parser.parse_args()
		connection = sqlite3.connect('warehouse_inventory.db')
		cursor = connection.cursor()
		existing_id_query = "SELECT id FROM inventory WHERE item=?"
		apply_query = cursor.execute(existing_id_query, (item_name,))
		item_id_exist = apply_query.fetchone() 
		print("\nitem_id_exist\n", item_id_exist)
		if item_id_exist:
			update_val_query = "UPDATE inventory SET price=?, existance=? WHERE id=?"
			apply_update = cursor.execute(update_val_query, (data['price'], data['existance'], item_id_exist[0]))

			connection.commit()
			connection.close()
			return {"message": "Item: {} values updated.".format(item_name)}
		else:
			insert_query = "INSERT INTO inventory VALUES (NULL, ?, ?, ?)"
			cursor.execute(insert_query,(item_name, data['price'], data['existance']))

			connection.commit()
			connection.close()
			return {"message": "Item: {} added to the db.".format(item_name)}

	def delete(self, item_name):
		connection = sqlite3.connect('warehouse_inventory.db')
		cursor = connection.cursor()
		look_for_duplicates = "SELECT * FROM inventory WHERE item=?"
		apply_query = cursor.execute(look_for_duplicates, (item_name,))
		item_exist = apply_query.fetchone() 
		if item_exist:
			delete_query = "DELETE FROM inventory WHERE item=?"
			apply_query = cursor.execute(delete_query, (item_name,))
			connection.commit()
			connection.close()
			return {'message': 'Item {} deleted!!'.format(item_name)}
		else:
			return {'message': 'The item {} does not exist!'.format(item_name)}, 400

api.add_resource(Item, '/item/<string:item_name>')	
api.add_resource(ItemList, '/items_list')

app.run(port = 5000, debug = True)