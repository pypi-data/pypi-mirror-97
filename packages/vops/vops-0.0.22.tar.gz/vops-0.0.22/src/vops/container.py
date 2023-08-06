class OptionObj:
	def __init__(self):
		self.chain = None
		self.expiration = None
		self.stockPrice = None

	def __init__(self, a_chain, a_expiration, a_stockPrice):
		self.chain = a_chain
		self.expiration = a_expiration
		self.stockPrice = a_stockPrice

	def getExpiration(self):
		return self.expiration

	def getChain(self):
		return self.chain

	def getAttr(self, contractName, attr):
		colNum = self.chain.columns.get_loc(attr)
		row = self.chain.loc[self.chain['Contract Name'] == contractName]

		return row.iloc[0, colNum].replace(',', '')

class AggregateOptionObj:
	def __init__(self):
		self.call_chain = None
		self.put_chain = None
		self.expiration = None
		self.stockPrice = None

	def __init__(self, a_call_chain, a_put_chain, a_expiration, a_stockPrice):
		self.call_chain = a_call_chain
		self.put_chain = a_put_chain
		self.expiration = a_expiration
		self.stockPrice = a_stockPrice

	def getExpiration(self):
		return self.expiration

	def getCallChain(self):
		return self.call_chain

	def getPutChain(self):
		return self.put_chain

	def getAttr(self, contractName, type="Call", attr):
		if type == "Call":
			colNum = self.call_chain.columns.get_loc(attr)
			row = self.call_chain.loc[self.call_chain['Contract Name'] == contractName]

			return row.iloc[0, colNum].replace(',', '')

		elif type == "Put":
			colNum = self.put_chain.columns.get_loc(attr)
			row = self.put_chain.loc[self.put_chain['Contract Name'] == contractName]

			return row.iloc[0, colNum].replace(',', '')

class CumulativeChain:
	def __init__(self):
		self.chain = None
		self.expiration = None
		self.stockPrice = None

class Option:
	def __init__(self):
		self.contract_name = None
		self.type = None
		self.strike = None
		self.last_price = None


