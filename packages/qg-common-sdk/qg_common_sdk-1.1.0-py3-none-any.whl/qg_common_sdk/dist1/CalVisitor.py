# Generated from Cal.g4 by ANTLR 4.9.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .CalParser import CalParser
else:
    from CalParser import CalParser


# This class defines a complete generic visitor for a parse tree produced by CalParser.

class CalVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CalParser#AndExpr.
    def visitAndExpr(self, ctx: CalParser.AndExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#CheckExpr.
    def visitCheckExpr(self, ctx: CalParser.CheckExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#DependExpr.
    def visitDependExpr(self, ctx: CalParser.DependExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#ConditionExpr.
    def visitConditionExpr(self, ctx: CalParser.ConditionExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#AtomExpr.
    def visitAtomExpr(self, ctx: CalParser.AtomExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#ParenExpr.
    def visitParenExpr(self, ctx: CalParser.ParenExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CalParser#OpExpr.
    def visitOpExpr(self, ctx: CalParser.OpExprContext):
        return self.visitChildren(ctx)


del CalParser
