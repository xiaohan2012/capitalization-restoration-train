import numpy as np
import pandas as pds


def main(input, labels=['AL', 'IC']):
    """
    Return:
    - Label-wise average
    - Average item accuracy
    - micro/macro  average
    """
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
    label_wise_avg = make_2d_df(prf1_mean*100, index=labels)
    
    # micro
    micro_prf1 = np.zeros((n_exper, 3))
    micro_input = input.sum(axis=1)
    micro_prf1[:, 0] = micro_input[:, 0] / micro_input[:, 1]
    micro_prf1[:, 1] = micro_input[:, 0] / micro_input[:, 2]
    micro_prf1[:, 2] = (2 * micro_prf1[:, 0] * micro_prf1[:, 1] /
                        (micro_prf1[:, 0] + micro_prf1[:, 1]))

    avg_item_acc = np.mean(micro_input[:, 0] / micro_input[:, 2])

    m_avg = make_2d_df([prf1.mean(axis=1).mean(axis=0),
                        micro_prf1.mean(axis=0)],
                       index=['micro-average', 'macro-average'])
    
    return label_wise_avg, avg_item_acc * 100, m_avg * 100


def calc_and_print(input, labels):
    label_wise_avg, avg_item_acc, m_avg = main(input, labels)

    print("Label-wise average:")
    print(label_wise_avg)
    
    print('')
    print("Average item accuracy:")
    print(avg_item_acc)

    print('')
    print(m_avg)


if __name__ == '__main__':
    input = np.asarray([[(97578, 99672, 98268),
                         (16014, 16704, 18108)],
                        [(96629, 98651, 97323),
                         (16122, 16816, 18144)],
                        [(96874, 98869, 97558),
                         (16172, 16856, 18167)],
                        [(97035, 99096, 97743),
                         (15995, 16703, 18056)],
                        [(97788, 99692, 98499),
                         (16115, 16826, 18019)],
                        [(96769, 98776, 97506),
                         (16236, 16973, 18243)],
                        [(97720, 99764, 98383),
                         (15820, 16483, 17864)],
                        [(97653, 99824, 98349),
                         (16164, 16860, 18335)],
                        [(97259, 99228, 97922),
                         (16188, 16851, 18157)],
                        [(96936, 98997, 97710),
                         (16060, 16834, 18121)]],
                       dtype=np.float64)
    calc_and_print(input, ['AL', 'IC'])
