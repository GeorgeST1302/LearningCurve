import java.util.Arrays;

public class MaxHeap {
    private int[] arr;
    private int size;
    private int capacity;

    // Constructor to initialize the heap with a given capacity
    public MaxHeap(int capacity) {
        this.capacity = capacity;
        this.arr = new int[capacity];
        this.size = 0;
    }

    // Returns the index of the parent, left child, and right child
    private int parent(int i) { return (i - 1) / 2; }
    private int leftChild(int i) { return 2 * i + 1; }
    private int rightChild(int i) { return 2 * i + 2; }

    // Ensures the heap property is maintained
    private void heapify(int i) {
        int largest = i;
        int l = leftChild(i);
        int r = rightChild(i);

        if (l < size && arr[l] > arr[largest]) largest = l;
        if (r < size && arr[r] > arr[largest]) largest = r;

        if (largest != i) {
            swap(i, largest);
            heapify(largest);
        }
    }

    // Swap elements at indices i and j
    private void swap(int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // Insert a new key into the heap
    public void insert(int key) {
        if (size == capacity) {
            System.out.println("Overflow: Cannot insert key");
            return;
        }

        int i = size++;
        arr[i] = key;

        // Restore heap property by moving the new key up
        while (i != 0 && arr[parent(i)] < arr[i]) {
            swap(i, parent(i));
            i = parent(i);
        }
    }

    // Remove and return the maximum element from the heap
    public int removeMax() {
        if (size <= 0) return Integer.MIN_VALUE;
        if (size == 1) return arr[--size];

        int root = arr[0];
        arr[0] = arr[--size];
        heapify(0);
        return root;
    }

    // Return the maximum element
    public int getMax() {
        return size > 0 ? arr[0] : Integer.MIN_VALUE;
    }

    // Delete the element at index i
    public void delete(int i) {
        if (i >= size) return;

        arr[i] = Integer.MAX_VALUE;
        while (i != 0 && arr[parent(i)] < arr[i]) {
            swap(i, parent(i));
            i = parent(i);
        }
        removeMax();
    }

    // Return the number of elements in the heap
    public int getSize() {
        return size;
    }

    public static void main(String[] args) {
        MaxHeap heap = new MaxHeap(15);
        heap.insert(3); heap.insert(10); heap.insert(12);
        heap.insert(8); heap.insert(2); heap.insert(14);

        System.out.println("Size: " + heap.getSize());
        System.out.println("Max: " + heap.getMax());

        heap.delete(2);

        heap.insert(15); heap.insert(5);
        System.out.println("Size: " + heap.getSize());
        System.out.println("Max: " + heap.getMax());
    }
}


/*import java.util.Arrays;

public class MinHeap { // Changed class name from MaxHeap to MinHeap
    private int[] arr;
    private int size;
    private int capacity;

    public MinHeap(int capacity) { // Constructor remains unchanged
        this.capacity = capacity;
        this.arr = new int[capacity];
        this.size = 0;
    }

    private int parent(int i) { return (i - 1) / 2; }
    private int leftChild(int i) { return 2 * i + 1; }
    private int rightChild(int i) { return 2 * i + 2; }

    private void heapify(int i) { // Modified heapify method for min-heap
        int smallest = i; // Changed variable name from largest to smallest
        int l = leftChild(i);
        int r = rightChild(i);

        // Check if left child exists and is smaller than the current node
        if (l < size && arr[l] < arr[smallest]) smallest = l;
        // Check if right child exists and is smaller than the current smallest
        if (r < size && arr[r] < arr[smallest]) smallest = r;

        // If the smallest is not the current node, swap and heapify the affected subtree
        if (smallest != i) {
            swap(i, smallest);
            heapify(smallest);
        }
    }

    private void swap(int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public void insert(int key) { // Insert method remains largely the same
        if (size == capacity) {
            System.out.println("Overflow: Cannot insert key");
            return;
        }

        int i = size++;
        arr[i] = key;

        // Bubble up to maintain the min-heap property (changed condition to '<')
        while (i != 0 && arr[parent(i)] > arr[i]) { // Changed comparison to maintain min-heap
            swap(i, parent(i));
            i = parent(i);
        }
    }

    public int removeMin() { // Changed method name from removeMax to removeMin
        if (size <= 0) return Integer.MAX_VALUE; // Use Integer.MAX_VALUE to signify an empty heap
        if (size == 1) return arr[--size];

        int root = arr[0];
        arr[0] = arr[--size];
        heapify(0); // Re-adjust heap to maintain min-heap property
        return root;
    }

    public int getMin() { // Changed method name from getMax to getMin
        return arr[0];
    }

    public void delete(int i) { // Delete method remains largely the same
        if (i >= size) return;
        arr[i] = Integer.MIN_VALUE; // Use Integer.MIN_VALUE to ensure bubbling up
        // Bubble up to maintain the min-heap property
        while (i != 0 && arr[parent(i)] > arr[i]) { // Changed comparison to maintain min-heap
            swap(i, parent(i));
            i = parent(i);
        }
        removeMin(); // Remove the element that was bubbled to the root
    }

    public int getSize() {
        return size;
    }

    public static void main(String[] args) {
        MinHeap heap = new MinHeap(15); // Changed class name to MinHeap
        heap.insert(3); heap.insert(10); heap.insert(12);
        heap.insert(8); heap.insert(2); heap.insert(14);

        System.out.println("Size: " + heap.getSize());
        System.out.println("Min: " + heap.getMin()); // Changed output to Min

        heap.delete(2); // Deletes the element at index 2

        heap.insert(1); heap.insert(5); // Insert elements
        System.out.println("Size: " + heap.getSize());
        System.out.println("Min: " + heap.getMin()); // Changed output to Min
    }
} */
