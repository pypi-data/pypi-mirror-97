import matplotlib.pyplot as plt

from . import container

#Inputs: x = stock price, strike = strike price, p = premium
#Output: Net Profit or Loss

def longCall(x, strike, p):
	if x < strike:
		return -p
	elif x >= strike:
		return x - strike - p
	else:
		return None

def shortCall(x, strike, p):
	if x < strike:
		return p
	elif x >= strike:
		return p - (x - strike)
	else:
		return None

def longPut(x, strike, p):
	if x < strike:
		return strike - x - p
	elif x >= strike:
		return -p


def shortPut(x, strike, p):
	if x < strike:
		return p + (x - strike)
	elif x >= strike:
		return p

def graphCalls(optionObj, contractName, display = True, export = False, output = 'graph.pdf'):

	s = float(optionObj.getAttr(contractName, 'Strike'))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]

	y_long = [longCall(i, s, lp) for i in x]
	y_short = [shortCall(i, s, lp) for i in x]

	fig, axs = plt.subplots(2)
	fig.suptitle("Call Option: " + contractName)
	axs[0].axvline(x = optionObj.stockPrice)
	axs[0].plot(x, y_long)
	axs[0].title.set_text("Long Call")
	axs[0].set_xlabel("Stock Price at Expiration")
	axs[0].set_ylabel("Profit/Loss ($)")

	axs[1].plot(x, y_short)
	axs[1].title.set_text("Short Call")
	axs[1].set_xlabel("Stock Price at Expiration")
	axs[1].set_ylabel("Profit/Loss ($)")
	# axs[1].axvline(x = optionObj.stockPrice)

	fig = plt.gcf().subplots_adjust(hspace = 0.5)
	# fig.subplots_adjust(hspace = 0.2)

	if export == True:
		plt.savefig(output)

	if display == True:
		plt.show()

def graphPuts(optionObj, contractName, display = True, export = False, output = 'graph.png'):

	s = float(optionObj.getAttr(contractName, 'Strike'))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]

	y_long = [longPut(i, s, lp) for i in x]
	y_short = [shortPut(i, s, lp) for i in x]

	fig, axs = plt.subplots(2)
	fig.suptitle("Put Option: " + contractName)
	axs[0].plot(x, y_long)
	axs[0].title.set_text("Long Put")
	axs[0].set_xlabel("Stock Price at Expiration")
	axs[0].set_ylabel("Profit/Loss ($)")

	axs[1].plot(x, y_short)
	axs[1].title.set_text("Short Put")
	axs[1].set_xlabel("Stock Price at Expiration")
	axs[1].set_ylabel("Profit/Loss ($)")

	fig = plt.gcf().subplots_adjust(hspace = 0.5)
	# fig.subplots_adjust(hspace = 0.2)

	if export == True:
		plt.savefig(output)

	if display == True:
		plt.show()



def graphLongCall(optionObj, contractName, export = False):
	s = float(optionObj.getAttr(contractName, 'Strike'))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]
	y = [longCall(i, s, lp) for i in x]

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y)

	if export == True:
		plt.savefig('options.png')

	plt.show()

def graphShortCall(optionObj, contractName, export = False):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]
	y = [shortCall(i, s, lp) for i in x]

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y)

	if export == True:
		plt.savefig('options.png')

	plt.show()

def graphLongPut(optionObj, contractName, export = False):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]
	y = [longPut(i, s, lp) for i in x]

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y)

	if export == True:
		plt.savefig('options.png')

	plt.show()

def graphShortPut(optionObj, contractName, export = False):
	s = float(str(optionObj.getAttr(contractName, 'Strike')).replace(',', '').replace('\n', ''))
	lp = float(optionObj.getAttr(contractName, 'Last Price'))

	x = [i for i in range(round(float(optionObj.stockPrice)) // 2, round(float(optionObj.stockPrice)) * 2)]
	y = [shortPut(i, s, lp) for i in x]

	plot_title = contractName
	plt.title(plot_title)
	plt.plot(x, y)

	if export == True:
		plt.savefig('options.png')

	plt.show()
