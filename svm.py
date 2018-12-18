import mnist_loader
from sklearn import svm
import numpy as np
import pickle

def svm_baseline():
    training_input, training_results, test_input,test_results = mnist_loader.load_data_wrapper()
    # train
    training_input = np.array(training_input)
    training_results = np.array(training_results)
    test_input = np.array(test_input)
    test_results = np.array(test_results)
    print(training_input.shape)
    print(training_results.shape)
    print(test_input.shape)
    print(test_results.shape)
    clf = svm.SVC()
    clf.fit(training_input, training_results)
    filename = 'finalized_model2.sav'
    pickle.dump(clf, open(filename, 'wb'))
    predictions = [ int(a) for a in clf.predict(test_input)]
    num_correct = sum(int(a == y) for a, y in zip(predictions, test_results))
    print("Baseline classifier using an SVM.")
    print(str(num_correct) + " of " + str(len(test_input)) + " values correct.")
    # scores = cross_val_score(clf, X, y, cv=10)
    # print(scores)
if __name__ == "__main__":
    svm_baseline()
