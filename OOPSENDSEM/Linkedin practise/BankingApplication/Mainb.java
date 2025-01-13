package BankingApplication;

public class Mainb {
    public static void main (String []args){
        BankAccount account1 =  new BankAccount("George",90020);
        BankAccount account2 =  new BankAccount("Mariam",10000);
        account1.deposit(9000);
        account2.withdraw(2000);
    }
    
}
