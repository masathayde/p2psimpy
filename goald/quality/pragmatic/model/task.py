from goald.quality.pragmatic.model.refinement import Refinement
from goald.quality.pragmatic.model.plan import Plan


class Task(Refinement):
    def __init__(self, metric=None, contextValueMap=None, lessIsMore=False):
        Refinement.__init__(self)
        self.providedQualityLevels = {}
        self.lessIsMore = lessIsMore

        if contextValueMap and metric:
            self.providedQualityLevels[metric] = contextValueMap

    def myType(self):
        return Refinement().TASK

    def setProvidedQuality(self, context, metric, value):
        map = {}

        if metric in self.providedQualityLevels:
            map = self.providedQualityLevels[metric]
            map[context] = value
            self.providedQualityLevels[metric] = map
        else:
            map[context] = value
            self.providedQualityLevels[metric] = map

    def myProvidedQuality(self, metric, contextSet):
        myQuality = 0
        set = False

        if metric in self.providedQualityLevels:
            QLContexts = self.providedQualityLevels[metric].keys()
            for c in QLContexts:
                if 'None' == c.label:
                    myQuality = self.providedQualityLevels[metric][context]
                    set = True

        for current in contextSet:
            if metric in self.providedQualityLevels:
                if not set:
                    myQuality = self.providedQualityLevels[metric][current]
                    set = True
                else:
                    if metric.getLessIsBetter():
                        if(myQuality > self.providedQualityLevels[metric][current]):
                            myQuality = self.providedQualityLevels[metric][current]
                    elif(myQuality < self.providedQualityLevels[metric][current]):
                        myQuality = self.providedQualityLevels[metric][current]

        return myQuality

    def abidesByInterpretation(self, interp, current):
        feasible = True
        if interp is None:
            return True

        interp.getQualityConstraints(current)

        for qc in interp.getQualityConstraints(current):
            try:
                if not qc.abidesByQC(self.myProvidedQuality(qc.metric, current), qc.metric):
                    feasible = False
            except:
                print("MetricNotFoundException Metric: ", qc.metric)
                raise

        if interp.getQualityConstraints(None) is not None:
            for qc in interp.getQualityConstraints(None):
                try:
                    if not qc.abidesByQC(self.myProvidedQuality(qc.getMetric(),current), qc.getMetric()):
                        feasible = False
                except:
                    print("MetricNotFoundException")
                    raise

        return feasible

    def isAchievable(self, current, interp):
        if not self.isApplicable(current):
            return None
        if self.abidesByInterpretation(interp, current):
            return Plan(self)
        else:
            return None
