/* import java.util.Scanner;

public class Merge {
    public static void mergeSort(int[] a, int i, int e) {
        if (i < e) {
            int m = (i + e) / 2;
            mergeSort(a, i, m);
            mergeSort(a, m + 1, e);
            merge(a, i, m, e);
        }
    }

    public static void merge(int[] a, int i, int m, int e) {
        int n1 = m - i + 1;
        int n2 = e - m;

        int[] L = new int[n1];
        int[] R = new int[n2];

        for (int x = 0; x < n1; ++x)
            L[x] = a[i + x];
        for (int y = 0; y < n2; ++y)
            R[y] = a[m + 1 + y];

        int x = 0, y = 0;
        int k = i;
        while (x < n1 && y < n2) {
            
            if (L[x] <= R[y]) {
                a[k] = L[x];
                x++;
            } else {
                a[k] = R[y];
                y++;
            }
            k++;
        }

        while (x < n1) {
            a[k] = L[x];
            x++;
            k++;
        }

        while (y < n2) {
            a[k] = R[y];
            y++;
            k++;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter the number of elements:");
        int n = scanner.nextInt();

        int[] arr = new int[n];
        System.out.println("Enter the elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
        }

        System.out.println("Given Array");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();

        mergeSort(arr, 0, arr.length - 1);

        System.out.println("\nSorted array");
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
} */