import java.util.ArrayList;
import java.util.Arrays;

public class Heaps {

    // The following function heapifies the elements
    private static void heapify(int[] arr, int n, int i, boolean isMaxHeap) {
int largest = i; // root element 
 int left = 2 * i + 1; // left node = 2*i + 1
 int right = 2 * i + 2; // right node = 2*i + 2
if (left < n && (isMaxHeap ? arr[left] > arr[largest] : arr[left] < arr[largest])) {
    
largest = left;
}
    if (right < n && (isMaxHeap ? arr[right] > arr[largest] : arr[right] < arr[largest])) {
             largest = right;
    }
 if (largest != i) {
     int swap = arr[i];
  arr[i] = arr[largest];
 arr[largest] = swap;
     heapify(arr, n, largest, isMaxHeap);
        }
    }

    // Build heap function
    private static void buildHeap(int[] arr, boolean isMaxHeap) {
        for (int i = arr.length / 2 - 1; i >= 0; i--) {
            heapify(arr, arr.length, i, isMaxHeap);
        }
    }

    void insert(ArrayList<Integer> hT, int newNum) {
        hT.add(newNum);
        int index = hT.size() - 1;

        // Bubble up to maintain heap property
        while (index > 0) {
            int parentIndex = (index - 1) / 2;
            if ((hT.get(parentIndex) < hT.get(index) && isMaxHeap) ||
                (hT.get(parentIndex) > hT.get(index) && isMaxHeap)) {
                // Swap
                int temp = hT.get(parentIndex);
                hT.set(parentIndex, hT.get(index));
                hT.set(index, temp);
                index = parentIndex;
            } else {
                break;
            }
        }
    }

    // Print the heap
    private static void printHeap(int[] arr) {
        int levels = (int) (Math.log(arr.length) / Math.log(2)) + 1;
        for (int i = 0; i < levels; i++) {
            int start = (1 << i) - 1; // 2^i - 1
            int end = Math.min(start + (1 << i), arr.length); // 2^i nodes in this level
            for (int j = start; j < end; j++) {
                System.out.print(arr[j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void main(String[] args) {
        int[] numbers = {3, 1, 4, 1, 5, 9, 2, 6, 5};

    int[] maxHeap = Arrays.copyOf(numbers, numbers.length);
        buildHeap(maxHeap, true);
        System.out.print("Max-Heap:");
        printHeap(maxHeap);

           int[] minHeap = Arrays.copyOf(numbers, numbers.length);
  buildHeap(minHeap, false);
  System.out.print("Min-Heap:");
     printHeap(minHeap);
 }
}
