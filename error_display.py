import numpy as np
from itertools import izip
from tabulate import tabulate

    
def print_label_error(words,
                      features,
                      correct_labels, predicted_labels,
                      target_true_label=None, target_pred_label=None,
                      print_features=False,
                      model=None,
                      dict_vect=None,
                      label_encoder=None):
    if correct_labels != predicted_labels:
        # we want labels that are both
        # incorrect and meet our label specs
        if target_true_label and target_pred_label:
            display_or_not = map(lambda (cl, pl): cl != pl and
                                 cl == target_true_label and
                                 pl == target_pred_label,
                                 izip(correct_labels, predicted_labels))
        else:
            display_or_not = map(lambda (cl, pl): cl != pl,
                                 izip(correct_labels, predicted_labels))

        if np.any(display_or_not):
            # add some high lighting
            words = [("**" + w + "**" if flag else w)
                     for w, flag in izip(words, display_or_not)]
            
            data = [['Sentence:'] + words,
                    ['True:'] + correct_labels,
                    ['Pred:'] + predicted_labels]

            def get_feature_weight(label, feature_name, feature_value):
                if feature_value is None:  # ingnore null feature value
                    return 0

                if isinstance(feature_value, int):
                    feat_str = feature_name
                else:
                    feat_str = u"{}={}".format(feature_name, feature_value)
                
                # feature value in training data
                if feat_str in dict_vect.vocabulary_:
                    return model.coef_[label_encoder.transform(label),
                                       dict_vect.vocabulary_[feat_str]]
                else:
                    return 0

            if print_features:
                assert model and dict_vect and label_encoder
                for feat_name in features[0].keys():
                    row = [feat_name]
                    for token in features:
                        feat_value = token.get(feat_name, '\\')
                        true_label_weight = get_feature_weight(
                            target_true_label,
                            feat_name,
                            token.get(feat_name, None)
                        )
                        pred_label_weight = get_feature_weight(
                            target_pred_label,
                            feat_name,
                            token.get(feat_name, None)
                        )
                        row.append(u"{}({:+.2f}/{:+.2f})".format(
                            feat_value, true_label_weight,
                            pred_label_weight))

                    data.append(row)

            print tabulate(data)
