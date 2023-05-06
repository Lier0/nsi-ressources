from IPython.display import display, HTML

def display_green():
    display(HTML("<div style='color: green;'>Bonne réponse</div>"))
def display_red():
    display(HTML("<div style='color: red;'>Mauvaise réponse</div>"))

def display_answer(answer, solution):
    if type(answer) is display_answer.__class__:
        answer = answer()
    if answer == solution:
        display_green()
    else:
        display_red()

def check_answer(answer, solution):
    for s in solution:
        if s not in answer:
            return display_red()
    display_green()

def answer_root(root):
    display_answer(root, 'a')

def answer_nodes(nodes):
    check_answer(nodes, ['a', 'b', 'c', 'd'])

def answer_leaves(leaves):
    check_answer(leaves, ['c', 'd'])

def answer_trees(trees):
    solutions = [['a', 'b', 'c', 'd'], ['b', 'c'], ['c'], ['d']]
    check_answer(trees, solutions)

def answer_size(size):
    display_answer(size, 4)

def answer_height(height):
    display_answer(height, 3)