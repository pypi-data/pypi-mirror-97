import inspect
import linecache
import re
import sys
import weakref

from CleverSheep.Test.Tester import Coordinator
from CleverSheep.Test.Tester import log
from CleverSheep.Test.Tester import options

rProcCall = re.compile(r' *(?P<name>[a-zA-Z0-9_.]+)\(')
rFuncCall = re.compile(r'[^=]*= *(?P<name>[a-zA-Z0-9_.]+)\(')
rStepComment = re.compile(r'^ *# ?> (.*)')
rComment = re.compile(r'^ *#(.*)')


def getFuncClassID(func):
    this = getattr(func, "__self__", None)
    if this is None:
        funcClass = getattr(func, "im_class", None)
    else:
        funcClass = getattr(this, "__class__", None)
    if funcClass is None:
        return None, 0
    return funcClass, id(funcClass)


#{ Public
class TestSpecDB(object):
    def __init__(self):
        self._callMap = {}
        self._stepMap = {}

    def gatherTestSteps(self, func):
        f = TestMap.getTestMap(func)
        if f is not None:
            self.getMap(f)

    def getThing(self, func):
        try:
            func = func.func
        except AttributeError:
            pass
        _, classID = getFuncClassID(func)

        # If this is a test function it should be in a Suite but if it is not
        # we need to just use the function as the key
        try:
            result = self._callMap[(func.__code__, classID)]
        except KeyError:
            result = self._callMap[func.__code__]

        return result

    def getMap(self, point):
        func = point.func
        key = func.__code__, id(getattr(func, "__class__", None))
        callMap = {key: point,
                   func.__code__: point}
        stepMap = {}
        for level, point, boundArgs in point.walk():
            if point.type == "func":
                func = point.func
                key = func.__code__, id(getattr(func, "__class__", None))
                callMap[key] = point
                callMap[func.__code__] = point
            elif point.type == "step":
                func = point.funcPoint.func
                stepPoint = point.stepPoint
                stepMap[(func.__code__, stepPoint.lNum)] = stepPoint

        self._callMap.update(callMap)
        self._stepMap.update(stepMap)

    def dump(self, func):
        for level, p in func.walk():
            pad = "  " * level
            if p.type == "step":
                lines = str(p).splitlines()
                for i, line in enumerate(lines):
                    print("%s%s" % (pad, line))

    def runAndTrace(self, func, *args, **kwargs):
        runTracer = RunTracer(self._callMap, self._stepMap)
        runTracer.run(func, args, kwargs)
#}

#{ Internal
class PointOfInterest(object):
    def dump(self, ind=0):
        pass

    def walk(self, level=0, select=lambda l, c: True, args=None, done=None):
        return []

    @property
    def levelAdjust(self):
        return 0


class Step(PointOfInterest):
    """Details of a test step.

    :Ivariables:
      lNum
        The file line number where the step starts.
      lines
        The lines of text that describe the test step.
    """
    sortV = 50
    type = "step"

    def __init__(self, lNum, lines):
        self.lNum = lNum
        self.lines = list(lines)

    def __str__(self):
        return "\n".join(self.lines)


class BoundStep(Step):
    def __init__(self, funcPoint, stepPoint):
        super(BoundStep, self).__init__(stepPoint.lNum, stepPoint.lines)
        self.funcPoint = weakref.proxy(funcPoint)
        self.stepPoint = stepPoint


