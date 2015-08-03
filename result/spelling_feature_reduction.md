# With spelling features

```
Subset accuracy: 95.18

             precision    recall  f1-score   support

         AL     0.9515    0.9803    0.9656     37955
         AN     0.9888    0.9984    0.9936      5674
         AU     0.9966    1.0000    0.9983      2643
         IC     0.9296    0.8705    0.8991     13889
         MX     0.9007    0.5567    0.6881       864

```

avg / total     0.9512    0.9518    0.9506     61025

Precision/Recall/F1(macro) : 0.9534  0.8812  0.9089

Precision/Recall/F1(micro) : 0.9518  0.9518  0.9518

# Without 1 'begins-with-alphabetic'

Subset accuracy: 95.10

             precision    recall  f1-score   support

         AL     0.9515    0.9791    0.9651     37955
         AN     0.9857    0.9958    0.9907      5674
         AU     0.9936    0.9996    0.9966      2643
         IC     0.9293    0.8703    0.8988     13889
         MX     0.8704    0.5752    0.6927       864

avg / total     0.9503    0.9510    0.9499     61025

Precision/Recall/F1(macro) : 0.9461  0.8840  0.9088

Precision/Recall/F1(micro) : 0.9510  0.9510  0.9510


# Without 2 spelling features

The following are removed as we observe unreasonablly large weight for them on the trained model:

```
spelling_features = [
    (('all-letter-uppercase', 0), ),
    (('begins-with-alphabetic', 0), ),
 ]


```

Evaluation summary:
Subset accuracy: 94.11

             precision    recall  f1-score   support

         AL     0.9476    0.9801    0.9636     37955
         AN     0.9830    0.9963    0.9896      5674
         AU     0.9653    0.7688    0.8559      2643
         IC     0.9047    0.8664    0.8851     13889
         MX     0.8401    0.5961    0.6974       864

avg / total     0.9404    0.9411    0.9397     61025

Precision/Recall/F1(macro) : 0.9281  0.8415  0.8783

Precision/Recall/F1(micro) : 0.9411  0.9411  0.9411


# Conclusion

all-letter-uppsercase helps significantly, while the other not so obvious.

