from sklearn.neural_network import MLPClassifier


def nar_model(train_data, train_label, embedding):
    """
    A multi-layer neural network model

    Prameters:
    train_data -- dataset that have articles user cluster clicked, and skipped
    train_label -- to simplify, use 1 or 0 to classify: 0 not clicked, 1 clicked
    embedding -- article embedding: numpy matrix, the output of ACR model

    Output:
    recommendation: list of article id that might be clicked by this class of user

    """
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(5, 2), random_state=1)

    clf.fit(train_data, train_label)
    MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1,
                solver='lbfgs')
    
    result = clf.predict(embedding)
    recommendation = []
    # store article id into recommendtaion
    for i in range(len(result)):
        if result[i] == 1:
            recommendation.append(i)

    return recommendation

def main():
    # test train_data: convert to number if the input is word, each row should be feature vector of a document
    train_data = [[0., 0.], [1., 1.]]
    # test train_label: whether user clicked that document or not
    train_label = [0, 1]
    # test data
    embedding = [[2., 2.], [-1., -2.]]
    recommendation = nar_model(train_data, train_label, embedding)
    print(recommendation)

if __name__ == "__main__":
    main()