from simple_converge.tf_regularizers import L1Regularizer
from simple_converge.tf_regularizers import L2Regularizer
from simple_converge.tf_regularizers import L1L2Regularizer

regularizers_collection = {

    "l1_regularizer": L1Regularizer,
    "l2_regularizer": L2Regularizer,
    "l1_l2_regularizer": L1L2Regularizer
}
