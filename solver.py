import createTree
import pickle
from createTree import TreeNode

def solve(tree):
    print("N.B. This solver will give you the optimal path to win, provided there is one!")
    firstPlayerIsUser = True if input("Is the first player the user? (yes/no): ").strip().lower() == 'yes' else False
    turn = 0
    word = ''
    while True:
        if firstPlayerIsUser != bool(turn % 2):
            winningLetters = [char for char, child in tree.children.items() if child.firstPlayerWins == firstPlayerIsUser]
            if winningLetters:
                print("Winning moves for the current player:", winningLetters)
            else:
                print("No winning moves available.")
            while True:
                char = input("Enter your move (character): ").strip().lower()
                if char in tree.children:
                    tree = tree.children[char]
                    word += char
                    break
                else:
                    print("Invalid move. Try again.")
            if tree.isLeaf:
                print("You lost! The word is: ", word)
                break
        else:
            while True:
                char = input("Enter the opponent's move (character): ").strip().lower()
                if char in tree.children:
                    tree = tree.children[char]
                    word += char
                    break
                else:
                    print("Invalid move. Try again.")
            if tree.isLeaf:
                print("You won! The word is: ", word)
                break
        turn += 1


if __name__ == "__main__":
    tree = createTree.loadTreeFromFile('solved_tree.pkl')
    solve(tree)

