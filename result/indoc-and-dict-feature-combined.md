# Before

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

# After adding

```
(('indoccap', 0), ('lower-in-dict', 0)),
(('indoccap', 0), ('upper-in-dict', 0)),
(('indoccap', 0), ('cap-in-dict', 0))
```


Subset accuracy: 95.14

             precision    recall  f1-score   support

         AL     0.9514    0.9794    0.9652     37955
         AN     0.9855    0.9956    0.9905      5674
         AU     0.9936    0.9996    0.9966      2643
         IC     0.9303    0.8705    0.8994     13889
         MX     0.8883    0.5799    0.7017       864

avg / total     0.9507    0.9514    0.9502     61025

Precision/Recall/F1(macro) : 0.9498  0.8850  0.9107

Precision/Recall/F1(micro) : 0.9514  0.9514  0.9514

# Conclusion

Improved a little overall.

Most significant for `MX`. Then `IC`.
