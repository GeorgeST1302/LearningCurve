package BankingApplication;

public class Mainb{
    public static void main(String[]args){
        BankAccount bankaccount1 = new BankAccount("George",1000);
        BankAccount bankaccount2 = new BankAccount("Mariam",2000);
        bankaccount1.deposit(5000);
        bankaccount2.withdraw(450);
        System.out.println("Account 1 balance is :" + bankaccount1.getBalance());
        System.out.println("Account 2 balance is :" + bankaccount2.getBalance());
     }
}