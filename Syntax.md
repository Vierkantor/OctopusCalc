Syntax
======

The syntax as it now is:

value :: Integer | Decimal | Boolean

infixPart -> infix expression

argumentList -> ''
argumentList -> expression
argumentList -> expression ',' argumentList

expression -> function argumentList
expression -> value infixPart
expression -> '(' expression ')' infixPart