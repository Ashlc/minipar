from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en

# Test for print('Hello, world!')

root = SyntaxNode(en.PROGRAM)
print_node = SyntaxNode(en.RW_PRINT, SyntaxNode(en.STRING_LITERAL, "Hello, world!"))

root.add_children(print_node)

root.print_tree()
print(root.children[0].node_type)
print(root.children[0].value.value)