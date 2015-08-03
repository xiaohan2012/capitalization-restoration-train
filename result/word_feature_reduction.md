## Richer features

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

## Poorer word features

Removed features:

```
lexical_features = [ 
    (('word',  1), ),
    (('word',  -1), ),
    (('word',  0), ('word',  1)),
]

pos_features = [
    (('pos-tag',  1), ),
    (('pos-tag',  -1), ),
    (('pos-tag',  0), ('pos-tag',  1)),
    (('pos-tag-lower',  0), ),
]
```

Features that are removed are commented out above.

Subset accuracy: 94.62

             precision    recall  f1-score   support

         AL     0.9455    0.9776    0.9613     37955
         AN     0.9831    0.9972    0.9901      5674
         AU     0.9932    1.0000    0.9966      2643
         IC     0.9243    0.8556    0.8886     13889
         MX     0.8843    0.5220    0.6565       864

avg / total     0.9454    0.9462    0.9446     61025

Precision/Recall/F1(macro) : 0.9461  0.8705  0.8986

Precision/Recall/F1(micro) : 0.9462  0.9462  0.9462




## Conclusion

Richer lexical features help. But *which* help?
