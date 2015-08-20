import numpy as np
import pandas as pds

input = np.asarray([[(17986, 18491, 19016),
                     (62242, 63297, 62770),
                     (1024, 1024, 1027),
                     (9239, 9240, 9239),
                     (3656, 3680, 3680)],
                    [(17751, 18268, 18759),
                     (63029, 64066, 63599),
                     (951, 951, 953),
                     (9178, 9179, 9178),
                     (3697, 3750, 3725)],
                    [(17751, 18268, 18759),
                     (63029, 64066, 63599),
                     (951, 951, 953),
                     (9178, 9179, 9178),
                     (3697, 3750, 3725)],
                    [(17867, 18435, 18982),
                     (62200, 63355, 62804),
                     (1026, 1026, 1030),
                     (9375, 9375, 9375),
                     (3673, 3709, 3709)],
                    [(17722, 18222, 18716),
                     (62638, 63669, 63176),
                     (1026, 1026, 1030),
                     (9121, 9121, 9124),
                     (3681, 3722, 3714)],
                    [(17918, 18454, 18914),
                     (62759, 63776, 63330),
                     (962, 962, 963),
                     (8976, 8976, 8976),
                     (3672, 3707, 3692)],
                    [(18050, 18548, 19053),
                     (62528, 63555, 63054),
                     (979, 979, 981),
                     (9478, 9479, 9478),
                     (3795, 3822, 3817)],
                    [(17846, 18333, 18857),
                     (62508, 63546, 63028),
                     (1038, 1038, 1041),
                     (9104, 9105, 9104),
                     (3629, 3663, 3655)],
                    [(18017, 18606, 19080),
                     (62464, 63563, 63077),
                     (996, 996, 997),
                     (9295, 9295, 9295),
                     (3654, 3681, 3692)],
                    [(17782, 18302, 18786),
                     (62794, 63830, 63348),
                     (1012, 1012, 1012),
                     (9262, 9262, 9262),
                     (3717, 3751, 3749)]],
                   dtype=np.float64)

# precision, recall and f1 for each
prf1 = np.zeros(input.shape, dtype=np.float64)

n_exper, n_label, _ = input.shape
for i in xrange(n_exper):
    # precision
    prf1[i, :, 0] = input[i, :, 0] / input[i, :, 1]

    # recall
    prf1[i, :, 1] = input[i, :, 0] / input[i, :, 2]
    
    # f1
    prf1[i, :, 2] = (2 * prf1[i, :, 0] * prf1[i, :, 1] /
                           (prf1[i, :, 0] + prf1[i, :, 1]))

def make_2d_df(data, index):
    return pds.DataFrame(data, columns=["precision", "recall", "f1"],
                         index=index)

def make_1d_df(data, name):
    return pds.DataFrame(data,
                         columns=["precision", "recall", "f1"])


prf1_mean = prf1.mean(axis=0)
print("Label-wise average:")
print("precision/recall/f1")
print(make_2d_df(prf1_mean*100, index=['IC', 'AL' ,'MX', 'AN', 'AU']))

# macro
print("Average macro-average:")
print("precision/recall/f1")
print(prf1.mean(axis=1).mean(axis=0)[None, :])


# micro
micro_prf1 = np.zeros((n_exper, 3))
micro_input = input.sum(axis=1)
micro_prf1[:, 0] = micro_input[:, 0] / micro_input[:, 1]
micro_prf1[:, 1] = micro_input[:, 0] / micro_input[:, 2]
micro_prf1[:, 2] = (2 * micro_prf1[:, 0] * micro_prf1[:, 1] / 
                    (micro_prf1[:, 0] + micro_prf1[:, 1]))

print("Average micro-average:")
print("precision/recall/f1")
print(micro_prf1.mean(axis=0))

# item accuracy
print("Average item accuracy:")
print(np.mean(micro_input[:, 0] / micro_input[:, 2]))

print(make_2d_df([prf1.mean(axis=1).mean(axis=0),
                  micro_prf1.mean(axis=0)],
                 index=['micro-average', 'macro-average']))
