# Features

```
lexical_features = [ 
    (('word',  1), ),
    (('word',  -1), ),
    (('word',  0), ),
    (('word', -1), ('word',  0)),
    (('word',  0), ('word',  1)),
]

positional_features = [
    (('is-leading-word', 0), ),
]

dict_features = [
    (('lower-in-dict', 0), ),
    (('upper-in-dict', 0), ),
    (('cap-in-dict', 0), ),
    (('orig-in-dict', 0), ),
]

pos_features = [
    (('pos-tag',  1), ),
    (('pos-tag',  -1), ),
    (('pos-tag',  0), ),
    (('pos-tag', -1), ('pos-tag',  0)),
    (('pos-tag',  0), ('pos-tag',  1)),
    (('pos-tag-lower',  0), ),
    (('pos-tag-lower',  -1), ),
    (('pos-tag-lower',  -1), ('pos-tag-lower',  0)),
]

spelling_features = [
    (('all-letter-uppercase', 0), ),
    # (('begins-with-alphabetic', 0), ),
    (('has-punct', 0), )
]

document_features = [(('indoccap', 0), ),
                     (('indoclower', 0), ),
                     (('indoccap', 0), ('lower-in-dict', 0)),
                     (('indoccap', 0), ('upper-in-dict', 0)),
                     (('indoccap', 0), ('cap-in-dict', 0))
]

```

removed `begins-with-alphabetic`
added: `pos-tag-lower` and `indoccap`+`in-doct` features

# Before

Subset accuracy: 95.18

             precision    recall  f1-score   support

         AL     0.9515    0.9803    0.9656     37955
         AN     0.9888    0.9984    0.9936      5674
         AU     0.9966    1.0000    0.9983      2643
         IC     0.9296    0.8705    0.8991     13889
         MX     0.9007    0.5567    0.6881       864

avg / total     0.9512    0.9518    0.9506     61025

Precision/Recall/F1(macro) : 0.9534  0.8812  0.9089

Precision/Recall/F1(micro) : 0.9518  0.9518  0.9518


# After


Subset accuracy: 95.18

             precision    recall  f1-score   support

         AL     0.9511    0.9799    0.9653     37955
         AN     0.9880    0.9979    0.9929      5674
         AU     0.9955    0.9996    0.9975      2643
         IC     0.9311    0.8697    0.8993     13889
         MX     0.9027    0.5903    0.7138       864

avg / total     0.9512    0.9518    0.9507     61025

Precision/Recall/F1(macro) : 0.9537  0.8875  0.9138

Precision/Recall/F1(micro) : 0.9518  0.9518  0.9518

**What?**

