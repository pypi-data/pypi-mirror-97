import sqlite3 as _sql
class db():
	def __init__(self,conn,values):
		if conn:
			self._conn=_sql.connect(conn)
			self._cursor=self._conn.cursor()
		else:
			self._conn=False
		if isinstance(values, dict):
			self._values=values
		else:
			print("Your values must be a dict")
			self._values={}
	def get(self,thing,type,where='11'):
		if self._conn:
			self._cursor.execute(f"SELECT var{thing} FROM {type} WHERE {where[0]} LIKE '{where[1]}'")
			return self._cursor.fetchone()[0]
		else:
			return "null"
	def set(self,things,type,where=["id",123455]):
		if self._conn:
			self._cursor.execute(f"UPDATE {type} SET var{things[0]}='{things[1]}' WHERE {where[0]} == {where[1]}")
			self._conn.commit()
	async def set_all(self, client):
		valstr="id INT"
		for var in self._values:
			valstr+=",\n	var"+var+" TEXT"
		gs=["servers", "globals", "channels"]
		for g in client.guilds:
			gs.append("server"+str(g.id))
		for n in gs:
			self._cursor.execute("""CREATE TABLE IF NOT EXISTS """+str(n)+"""(
		"""+valstr+"""
		)""")
		for var in self._values:
			for n in gs:
				try:
					self._cursor.execute(f"alter table {n} add column 'var{var}' 'TEXT'")
				except:
					pass
		adds=""
		for v in self._values:
			if v!="id":
				adds+=f",'{self._values[v]}'"
		for guild in client.guilds:
			self._values["id"]=f'{guild.id}'
			try:
				if self._cursor.execute(f"SELECT id FROM servers WHERE id = '{guild.id}'").fetchone() is None:
					self._cursor.execute(f"INSERT INTO servers VALUES('{guild.id}'{adds})")
			except Exception as e:
				pass
			for var in self._values:
				try:
					if self._cursor.execute(f"SELECT var{var} FROM servers WHERE id = '{guild.id}'").fetchone()[0] is None:
						self._cursor.execute(f'UPDATE servers SET var{var}="{info._vars[var]}" WHERE id="{guild.id}"')
				except Exception as e:
					pass
		for channel in client.get_all_channels():
			self._values["id"]=f'{channel.id}'
			try:
				if self._cursor.execute(f"SELECT id FROM channels WHERE id = '{channel.id}'").fetchone() is None:
					self._cursor.execute(f"INSERT INTO channels VALUES('{channel.id}'{adds})")
			except Exception as e:
				pass
			for var in self._values:
				try:
					if self._cursor.execute(f"SELECT var{var} FROM channels WHERE id = '{channel.id}'").fetchone()[0] is None:
						self._cursor.execute(f'UPDATE channels SET var{var}="{info._vars[var]}" WHERE id="{channel.id}"')
				except Exception as e:
					pass
		for member in client.get_all_members():
			self._values["id"]=f'{member.id}'
			try:
				if self._cursor.execute(f"SELECT id FROM globals WHERE id = '{member.id}'").fetchone() is None:
					self._cursor.execute(f"INSERT INTO globals VALUES('{member.id}'{adds})")
			except Exception as e:
				pass
			for var in self._values:
				try:
					if self._cursor.execute(f"SELECT var{var} FROM globals WHERE id = '{member.id}'").fetchone()[0] is None:
						self._cursor.execute(f'UPDATE globals SET var{var}="{info._vars[var]}" WHERE id="{member.id}"')
				except Exception as e:
					pass
			for guild in client.guilds:
				try:
					if self._cursor.execute(f"SELECT id FROM server{guild.id} WHERE id = '{member.id}'").fetchone() is None:
						self._cursor.execute(f"INSERT INTO server{guild.id} VALUES('{member.id}'{adds})")
				except Exception as e:
					pass
				for var in self._values:
					try:
						if self._cursor.execute(f"SELECT var{var} FROM server{guild.id} WHERE id = '{member.id}'").fetchone()[0] is None:
							self._cursor.execute(f'UPDATE server{guild.id} SET var{var}="{info._vars[var]}" WHERE id="{member.id}"')
					except Exception as e:
						pass
		self._conn.commit()