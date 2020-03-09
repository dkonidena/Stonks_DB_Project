# Import necessary modules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import pickle
import random
import math
import time
import ML.tradeObj
import schedule

# create the function which has this Trade[] object passed to it
def cronJob(getAllTrades, neigboursFromRules, noOfIterations):
    print("Training starting...")
    allTrades = getAllTrades()
    trades = list()
    # get the size of the trades list
    d = len(allTrades)
    for i in range(noOfIterations): # noOfIterations
        # pseudorandom number
        r = random.random()
        # now find the largest value i such that i(i+1) < rd(d+1)
        i = math.floor(math.sqrt(r * d * (d + 1)))
        while ((i * (i + 1)) < (r * d * (d + 1))):
            i += 1

        # now add at that index
        trades.append(allTrades[i])

    X_train_notional = list()
    y_train_notional = list()
    X_train_quantity = list()
    y_train_quantity = list()
    for t in trades:
        X_train_notional.append([t.getPreviousNotional()])
        y_train_notional.append(t.getCurrentNotional())
        X_train_quantity.append([t.getPreviousQuantity()])
        y_train_quantity.append(t.getCurrentQuantity())

    knn_notional = KNeighborsClassifier(n_neighbors=neigboursFromRules) # neigboursFromRules
    knn_notional.fit(X_train_notional, y_train_notional)

    knn_quantity = KNeighborsClassifier(n_neighbors=neigboursFromRules) # neigboursFromRules
    knn_quantity.fit(X_train_quantity, y_train_quantity)

    # now save the state of these objects to the server
    with open('knn_notional.pkl', 'wb') as output:
	    pickle.dump(knn_notional, output, pickle.HIGHEST_PROTOCOL)
    with open('knn_quantity.pkl', 'wb') as output:
	    pickle.dump(knn_quantity, output, pickle.HIGHEST_PROTOCOL)

    print("Training finished...")

def job(allTrades, neigboursFromRules, noOfIterations):
    print("Scheduler started")
    schedule.every().day.at("00:00").do(cronJob, allTrades, neigboursFromRules, noOfIterations)
    while True:
        schedule.run_pending()
        time.sleep(1)
