package Employeeclass;
import Employeeclass.*;
// Create an employee class with properties name , age . salary ,location 
// Behavior :raise salary
// which all members are suppose to be static and non static
// Create a main class for building instances 
// Give one Employee a raise
// Display the salary of both the employees
public class Employee{

    double salary;
    String name;
    int age ;
    String location;

    void RaiseSalary(){
        this.salary = this.salary *0.2;
    }
    Employee (double salary,String name,int age,String location){
        this.salary = salary;
        this.name = name;
        this.age = age;
        this.location = location ;

    }
    

}