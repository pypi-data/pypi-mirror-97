class LinearRegression:
    #def __init__(self, name, age):
    #    je ne sais pas
    def fit(self, X, y, method, learning_rate=0.01, iterations=500, batch_size=32):

        # x devient une matrice avec des 1 en bas avec la taille de y
        X = np.concatenate([X, np.ones_like(y)], axis=1)
        # on récupère la taille de X et y
        rows, cols = X.shape
        if method == 'solve':
            # si on a plus de lignes que de variables, we gather the rank of the matrix
            if rows >= cols == np.linalg.matrix_rank(X):
                # on stocke dans les coefficients le produit matriciel avec la formule connue
                self.weights = np.matmul(
                    np.matmul(
                        np.linalg.inv(
                            np.matmul(
                                X.transpose(),
                                X)),
                        X.transpose()),
                    y)
            # si on a moins de lignes que de colonnes
            else:
                print('X has not full column rank. method=\'solve\' cannot be used.')

        # METHOD Stochastic gradient descent
        elif method == 'sgd':
            self.weights = np.random.normal(scale=1/cols, size=(cols, 1))
            for i in range(iterations):
                Xy = np.concatenate([X, y], axis=1)
                np.random.shuffle(Xy)
                X, y = Xy[:, :-1], Xy[:, -1:]
                for j in range(int(np.ceil(rows/batch_size))):
                    start, end = batch_size*j, np.min([batch_size*(j+1), rows])
                    Xb, yb = X[start:end], y[start:end]
                    gradient = 2*np.matmul(
                        Xb.transpose(),
                        (np.matmul(Xb,
                                   self.weights)
                         - yb))
                    self.weights -= learning_rate*gradient

        else:
            print(f'Unknown method: \'{method}\'')

        return self

    def predict(self, X):

        # Si on a pas attribué les poids alors c'est qu'on a pas utilisé le fit
        if not hasattr(self, 'weights'):
            print('Cannot predict. You should call the .fit() method first.')
            return
        # Sinon : on reprend le X de départ et on ajoute des une matrice de 1 telle que ...
        X = np.concatenate([X, np.ones((X.shape[0], 1))], axis=1)

        # Si on a un nombre différent de variables que de coefficients alors on a un problème
        if X.shape[1] != self.weights.shape[0]:
            print(f'Shapes do not match. {X.shape[1]} != {self.weights.shape[0]}')
            return

        # Sinon on retourne simplement le produit matriciel en X et les weights obtenus

        return np.matmul(X, self.weights)

    def rmse(self, X, y):

        # on utilise la fonction ci dessus
        y_hat = self.predict(X)

        # si on a pas de prédiction on ne peut pas calculer le RMSE
        if y_hat is None:
            return

        # Sinon on applique la formule standard
        return np.sqrt(((y_hat - y)**2).mean())
