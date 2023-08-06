from simple_converge.tf_optimizers.SgdOptimizer import SgdOptimizer
from simple_converge.tf_optimizers import AdamOptimizer

optimizers_collection = {

    "sgd_optimizer": SgdOptimizer,
    "adam_optimizer": AdamOptimizer
}