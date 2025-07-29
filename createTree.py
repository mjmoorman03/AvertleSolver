import pickle 

def getWordsArray():
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    return words


def removePrefixes(words):
    """
    Remove words that are prefixes of other words in the list.
    """
    words.sort(key=len)
    result = []
    prefixes = set()

    for word in words:
        if not any(word.startswith(prefix) for prefix in prefixes):
            result.append(word)
            prefixes.add(word)

    return result


def writeWordsToFile(words):
    with open('wordNoPrefixes.txt', 'w') as file:
        for word in words:
            file.write(word + '\n')


# player starts, so player chooses when string length is currently even
class TreeNode:
    def __init__(self, value=None):
        self.parent = None
        self.value = value
        self.children = {}
        self.isLeaf = False
        self.firstPlayerWins = False
        self.depth = 0


# a node's children are strings that can be formed by adding one character to the current string
# that are contained in the words list
def createWordsTree(words):
    root = TreeNode()
    root.value = ""
    for word in words:
        depth = 0
        current = root
        for char in word:
            depth += 1
            if char not in current.children:
                new_node = TreeNode(char)
                new_node.parent = current
                current.children[char] = new_node
            current = current.children[char]
            current.depth = depth  # increment depth based on character position in word
        current.isLeaf = True
    return root


def saveTreeToFile(tree, filename='tree.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(tree, file)

def loadTreeFromFile(filename='tree.pkl'):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
    
def solveStackelbergTree(root):
    """
    Solve the Stackelberg game on the tree.
    """
    def dfs(node):
        if node.isLeaf:
            # since this would mean player 2 played last
            node.firstPlayerWins = node.depth % 2 == 0
            return node.firstPlayerWins
        
        firstPlayerWins = [dfs(child) for child in node.children.values()]
        # if current player is first player (even length string)
        # then they win if at least one child leads to a win for them (by playing that child)
        if node.depth % 2 == 0:
            node.firstPlayerWins = any(firstPlayerWins)
        # if current player is second player (odd length string)
        # they only lose if all children lead to a win for the first player
        else:
            node.firstPlayerWins = all(firstPlayerWins)

        return node.firstPlayerWins
    
    dfs(root)
    return root
    

if __name__ == "__main__":
    # verify depth to ensure we really are solving correctly
    words = getWordsArray()
    maxLength = max(len(word) for word in words)
    print(f"Max word length: {maxLength}")

    tree = createWordsTree(words)
    def calculateMaxDepth(node, depth=0):
        if node.isLeaf:
            return depth
        return max(calculateMaxDepth(child, depth + 1) for child in node.children.values())
    maxDepth = calculateMaxDepth(tree)
    print(f"Max tree depth: {maxDepth}")
        
    # now, do backwards induction to solve the Stackelberg game on the tree
    solvedTree = solveStackelbergTree(tree)
    saveTreeToFile(solvedTree, 'solved_tree.pkl')
    print(f"Result: First player wins: {solvedTree.firstPlayerWins}")