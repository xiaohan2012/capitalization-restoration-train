class UnigramLabeler(object):
    """
    Labeler that operates on each token separately
    """
    def __init__(self, dict_vect, label_encoder, model):
        self._dict_vect = dict_vect
        self._label_encoder = label_encoder
        self._model = model
        
    def predict(self, list_of_token_features):
        """
        Parameter:
        ----------
        list_of_token_features: list<dict<str->object>>
            the features of input sentence tokens

        Return:
        ----------
        list of str: the token labels
        """
        X = self._dict_vect.transform(list_of_token_features)
        y = self._model.predict(X)
        return self._label_encoder.inverse_transform(y).tolist()
