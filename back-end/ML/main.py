# Import necessary modules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import pickle
import ML.tradeObj

# create the function which has this Trade object passed to it
def suggestChange(trade):

    with open('knn_notional.pkl', 'rb') as inp:
	    knn_notional = pickle.load(inp)
    with open('knn_quantity.pkl', 'rb') as inp:
        knn_quantity = pickle.load(inp)

    # Predict on dataset which model has not seen before
    y_test_notional = knn_notional.predict([[trade.getPreviousNotional()]])
    y_test_quantity = knn_quantity.predict([[trade.getPreviousQuantity()]])


    # can change these for given rules
    if abs(float(trade.getPreviousNotional()) - float(y_test_notional[0])) < 50000:
        y_test_notional = [trade.getPreviousNotional()]
    if abs(float(trade.getPreviousQuantity()) - float(y_test_quantity[0])) < 10:
        y_test_quantity = [trade.getPreviousQuantity()]

    # working under the assumption the order of test does not change when being iterated upon
    trade.setBothValues(y_test_notional[0], y_test_quantity[0])

    return trade
