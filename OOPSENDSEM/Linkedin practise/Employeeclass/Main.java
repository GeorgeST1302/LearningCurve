package Employeeclass;

public class Main {
    
    public static void  main (String [] args){
        String name = "George";
            name.length();
        Employee employee1 = new Employee(80000,"George",19,"USA");
        Employee employee2 = new Employee(90000,"John", 20,"UK");

        employee1.RaiseSalary();
        System.out.println("Employee 1 salary is : "+ employee1.salary);
    }
}