import java.util.Scanner;

// Node class for AVL Tree
class Node {
    int element, height;
    Node leftChild, rightChild;

    Node(int element) {
        this.element = element;
        height = 0;
    }
}

// AVL Tree class
class AVLTree {
    private Node root;

    // Insert element into AVL Tree
    public void insert(int element) {
        root = insert(root, element);
    }

    // Check if the tree is empty
    public boolean isEmpty() {
        return root == null;
    }

    // Remove all nodes
    public void clear() {
        root = null;
    }

    // Get total number of nodes
    public int size() {
        return size(root);
    }

    // Search for an element
    public boolean search(int element) {
        return search(root, element);
    }

    // Display tree in-order
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    // Display tree pre-order
    public void preorder() {
        preorder(root);
        System.out.println();
    }

    // Display tree post-order
    public void postorder() {
        postorder(root);
        System.out.println();
    }

    private Node insert(Node node, int element) {
        if (node == null) return new Node(element);

        if (element < node.element) {
            node.leftChild = insert(node.leftChild, element);
        } else if (element > node.element) {
            node.rightChild = insert(node.rightChild, element);
        } else {
            return node; // Duplicate elements are not allowed
        }

        return balance(node);
    }

    private Node balance(Node node) {
        int balanceFactor = height(node.leftChild) - height(node.rightChild);

        if (balanceFactor > 1) {
            if (height(node.leftChild.leftChild) >= height(node.leftChild.rightChild)) {
                node = rotateRight(node);
            } else {
                node = rotateLeftRight(node);
            }
        } else if (balanceFactor < -1) {
            if (height(node.rightChild.rightChild) >= height(node.rightChild.leftChild)) {
                node = rotateLeft(node);
            } else {
                node = rotateRightLeft(node);
            }
        }

        node.height = Math.max(height(node.leftChild), height(node.rightChild)) + 1;
        return node;
    }

    private Node rotateRight(Node node) {
        Node newRoot = node.leftChild;
        node.leftChild = newRoot.rightChild;
        newRoot.rightChild = node;
        node.height = Math.max(height(node.leftChild), height(node.rightChild)) + 1;
        newRoot.height = Math.max(height(newRoot.leftChild), node.height) + 1;
        return newRoot;
    }

    private Node rotateLeft(Node node) {
        Node newRoot = node.rightChild;
        node.rightChild = newRoot.leftChild;
        newRoot.leftChild = node;
        node.height = Math.max(height(node.leftChild), height(node.rightChild)) + 1;
        newRoot.height = Math.max(height(newRoot.rightChild), node.height) + 1;
        return newRoot;
    }

    private Node rotateLeftRight(Node node) {
        node.leftChild = rotateLeft(node.leftChild);
        return rotateRight(node);
    }

    private Node rotateRightLeft(Node node) {
        node.rightChild = rotateRight(node.rightChild);
        return rotateLeft(node);
    }

    private int height(Node node) {
        return node == null ? -1 : node.height;
    }

    private int size(Node node) {
        if (node == null) return 0;
        return 1 + size(node.leftChild) + size(node.rightChild);
    }

    private boolean search(Node node, int element) {
        while (node != null) {
            if (element < node.element) {
                node = node.leftChild;
            } else if (element > node.element) {
                node = node.rightChild;
            } else {
                return true;
            }
        }
        return false;
    }

    private void inorder(Node node) {
        if (node != null) {
            inorder(node.leftChild);
            System.out.print(node.element + " ");
            inorder(node.rightChild);
        }
    }

    private void preorder(Node node) {
        if (node != null) {
            System.out.print(node.element + " ");
            preorder(node.leftChild);
            preorder(node.rightChild);
        }
    }

    private void postorder(Node node) {
        if (node != null) {
            postorder(node.leftChild);
            postorder(node.rightChild);
            System.out.print(node.element + " ");
        }
    }
}

// Main class
public class AVLTreeExample {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        AVLTree tree = new AVLTree();
        char choice;

        do {
            System.out.println("\nSelect an operation:");
            System.out.println("1. Insert a node");
            System.out.println("2. Search a node");
            System.out.println("3. Get total number of nodes");
            System.out.println("4. Is tree empty?");
            System.out.println("5. Remove all nodes");
            System.out.println("6. Display tree in Post order");
            System.out.println("7. Display tree in Pre order");
            System.out.println("8. Display tree in In order");

            int ch = sc.nextInt();
            switch (ch) {
                case 1:
                    System.out.println("Enter element to insert:");
                    tree.insert(sc.nextInt());
                    break;
                case 2:
                    System.out.println("Enter element to search:");
                    System.out.println(tree.search(sc.nextInt()));
                    break;
                case 3:
                    System.out.println("Total nodes: " + tree.size());
                    break;
                case 4:
                    System.out.println("Tree empty: " + tree.isEmpty());
                    break;
                case 5:
                    tree.clear();
                    System.out.println("Tree cleared.");
                    break;
                case 6:
                    System.out.println("Post order:");
                    tree.postorder();
                    break;
                case 7:
                    System.out.println("Pre order:");
                    tree.preorder();
                    break;
                case 8:
                    System.out.println("In order:");
                    tree.inorder();
                    break;
                default:
                    System.out.println("Invalid choice.");
            }
            System.out.println("Press 'y' to continue");
            choice = sc.next().charAt(0);
        } while (choice == 'Y' || choice == 'y');

        sc.close();
    }
}