def isMethodOrFunc(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def unwrapFunc(func):
    while hasattr(func, "undecorated"):
        func = func.undecorated
    return func


tpl = '''class _X_(object):
    def %s(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    def go(self):
        %s
'''

ccc = '''
inst = _X_()
inst.go()
'''

propagateArgErrs = True


def bindArgsForInvocation(calledFunc, callCode, namespace=None):
    calledName = calledFunc.func.__name__
    callCode = callCode.strip()

    if not callCode.startswith("self."):
        return

    d = namespace or {}
    try:
        exec(tpl % (calledName, callCode), d, d)
        exec(ccc, d, d)
    except:  # Pretty much any exception can occur.
        return

    try:
        return inspect.getcallargs(calledFunc.func, None,
                                   *d["inst"].args, **d["inst"].kwargs)
    except: # Types of exception unpredictable.
        if propagateArgErrs:
            raise


class TestMap(PointOfInterest):
    """Mapping of a test function (direct or indirect) to useful information.

    :Ivariables:
      func
        The function in question.
      code
        The code of the function.
      lines, startLine
        The text lines of the functions and the number of the line where the
        function's definition begins.
      invocations
        Sequence of ``(lineNumber, TestMap)``. Each represents the invocation
        of a function/method.
      steps
        The detailed steps extracted from the source code.
    """
    sortV = 100
    type = "func"
    _known = {}
    _classMap = {}

    def __init__(self, func, cls):
        linecache.checkcache()
        self.func = func
        self.cls = cls
        self.code = func.__code__
        try:
            func = unwrapFunc(func)
            self.lines, self.startLine = inspect.getsourcelines(func)
        except:  # Exception types difficult to predict
            self.startLine = 0
            self.lines = []
        self.invocations = []
        self.steps = []
        self._deadEnds = set()

        self.name = None
        self.isMethodCall = None
        self.module = None

    @property
    def levelAdjust(self):
        if getattr(self.func, "_cs_inline", None):
            return -1
        return 0

    def processInvocation(self, lineIdx, line, emitStep, module, cls):
        m = rProcCall.match(line) or rFuncCall.match(line)
        if m:
            emitStep()
            methodCall = False
            invokeName = m.group("name")
            if invokeName.startswith("self."):
                invokeName = invokeName[5:]
                methodCall = True

            calledFunc = getattr(module, invokeName, None)
            if calledFunc is None and cls is not None:
                calledFunc = cls.__dict__.get(invokeName, None)
                if calledFunc is None:
                    for base in cls.__bases__:
                        calledFunc = getattr(base, invokeName, None)
                        if calledFunc is not None:
                            break
            if calledFunc is None:
                return True

            try:
                self._classMap[calledFunc] = cls
            except TypeError:
                pass
            if not (isMethodOrFunc(calledFunc)
                    or hasattr(calledFunc, "_cs_isProcedural")):
                return True

            testMap = self.getTestMap(calledFunc)
            testMap.name = invokeName
            testMap.isMethodCall = methodCall
            testMap.module = module

            self.invocations.append((self.startLine + lineIdx,
                                     (testMap, line.strip())))
            return True

    def getStepsAndCalls(self):
        """Find all test steps and function invocations for this function."""
        def emitStep():
            while step and not step[0].strip():
                step.pop(0)
            while step and not step[-1].strip():
                step.pop()
            if step:
                lNum = self.startLine + lineIdx
                self.steps.append((lNum, (Step(lNum, step), None)))
            step[:] = []

        step = []
        module = inspect.getmodule(self.func)
        klass = self.cls
        if klass is None:
            klass = self._classMap.get(self.func, None)
        for lineIdx, line in enumerate(self.lines):
            m = rStepComment.match(line)
            if m:
                step.append(m.group(1))
                continue

            if rComment.match(line):
                continue

            if self.processInvocation(lineIdx, line, emitStep, module, klass):
                continue

            if line.strip():
                emitStep()
            else:
                step.append(line.rstrip())
        emitStep()

    def walk(self, level=0, select=lambda l, c: True, args=None, done=None):
        if done is None:
            done = set()
        if self in done:
            return
        done.add(self)
        args = args or {}
        for i, (point, line) in sorted(
                self.invocations + self.steps,
                key=lambda el: (el[0], el[1][0].sortV, el[1])):
            if point is self:
                continue
            boundArgs = {}
            if select(level, point):
                if point.type == "step":
                    yield level, BoundStep(self, point), args
                else:
                    if point is not None:
                        boundArgs = bindArgsForInvocation(point, line, args)
                        yield level, point, boundArgs

            if point is not None:
                for child in point.walk(level + 1 + point.levelAdjust,
                                        select=select, args=boundArgs,
                                        done=done):
                    yield child

    def walkSteps(self):
        n = []
        for level, p, boundArgs in self.walk():
            if p.type == "step":
                while len(n) > level + 1:
                    n.pop()
                if len(n) <= level:
                    while len(n) <= level:
                        n.append(1)
                else:
                    n[-1] += 1

                yield n, p.lines, boundArgs

    @classmethod
    def getTestMap(cls, func):

        if options.get_option_value("details"):
            # If we cache the map values we don't get the correct output when the --details arg is used, however not
            # caching them is a fairly large performance hit so we only do it specifically for the details
            funcClass, _ = getFuncClassID(func)
            funcMap = TestMap(func, funcClass)
            funcMap.getStepsAndCalls()
            return funcMap
        else:
            funcClass, funcClassID = getFuncClassID(func)
            key = func.__code__, funcClassID
            if key not in cls._known:
                funcMap = TestMap(func, funcClass)
                cls._known[key] = funcMap
                funcMap.getStepsAndCalls()
            return cls._known[key]


class RunTracer(object):
    def __init__(self, callMap, stepMap):
        self.traceTable = {
            "call": self.handleCall,
            "line": self.handleLine,
            "return": self.handleReturn,
        }
        self.code = None
        self.stack = []
        self.n = []
        self._callMap = callMap
        self._stepMap = stepMap
        self._prevKey = None

        # A cache map of step index sequences mapping a tuple sequence of index
        # values to the latest value used at the next nested level of that
        # test step index sequence. The tuple (0,) is special meaning the root
        # top level index.
        # e.g. {(1,2,): 5} means that the most recent nested test index used
        # after 1.2 is 5, giving a test index 1.2.5 to start from and increment
        # for the next test step at that level.
        self.stepIdxMap = {(0,): 0}

    def run(self, func, args, kwargs):
        self.oldTrace = sys.gettrace()
        self.lineTrace = None
        sys.settrace(self.trace)
        _cs_test_invoker_marker_ = None
        try:
            func(*args, **kwargs)
        finally:
            sys.settrace(self.oldTrace)

    def _fallback(self, frame, event, arg):
        if self.oldTrace:
            return self.oldTrace(frame, event, arg)

    def trace(self, frame, event, arg):
        return self.traceTable.get(event, self._fallback)(frame, event, arg)

    def handleCall(self, frame, event, arg):
        lineTrace = None
        if self.oldTrace:
            lineTrace = self.oldTrace(frame, event, arg)
        code = frame.f_code
        callPoint = self._callMap.get(code, None)
        if callPoint is not None:
            if callPoint.levelAdjust == 0:
                # Save the current state of the test step index values
                nToSave = list(self.n)

                if not self.n or len(self.n) == 1:
                    # Dealing with the top level (root) test step, ensure
                    # it is set to the latest value in the index cache
                    self.n = [self.stepIdxMap.get((0,), 0)]

                # Note this code doesn't produce the same output as --details would in terms of test numbering
                # Instead of say 1.1.1.1 where the second and 3rd level have no calls you get 1.1
                # Trying to correctly fix this while also keeping the cs_inline working has proved too difficult so
                # for now I have just left it how Fractal had it as no one else would care
                if callPoint.steps and self.n[-1] != 0:
                    # The function about to be called contains test steps
                    # and the deepest nested step index is not zero
                    # which means a new level of step index should be added.
                    # Use the index cache to get the latest value for this
                    # new level if it has already been reached, or start at 0.
                    stepKey = tuple(self.n)
                    self.n.append(self.stepIdxMap.get(stepKey, 0))
            else:
                nToSave = self.n

            self.stack.append((self.code, nToSave, self.lineTrace))
            self.lineTrace = lineTrace
            self.code = code
            return self.trace
        return lineTrace

    def handleLine(self, frame, event, arg):
        if self.lineTrace:
            _ = self.lineTrace(frame, event, arg)
        stepKey = self.code, frame.f_lineno
        stepPoint = self._stepMap.get(stepKey, None)
        if stepPoint is not None:
            if stepKey == self._prevKey:
                return
            self._prevKey = stepKey
            self.n[-1] += 1

            nStr = ".".join(str(v) for v in self.n) + "."
            self.update_commentary([nStr] + stepPoint.lines)

            # Record the latest step index that has just been used at
            # this nested level
            if len(self.n) > 1:
                indexKey = tuple(self.n[:-1])
            else:
                indexKey = (0,)
            self.stepIdxMap[indexKey] = self.n[-1]
            return self.trace

    def handleReturn(self, frame, event, arg):
        if self.lineTrace:
            self.lineTrace(frame, event, arg)
        # record the current state of the test step index values before
        # restoring to the calling functions version.
        if self.n:
            currentStepNumbers = list(self.n)
        else:
            currentStepNumbers = None

        self.code, self.n, self.lineTrace = self.stack.pop()

        if self.n and currentStepNumbers:
            # It is possible that test steps at this level have
            # updated nested step level values shared by the calling function
            # It is important to update the restored step index values
            # to match these values in case there are any test steps
            # in the calling function that follow the call we are just
            # returning from.
            checkLength = min(len(self.n), len(currentStepNumbers))

            for index in range(checkLength):
                if self.n[index] < currentStepNumbers[index]:
                    self.n[index] = currentStepNumbers[index]

        return self.trace

    def update_commentary(self, lines):
        descr = " ".join(lines)
        status = Coordinator.getServiceProvider("status")
        status.setField("commentary", descr)
        log.info("#> %s", descr)
#}
