# Import pyomo module
from pyomo.environ import ConcreteModel, Set, Var, Objective, minimize, Constraint, log
from pyomo.opt import SolverFactory, SolverManagerFactory
from pyomo.core.expr.numvalue import NumericValue
import numpy as np
import pandas as pd
from ..constant import CET_ADDI, CET_MULT, FUN_PROD, FUN_COST, RTS_CRS, RTS_VRS, OPT_LOCAL
from .tools import set_neos_email


class CQRG1:
    """initial Group-VC-added CQR (CQR+G) model"""

    def __init__(self, y, x, tau, Cutactive, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
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

        # TODO(error/warning handling): Check the configuration of the model exist
        self.x = x
        self.y = y
        self.tau = tau
        self.cet = cet
        self.fun = fun
        self.rts = rts

        if type(self.x[0]) != list:
            self.x = []
            for x_value in x.tolist():
                self.x.append([x_value])

        self.Cutactive = Cutactive

        # Initialize the CNLS model
        self.__model__ = ConcreteModel()

        # Initialize the sets
        self.__model__.I = Set(initialize=range(len(self.y)))
        self.__model__.J = Set(initialize=range(len(self.x[0])))

        # Initialize the variables
        self.__model__.alpha = Var(self.__model__.I, doc='alpha')
        self.__model__.beta = Var(self.__model__.I,
                                  self.__model__.J,
                                  bounds=(0.0, None),
                                  doc='beta')
        self.__model__.epsilon = Var(self.__model__.I, doc='residual')
        self.__model__.epsilon_plus = Var(
            self.__model__.I, bounds=(0.0, None), doc='positive error term')
        self.__model__.epsilon_minus = Var(
            self.__model__.I, bounds=(0.0, None), doc='negative error term')
        self.__model__.frontier = Var(self.__model__.I,
                                      bounds=(0.0, None),
                                      doc='estimated frontier')

        # Setup the objective function and constraints
        self.__model__.objective = Objective(rule=self.__objective_rule(),
                                             sense=minimize,
                                             doc='objective function')
        self.__model__.error_decomposition = Constraint(self.__model__.I,
                                                        rule=self.__error_decomposition(),
                                                        doc='decompose error term')
        self.__model__.regression_rule = Constraint(self.__model__.I,
                                                    rule=self.__regression_rule(),
                                                    doc='regression equation')
        if self.cet == CET_MULT:
            self.__model__.log_rule = Constraint(self.__model__.I,
                                                 rule=self.__log_rule(),
                                                 doc='log-transformed regression equation')
        self.__model__.afriat_rule = Constraint(self.__model__.I,
                                                rule=self.__afriat_rule(),
                                                doc='elementary Afriat approach')
        self.__model__.sweet_rule = Constraint(self.__model__.I,
                                               self.__model__.I,
                                               rule=self.__sweet_rule(),
                                               doc='sweet spot approach')

        # Optimize model
        self.optimization_status = 0
        self.problem_status = 0

    def optimize(self, email=OPT_LOCAL):
        """Optimize the function by requested method"""
        # TODO(error/warning handling): Check problem status after optimization
        if remote == False:
            if self.cet == CET_ADDI:
                solver = SolverFactory("mosek")
                self.problem_status = solver.solve(self.__model__, tee=True)
                self.optimization_status = 1

            elif self.cet == CET_MULT:
                # TODO(warning handling): Use log system instead of print()
                print(
                    "Estimating the multiplicative model will be available in near future."
                )
                return False
        else:
            if self.cet == CET_ADDI:
                opt = "mosek"

            elif self.cet == CET_MULT:
                opt = "knitro"

            solver = SolverManagerFactory('neos')
            self.problem_status = solver.solve(self.__model__,
                                               tee=True,
                                               opt=opt)
            self.optimization_status = 1

    def __objective_rule(self):
        """Return the proper objective function"""

        def objective_rule(model):
            return self.tau * sum(model.epsilon_plus[i] for i in model.I) \
                + (1 - self.tau) * sum(model.epsilon_minus[i] for i in model.I)

        return objective_rule

    def __error_decomposition(self):
        """Return the constraint decomposing error to positive and negative terms"""

        def error_decompose_rule(model, i):
            return model.epsilon[i] == model.epsilon_plus[i] - model.epsilon_minus[i]

        return error_decompose_rule

    def __regression_rule(self):
        """Return the proper regression constraint"""
        if self.cet == CET_ADDI:
            if self.rts == RTS_VRS:
                def regression_rule(model, i):
                    return self.y[i] == model.alpha[i] \
                        + sum(model.beta[i, j] * self.x[i][j] for j in model.J) \
                        + model.epsilon[i]

                return regression_rule
            elif self.rts == RTS_CRS:
                # TODO(warning handling): replace with model requested not exist
                return False

        elif self.cet == CET_MULT:

            def regression_rule(model, i):
                return log(
                    self.y[i]) == log(model.frontier[i] + 1) + model.epsilon[i]

            return regression_rule

        # TODO(error handling): replace with undefined model attribute
        return False

    def __log_rule(self):
        """Return the proper log constraint"""
        if self.cet == CET_MULT:
            if self.rts == RTS_VRS:

                def log_rule(model, i):
                    return model.frontier[i] == model.alpha[i] + sum(
                        model.beta[i, j] * self.x[i][j] for j in model.J) - 1

                return log_rule
            elif self.rts == RTS_CRS:

                def log_rule(model, i):
                    return model.frontier[i] == sum(
                        model.beta[i, j] * self.x[i][j] for j in model.J) - 1

                return log_rule

        # TODO(error handling): replace with undefined model attribute
        return False

    def __afriat_rule(self):
        """Return the proper elementary Afriat approach constraint"""
        if self.fun == FUN_PROD:
            __operator = NumericValue.__le__
        elif self.fun == FUN_COST:
            __operator = NumericValue.__ge__

        if self.cet == CET_ADDI:
            if self.rts == RTS_VRS:

                def afriat_rule(model, i):
                    return __operator(
                        model.alpha[i] + sum(model.beta[i, j] * self.x[i][j]
                                             for j in model.J),
                        model.alpha[self.__model__.I.nextw(i)] +
                        sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j]
                            for j in model.J))

                return afriat_rule
            elif self.rts == RTS_CRS:
                # TODO(warning handling): replace with model requested not exist
                return False
        elif self.cet == CET_MULT:
            if self.rts == RTS_VRS:

                def afriat_rule(model, i):
                    return __operator(
                        model.alpha[i] + sum(model.beta[i, j] * self.x[i][j]
                                             for j in model.J),
                        model.alpha[self.__model__.I.nextw(i)] +
                        sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j]
                            for j in model.J))

                return afriat_rule
            elif self.rts == RTS_CRS:

                def afriat_rule(model, i):
                    return __operator(
                        sum(model.beta[i, j] * self.x[i][j] for j in model.J),
                        sum(model.beta[self.__model__.I.nextw(i), j] * self.x[i][j] for j in model.J))

                return afriat_rule

        # TODO(error handling): replace with undefined model attribute
        return False

    def __sweet_rule(self, ):
        """Return the proper sweet spot approach constraint"""
        if self.fun == FUN_PROD:
            __operator = NumericValue.__le__
        elif self.fun == FUN_COST:
            __operator = NumericValue.__ge__

        if self.cet == CET_ADDI:
            if self.rts == RTS_VRS:

                def sweet_rule(model, i, h):
                    if self.Cutactive[i, h]:
                        if i == h:
                            return Constraint.Skip
                        return __operator(model.alpha[i] + sum(model.beta[i, j] * self.x[i][j]
                                                               for j in model.J),
                                          model.alpha[h] + sum(model.beta[h, j] * self.x[i][j]
                                                               for j in model.J))
                    return Constraint.Skip

                return sweet_rule
            elif self.rts == RTS_CRS:
                # TODO(warning handling): replace with model requested not exist
                return False
        elif self.cet == CET_MULT:
            if self.rts == RTS_VRS:

                def sweet_rule(model, i, h):
                    if self.Cutactive[i, h]:
                        if i == h:
                            return Constraint.Skip
                        return __operator(model.alpha[i] + sum(model.beta[i, j] * self.x[i][j]
                                                               for j in model.J),
                                          model.alpha[h] + sum(model.beta[h, j] * self.x[i][j]
                                                               for j in model.J))
                    return Constraint.Skip

                return sweet_rule
            elif self.rts == RTS_CRS:

                def sweet_rule(model, i, h):
                    if self.Cutactive[i, h]:
                        if i == h:
                            return Constraint.Skip
                        return __operator(sum(model.beta[i, j] * self.x[i][j] for j in model.J),
                                          sum(model.beta[h, j] * self.x[i][j] for j in model.J))
                    return Constraint.Skip

                return sweet_rule

        # TODO(error handling): replace with undefined model attribute
        return False

    def get_alpha(self):
        """Return alpha value by array"""
        if self.optimization_status == 0:
            self.optimize()
        alpha = list(self.__model__.alpha[:].value)
        return np.asarray(alpha)

    def get_beta(self):
        """Return beta value by array"""
        if self.optimization_status == 0:
            self.optimize()
        beta = np.asarray([i + tuple([j]) for i, j in zip(list(self.__model__.beta),
                                                          list(self.__model__.beta[:, :].value))])
        beta = pd.DataFrame(beta, columns=['Name', 'Key', 'Value'])
        beta = beta.pivot(index='Name', columns='Key', values='Value')
        return beta.to_numpy()


class CERG1(CQRG1):
    """Convex expectile regression (CER)"""

    def __init__(self, y, x, tau, Cutactive, cet=CET_ADDI, fun=FUN_PROD, rts=RTS_VRS):
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
        super().__init__(y, x, tau, Cutactive, cet, fun, rts)
        self.__model__.objective.deactivate()
        self.__model__.squared_objective = Objective(
            rule=self.__squared_objective_rule(), sense=minimize, doc='squared objective rule')

    def __squared_objective_rule(self):
        def squared_objective_rule(model):
            return self.tau * sum(model.epsilon_plus[i] ** 2 for i in model.I) \
                + (1 - self.tau) * \
                sum(model.epsilon_minus[i] ** 2 for i in model.I)

        return squared_objective_rule
