/**
 * The SmaAndLar class contains a method to find the smallest and largest elements in an array.
 * 
 * The main method initializes an array of integers and then iterates through the array to find
 * the smallest and largest elements. It prints the smallest and largest elements to the console.
 * 
 * Logic:
 * 1. Initialize the smallest and largest variables with the first element of the array.
 * 2. Iterate through the array starting from the second element.
 * 3. For each element, check if it is smaller than the current smallest element. If so, update the smallest variable.
 * 4. For each element, check if it is larger than the current largest element. If so, update the largest variable.
 * 5. After the loop, print the smallest and largest elements.
 */
public class smaand {
    public static void main(String[] args) {
        int[] array = {3, 5, 7, 2, 8, -1, 4, 10, 12};
        
        int smallest = array[0];
        int largest = array[0];
        
        for (int i = 1; i < array.length; i++) {
            if (array[i] < smallest) {
                smallest = array[i];
            }
            if (array[i] > largest) {
                largest = array[i];
            }
        }
        
        System.out.println("Smallest element: " + smallest);
        System.out.println("Largest element: " + largest);
    }
}