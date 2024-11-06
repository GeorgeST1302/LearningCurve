public class ReverseNumber {

    // Recursive method to reverse a number
    public static int reverse(int num) {
        // Base case: if the number is a single digit, return the number
        if (num < 10) {
            return num;
        }
        // Recursive case: get the last digit and add it to the reversed number of the remaining digits
        int numOfDigits = (int) Math.log10(num); // Find the number of digits in the number
        return (num % 10) * (int) Math.pow(10, numOfDigits) + reverse(num / 10);
    }

    // Method to check if a number is a palindrome
    public static boolean isPalindrome(int num) {
        return num == reverse(num);
    }

    public static void main(String[] args) {
        int number = 12321; // Example number

        // Reverse the number
        int reversedNumber = reverse(number);
        System.out.println("Reversed Number: " + reversedNumber);

        // Check if the number is a palindrome
        if (isPalindrome(number)) {
            System.out.println(number + " is a palindrome.");
        } else {
            System.out.println(number + " is not a palindrome.");
        }
    }
}