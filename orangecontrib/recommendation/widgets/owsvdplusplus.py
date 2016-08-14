from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication

from Orange.data import Table
from Orange.widgets import settings
from Orange.widgets import gui
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner

from orangecontrib.recommendation import SVDPlusPlusLearner
from orangecontrib.recommendation.utils.sgd_optimizer import *


class OWSVDPlusPlus(OWBaseLearner):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "SVD++"
    description = 'Matrix factorization model which makes use of implicit ' \
                  'feedback information'
    icon = "icons/svdplusplus.svg"
    priority = 80

    LEARNER = SVDPlusPlusLearner

    inputs = [("Feedback information", Table, "set_feedback")]

    outputs = [("P", Table),
               ("Q", Table),
               ("Y", Table)]

    num_factors = settings.Setting(5)
    num_iter = settings.Setting(25)
    learning_rate = settings.Setting(0.005)
    bias_learning_rate = settings.Setting(0.005)
    lmbda = settings.Setting(0.02)
    bias_lmbda = settings.Setting(0.02)
    feedback = None

    # SGD optimizers
    sgd, momentum, nag, adagrad, rmsprop, adadelta, adam = range(7)
    opt_type = settings.Setting(sgd)
    opt_names = ['SGD', 'Momentum', "Nesterov's AG",
                 'AdaGrad', 'RMSprop', 'AdaDelta', 'Adam']
    momentum = settings.Setting(0.9)
    rho = settings.Setting(0.9)
    beta1 = settings.Setting(0.9)
    beta2 = settings.Setting(0.999)

    def add_main_layout(self):
        # hbox = gui.hBox(self.controlArea, "Settings")

        # Frist groupbox (Common parameters)
        box = gui.widgetBox(self.controlArea, "Parameters")
        self.base_estimator = SVDPlusPlusLearner()

        gui.spin(box, self, "num_factors", 1, 10000,
                 label="Number of latent factors:",
                 alignment=Qt.AlignRight, callback=self.settings_changed)

        gui.spin(box, self, "num_iter", 1, 10000,
                 label="Number of iterations:",
                 alignment=Qt.AlignRight, callback=self.settings_changed)

        gui.doubleSpin(box, self, "learning_rate", minv=1e-5, maxv=1e+5,
                       step=1e-5, label="Learning rate:", decimals=5,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "bias_learning_rate", minv=1e-5, maxv=1e+5,
                       step=1e-5, label="Bias learning rate:", decimals=5,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "lmbda", minv=1e-4, maxv=1e+4, step=1e-4,
                       label="Regularization:", decimals=4,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        gui.doubleSpin(box, self, "bias_lmbda", minv=1e-4, maxv=1e+4, step=1e-4,
                       label="Bias regularization:", decimals=4,
                       alignment=Qt.AlignRight, controlWidth=90,
                       callback=self.settings_changed)

        # Second groupbox (SGD optimizers)
        box = gui.widgetBox(self.controlArea, "SGD optimizers")

        gui.comboBox(box, self, "opt_type", label="SGD optimizer: ",
            items=self.opt_names, orientation=Qt.Horizontal,
            addSpace=4, callback=self._opt_changed)

        _m_comp = gui.doubleSpin(box, self, "momentum", minv=1e-4, maxv=1e+4,
                                 step=1e-4, label="Momentum:", decimals=4,
                                 alignment=Qt.AlignRight, controlWidth=90,
                                 callback=self.settings_changed)

        _r_comp = gui.doubleSpin(box, self, "rho", minv=1e-4, maxv=1e+4,
                                 step=1e-4, label="Rho:", decimals=4,
                                 alignment=Qt.AlignRight, controlWidth=90,
                                 callback=self.settings_changed)

        _b1_comp = gui.doubleSpin(box, self, "beta1", minv=1e-5, maxv=1e+5,
                                  step=1e-4, label="Beta 1:", decimals=5,
                                  alignment=Qt.AlignRight, controlWidth=90,
                                  callback=self.settings_changed)

        _b2_comp = gui.doubleSpin(box, self, "beta2", minv=1e-5, maxv=1e+5,
                                  step=1e-4, label="Beta 2:", decimals=5,
                                  alignment=Qt.AlignRight, controlWidth=90,
                                  callback=self.settings_changed)
        gui.rubber(box)
        self._opt_params = [_m_comp, _r_comp, _b1_comp, _b2_comp]
        self._show_right_optimizer()

    def _show_right_optimizer(self):
        enabled = [[False, False, False, False],  # SGD
                   [True, False, False, False],  # Momentum
                   [True, False, False, False],  # NAG
                   [False, False, False, False],  # AdaGrad
                   [False, True, False, False],  # RMSprop
                   [False, True, False, False],  # AdaDelta
                   [False, False, True, True],  # Adam
                ]

        mask = enabled[self.opt_type]
        for spin, enabled in zip(self._opt_params, mask):
            [spin.box.hide, spin.box.show][enabled]()

    def _opt_changed(self):
        self._show_right_optimizer()
        self.settings_changed()

    def select_optimizer(self):
        if self.opt_type == self.momentum:
            return Momentum(self.momentum)
        elif self.opt_type == self.nag:
            return NesterovMomentum(self.momentum)
        elif self.opt_type == self.adagrad:
            return AdaGrad()
        elif self.opt_type == self.rmsprop:
            return RMSProp(self.rho)
        elif self.opt_type == self.adadelta:
            return AdaDelta(self.rho)
        elif self.opt_type == self.adam:
            return Adam(beta1=self.beta1, beta2=self.beta2)
        else:
            return SGD()

    def create_learner(self):
        return self.LEARNER(
            num_factors=self.num_factors,
            num_iter=self.num_iter,
            learning_rate=self.learning_rate,
            bias_learning_rate=self.bias_learning_rate,
            lmbda=self.lmbda,
            bias_lmbda=self.bias_lmbda,
            feedback=self.feedback,
            optimizer=self.select_optimizer()
        )

    def get_learner_parameters(self):
        return (("Number of latent factors", self.num_factors),
                ("Number of iterations", self.num_iter),
                ("Learning rate", self.learning_rate),
                ("Bias learning rate", self.bias_learning_rate),
                ("Regularization", self.lmbda),
                ("Bias regularization", self.bias_lmbda),
                ("SGD optimizer", self.opt_names[self.opt_type]))

    def update_model(self):
        super().update_model()

        P = None
        Q = None
        Y = None
        if self.valid_data:
            P = self.model.getPTable()
            Q = self.model.getQTable()
            Y = self.model.getYTable()

        self.send("P", P)
        self.send("Q", Q)
        self.send("Y", Y)

    def set_feedback(self, feedback):
        self.feedback = feedback
        self.update_learner()

if __name__ == '__main__':
    app = QApplication([])
    widget = OWSVDPlusPlus()
    widget.show()
    app.exec()