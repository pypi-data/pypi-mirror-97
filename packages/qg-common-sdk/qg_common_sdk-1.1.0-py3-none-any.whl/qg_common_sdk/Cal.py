#!/usr/bin/python3
import re
import time

from antlr4 import *

from qg_common_sdk.dist1.CalLexer import CalLexer
from qg_common_sdk.dist1.CalParser import CalParser
from qg_common_sdk.dist1.CalVisitor import CalVisitor


class CalVisitor(CalVisitor):
    def visitConditionExpr(self, ctx: CalParser.ConditionExprContext):
        left = self.visit(ctx.left)
        if left and left != 'None':
            left = left.replace("\"", "").replace("'", "")
        right = self.visit(ctx.right)
        if right and right != 'None':
            if left is not None and left != '' and left != 'None' and left:
                return True
            else:
                return False
        else:
            return True

    def visitAndExpr(self, ctx: CalParser.AndExprContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if left and left != 'None':
            left = left.replace("\"", "").replace("'", "")
        if right and right != 'None':
            right = right.replace("\"", "").replace("'", "")
        return (left is not None and left != '' and left != 'None' and left) and (
                right is not None and right != '' and right != 'None' and right)

    def visitDependExpr(self, ctx: CalParser.CheckExprContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if right and right != 'None':
            right = right.replace("\"", "").replace("'", "")
        else:
            return True
        if left and left != 'None':
            if right:
                return True
            else:
                return False
        else:
            return left

    # Visit a parse tree produced by CalParser#CheckExpr.
    def visitCheckExpr(self, ctx: CalParser.CheckExprContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if (left == 'None' or left is None or left == '') and (right == 'None' or right is None or right == ''):
            return True
        op = ctx.op.text
        pattern = r'(\d{4}-\d{1,2}-\d{1,2})'
        pattern = re.compile(pattern)
        result = pattern.findall(left)
        if result:
            eval_str = '"{left}" {op} "{right}"'.format(left=str(left), op=str(op), right=str(right))
        else:
            eval_str = str(left) + str(op) + str(right)
        return eval(eval_str)

    def get_time(self, value):
        pattern = ('%Y年%m月%d日', '%Y-%m-%d', '%y年%m月%d日', '%y-%m-%d')
        output = '%Y-%m-%d'
        for i in pattern:
            try:
                ret = time.strptime(value, i)
                if ret:
                    return time.strftime(output, ret)
            except:
                return value

    # Visit a parse tree produced by CalParser#AtomExpr.
    def visitAtomExpr(self, ctx: CalParser.AtomExprContext):
        return ctx.getText()

    # Visit a parse tree produced by CalParser#ParenExpr.
    def visitParenExpr(self, ctx: CalParser.ParenExprContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by CalParser#OpExpr.
    def visitOpExpr(self, ctx: CalParser.OpExprContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        op = ctx.op.text
        eval_str = str(left) + str(op) + str(right)
        return eval(eval_str)


def calc(line) -> float:
    input_stream = InputStream(line)

    # lexing
    lexer = CalLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # parsing
    parser = CalParser(stream)
    tree = parser.expr()

    # use customized visitor to traverse AST
    visitor = CalVisitor()
    return visitor.visit(tree)


if __name__ == '__main__':
    while True:
        print(">>> ", end='')
        line = input()
        print(calc(line))
