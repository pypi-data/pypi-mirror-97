__author__ = "hugo.inzirillo"

from dataclasses import dataclass


@dataclass(init=True)
class ArchTestResult:
    lm_stat: float
    lm_pval: float
    f_stat: float
    f_pval: float

    @property
    def arch_effect(self):
        return self.f_pval <= 0.05
