# Generated from Cal.g4 by ANTLR 4.9.1
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\23")
        buf.write("$\4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2\13\n\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\7\2\37\n\2\f\2\16\2\"\13\2\3\2\2\3\2\3\2\2\5")
        buf.write("\3\2\6\13\3\2\f\r\3\2\16\17\2)\2\n\3\2\2\2\4\5\b\2\1\2")
        buf.write("\5\13\7\22\2\2\6\7\7\20\2\2\7\b\5\2\2\2\b\t\7\21\2\2\t")
        buf.write("\13\3\2\2\2\n\4\3\2\2\2\n\6\3\2\2\2\13 \3\2\2\2\f\r\f")
        buf.write("\n\2\2\r\16\7\3\2\2\16\37\5\2\2\13\17\20\f\t\2\2\20\21")
        buf.write("\7\4\2\2\21\37\5\2\2\n\22\23\f\b\2\2\23\24\7\5\2\2\24")
        buf.write("\37\5\2\2\t\25\26\f\7\2\2\26\27\t\2\2\2\27\37\5\2\2\b")
        buf.write("\30\31\f\6\2\2\31\32\t\3\2\2\32\37\5\2\2\7\33\34\f\5\2")
        buf.write("\2\34\35\t\4\2\2\35\37\5\2\2\6\36\f\3\2\2\2\36\17\3\2")
        buf.write("\2\2\36\22\3\2\2\2\36\25\3\2\2\2\36\30\3\2\2\2\36\33\3")
        buf.write("\2\2\2\37\"\3\2\2\2 \36\3\2\2\2 !\3\2\2\2!\3\3\2\2\2\"")
        buf.write(" \3\2\2\2\5\n\36 ")
        return buf.getvalue()


class CalParser(Parser):
    grammarFileName = "Cal.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'?'", "'&'", "'#'", "'>='", "'<='", "'>'",
                    "'<'", "'='", "'=='", "'*'", "'/'", "'+'", "'-'", "'('",
                    "')'"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "WORD", "WS"]

    RULE_expr = 0

    ruleNames = ["expr"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    WORD = 16
    WS = 17

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return CalParser.RULE_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class AndExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.left = None  # ExprContext
            self.op = None  # Token
            self.right = None  # ExprContext
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CalParser.ExprContext)
            else:
                return self.getTypedRuleContext(CalParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAndExpr"):
                listener.enterAndExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAndExpr"):
                listener.exitAndExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAndExpr"):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)

    class CheckExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.left = None  # ExprContext
            self.op = None  # Token
            self.right = None  # ExprContext
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CalParser.ExprContext)
            else:
                return self.getTypedRuleContext(CalParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCheckExpr"):
                listener.enterCheckExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCheckExpr"):
                listener.exitCheckExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCheckExpr"):
                return visitor.visitCheckExpr(self)
            else:
                return visitor.visitChildren(self)

    class DependExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.left = None  # ExprContext
            self.op = None  # Token
            self.right = None  # ExprContext
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CalParser.ExprContext)
            else:
                return self.getTypedRuleContext(CalParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterDependExpr"):
                listener.enterDependExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitDependExpr"):
                listener.exitDependExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDependExpr"):
                return visitor.visitDependExpr(self)
            else:
                return visitor.visitChildren(self)

    class ConditionExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.left = None  # ExprContext
            self.op = None  # Token
            self.right = None  # ExprContext
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CalParser.ExprContext)
            else:
                return self.getTypedRuleContext(CalParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterConditionExpr"):
                listener.enterConditionExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitConditionExpr"):
                listener.exitConditionExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitConditionExpr"):
                return visitor.visitConditionExpr(self)
            else:
                return visitor.visitChildren(self)

    class AtomExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.atom = None  # Token
            self.copyFrom(ctx)

        def WORD(self):
            return self.getToken(CalParser.WORD, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAtomExpr"):
                listener.enterAtomExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAtomExpr"):
                listener.exitAtomExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAtomExpr"):
                return visitor.visitAtomExpr(self)
            else:
                return visitor.visitChildren(self)

    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CalParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterParenExpr"):
                listener.enterParenExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitParenExpr"):
                listener.exitParenExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParenExpr"):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)

    class OpExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a CalParser.ExprContext
            super().__init__(parser)
            self.left = None  # ExprContext
            self.op = None  # Token
            self.right = None  # ExprContext
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CalParser.ExprContext)
            else:
                return self.getTypedRuleContext(CalParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterOpExpr"):
                listener.enterOpExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitOpExpr"):
                listener.exitOpExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOpExpr"):
                return visitor.visitOpExpr(self)
            else:
                return visitor.visitChildren(self)

    def expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CalParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CalParser.WORD]:
                localctx = CalParser.AtomExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 3
                localctx.atom = self.match(CalParser.WORD)
                pass
            elif token in [CalParser.T__13]:
                localctx = CalParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 4
                self.match(CalParser.T__13)
                self.state = 5
                self.expr(0)
                self.state = 6
                self.match(CalParser.T__14)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 2, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 28
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
                    if la_ == 1:
                        localctx = CalParser.ConditionExprContext(self,
                                                                  CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 10
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 11
                        localctx.op = self.match(CalParser.T__0)
                        self.state = 12
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = CalParser.AndExprContext(self, CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 13
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 14
                        localctx.op = self.match(CalParser.T__1)
                        self.state = 15
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 3:
                        localctx = CalParser.DependExprContext(self,
                                                               CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 16
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 17
                        localctx.op = self.match(CalParser.T__2)
                        self.state = 18
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 4:
                        localctx = CalParser.CheckExprContext(self,
                                                              CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 19
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 20
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                                (1 << CalParser.T__3) | (1 << CalParser.T__4) | (1 << CalParser.T__5) | (
                                1 << CalParser.T__6) | (1 << CalParser.T__7) | (1 << CalParser.T__8))) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 21
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 5:
                        localctx = CalParser.OpExprContext(self, CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 22
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 23
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not (_la == CalParser.T__9 or _la == CalParser.T__10):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 24
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 6:
                        localctx = CalParser.OpExprContext(self, CalParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 25
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 26
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not (_la == CalParser.T__11 or _la == CalParser.T__12):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 27
                        localctx.right = self.expr(4)
                        pass

                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 2, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    def sempred(self, localctx: RuleContext, ruleIndex: int, predIndex: int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx: ExprContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 8)

        if predIndex == 1:
            return self.precpred(self._ctx, 7)

        if predIndex == 2:
            return self.precpred(self._ctx, 6)

        if predIndex == 3:
            return self.precpred(self._ctx, 5)

        if predIndex == 4:
            return self.precpred(self._ctx, 4)

        if predIndex == 5:
            return self.precpred(self._ctx, 3)
