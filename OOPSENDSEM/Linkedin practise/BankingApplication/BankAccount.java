package BankingApplication;
import BankingApplication.*;
public class BankAccount{
    private String owner;
    private double balance;
    public BankAccount(String owner, int startingBalance){
        this.owner = owner;
        this.balance = Math.max(0,startingBalance);
        
    }
    public String getOwner(){
        return owner;

    }
    public double getBalance(){
        return balance;
    }
    public double deposit(double amount){
        if (amount>0){
            this.balance = this .balance + amount;
            return amount;
        }
        return 0;
    }
    public double withdraw(double amount){
        if(amount>0 && amount<= balance){
            this.balance = this.balance - amount;
            return amount;
        }
        return 0 ;
    }

    }
