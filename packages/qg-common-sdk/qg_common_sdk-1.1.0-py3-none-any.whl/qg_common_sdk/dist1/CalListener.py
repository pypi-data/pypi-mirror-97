# Generated from Cal.g4 by ANTLR 4.9.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .CalParser import CalParser
else:
    from CalParser import CalParser


# This class defines a complete listener for a parse tree produced by CalParser.
class CalListener(ParseTreeListener):

    # Enter a parse tree produced by CalParser#AndExpr.
    def enterAndExpr(self, ctx: CalParser.AndExprContext):
        pass

    # Exit a parse tree produced by CalParser#AndExpr.
    def exitAndExpr(self, ctx: CalParser.AndExprContext):
        pass

    # Enter a parse tree produced by CalParser#CheckExpr.
    def enterCheckExpr(self, ctx: CalParser.CheckExprContext):
        pass

    # Exit a parse tree produced by CalParser#CheckExpr.
    def exitCheckExpr(self, ctx: CalParser.CheckExprContext):
        pass

    # Enter a parse tree produced by CalParser#DependExpr.
    def enterDependExpr(self, ctx: CalParser.DependExprContext):
        pass

    # Exit a parse tree produced by CalParser#DependExpr.
    def exitDependExpr(self, ctx: CalParser.DependExprContext):
        pass

    # Enter a parse tree produced by CalParser#ConditionExpr.
    def enterConditionExpr(self, ctx: CalParser.ConditionExprContext):
        pass

    # Exit a parse tree produced by CalParser#ConditionExpr.
    def exitConditionExpr(self, ctx: CalParser.ConditionExprContext):
        pass

    # Enter a parse tree produced by CalParser#AtomExpr.
    def enterAtomExpr(self, ctx: CalParser.AtomExprContext):
        pass

    # Exit a parse tree produced by CalParser#AtomExpr.
    def exitAtomExpr(self, ctx: CalParser.AtomExprContext):
        pass

    # Enter a parse tree produced by CalParser#ParenExpr.
    def enterParenExpr(self, ctx: CalParser.ParenExprContext):
        pass

    # Exit a parse tree produced by CalParser#ParenExpr.
    def exitParenExpr(self, ctx: CalParser.ParenExprContext):
        pass

    # Enter a parse tree produced by CalParser#OpExpr.
    def enterOpExpr(self, ctx: CalParser.OpExprContext):
        pass

    # Exit a parse tree produced by CalParser#OpExpr.
    def exitOpExpr(self, ctx: CalParser.OpExprContext):
        pass


del CalParser
