import numpy as np
from numpy.testing import assert_array_almost_equal

from capitalization_train.calc_cv_result import calc


def test_calc_2d():
    inp = np.asarray([[125413., 140884., 145074.],
                      [704291., 723952., 719762.]])
    act_label_wise, act_item_acc, act_m_avg \
        = calc(inp, labels=['AL', 'IC'])
    al_prec, al_rec = inp[0, 0] / inp[0, 1], inp[0, 0] / inp[0, 2]
    al_f1 = 2 * al_prec * al_rec / (al_prec + al_rec)
    
    ic_prec, ic_rec = inp[1, 0] / inp[1, 1], inp[1, 0] / inp[1, 2]
    ic_f1 = 2 * ic_prec * ic_rec / (ic_prec + ic_rec)
    
    match_total, model_total, ref_total = inp.sum(axis=0)
    
    micro_prec, micro_rec = match_total / model_total, match_total / ref_total
    micro_f1 = 2 * micro_prec * micro_rec / (micro_prec + micro_rec)
    
    exp_label_wise = np.asarray([[al_prec, al_rec, al_f1],
                                 [ic_prec, ic_rec, ic_f1]])
    exp_item_acc = match_total / ref_total

    exp_m_avg = np.asarray([[micro_prec, micro_rec, micro_f1],
                            [np.mean([al_prec, ic_prec]),
                             np.mean([al_rec, ic_rec]),
                             np.mean([al_f1, ic_f1])]])
    
    assert_array_almost_equal(act_label_wise, exp_label_wise)
    assert_array_almost_equal(act_item_acc, exp_item_acc)
    assert_array_almost_equal(act_m_avg, exp_m_avg)
    

def test_calc_3d():
    pass
    
