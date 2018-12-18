# import numpy as np
#
# def load_data(name):
#
#     data = np.load(name)
#     return data
#
# def load_data_wrapper():
#
#     name = 'training_data.npy'
#     tr_d = load_data(name)
#     training_inputs = [np.reshape(x, (784, )) for x in tr_d[0]]
#     training_results_vectors = [np.reshape(y,(62,)) for y in tr_d[1]]
#     # training_data = zip(training_inputs, training_results)
#     name = 'testing_data.npy'
#     te_d = load_data(name)
#     test_inputs = [np.reshape(x, (784, )) for x in te_d[0]]
#     test_result_vector = [np.reshape(y,(62,)) for y in te_d[1]]
#     test_results =[]
#     training_results=[]
#     for a in training_results_vectors:
#         i = a.tolist().index(1.)
#         training_results.append(i)
#     for a in test_result_vector:
#         i = a.tolist().index(1.)
#         test_results.append(i)
#     test_results = np.array(test_results)
#     # test_data = zip(test_inputs, test_results)
#     return training_inputs , training_results, test_inputs,test_results
