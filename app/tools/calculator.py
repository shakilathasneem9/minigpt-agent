import ast
import operator as op

# Allowed operators only
allowed_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
}


def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)

    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        operator = type(node.op)

        if operator in allowed_operators:
            return allowed_operators[operator](left, right)
        else:
            raise ValueError("Unsupported operation")

    elif isinstance(node, ast.Constant):  # numbers
        return node.value

    else:
        raise ValueError("Invalid expression")


def calculate(expr: str) -> str:
    """
    Safe calculator using AST (no eval risk)
    Supports: +, -, *, /, %, parentheses
    """

    try:
        # Parse expression into AST
        node = ast.parse(expr, mode="eval")

        result = safe_eval(node)

        return str(result)

    except ZeroDivisionError:
        return "Error: Division by zero"

    except Exception:
        return "Invalid math expression"