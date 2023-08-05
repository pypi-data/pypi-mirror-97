# Import CNLS as parent class
from . import CQER, ICNLS
from pyomo.environ import Constraint
from pyomo.core.expr.numvalue import NumericValue
import numpy as np
from .constant import CET_ADDI, CET_MULT, FUN_PROD, FUN_COST, RTS_CRS, RTS_VRS


class ICQR(ICNLS.ICNLS, CQER.CQR):
    """Isotonic convex quantile regression (ICQR)"""

    def __init__(self, y, x, tau, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
        """
            y : Output variable
            x : Input variables
            tau : quantile
            cet  = CET_ADDI : Additive composite error term
                 = CET_MULT : Multiplicative composite error term
            fun  = FUN_PROD : Production frontier
                 = FUN_COST : Cost frontier
            rts  = RTS_VRS  : Variable returns to scale
                 = RTS_CRS  : Constant returns to scale
        """
        CQER.CQR.__init__(self, y, x, tau, cet, fun, rts)

        self._ICNLS__pmatrix = self._ICNLS__binaryMatrix()
        self.__model__.afriat_rule.deactivate()
        self.__model__.isotonic_afriat_rule = Constraint(self.__model__.I,
                                                         self.__model__.I,
                                                         rule=self._ICNLS__isotonic_afriat_rule(),
                                                         doc='isotonic afriat inequality')


class ICER(ICNLS.ICNLS, CQER.CER):
    """Isotonic convex expectile regression (ICER)"""

    def __init__(self, y, x, tau, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
        """
            y : Output variable
            x : Input variables
            tau : expectile
            cet  = CET_ADDI : Additive composite error term
                 = CET_MULT : Multiplicative composite error term
            fun  = FUN_PROD : Production frontier
                 = FUN_COST : Cost frontier
            rts  = RTS_VRS  : Variable returns to scale
                 = RTS_CRS  : Constant returns to scale
        """
        CQER.CER.__init__(self, y, x, tau, cet, fun, rts)

        self._ICNLS__pmatrix = self._ICNLS__binaryMatrix()
        self.__model__.afriat_rule.deactivate()
        self.__model__.isotonic_afriat_rule = Constraint(self.__model__.I,
                                                         self.__model__.I,
                                                         rule=self._ICNLS__isotonic_afriat_rule(),
                                                         doc='isotonic afriat inequality')
