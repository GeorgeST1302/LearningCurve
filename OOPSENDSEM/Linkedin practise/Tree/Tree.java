import java.awt.Color;
public class Tree { 
    protected static Color TRUNK_COLOR = new Color(102,51,0);
    private double heightFt; // Instance variables
    private double trunkDiameterInches;
    private TreeType treetype; //  We are using the enum TreeType here instead of a string to represent the type of tree.
//To use enum we have to use the datatype TreeType
    public Tree(double heightFt,double trunkDiameterInches,TreeType treetype) {
        this.heightFt = heightFt;
        this.trunkDiameterInches = trunkDiameterInches;
        this.treetype = treetype;
    }

    public double getheightFt(){ // with the access public it is a static method with public it's a access modifier which basically it can be accesed from thhe same class within 
        return heightFt;
    }
    public double gettrunkDiameterInches(){
        return trunkDiameterInches;
    }

    public TreeType gettreetype(){
        return treetype;
    }
    public void setTrunkDiameterInches (){
        this.trunkDiameterInches = trunkDiameterInches ;
    }
        public void grow(){
        this.heightFt = this.heightFt + 10;
        this.trunkDiameterInches = this.trunkDiameterInches +1;
    
 
    }
    static void announceTree(){
        System.out.println("Look out for that tree!"+ TRUNK_COLOR + "tree!");
    }
public void talltreeannounce(){
    if (this.heightFt> 100){
        System.out.println(" This is a tall " + this.treetype + " tree !");
    }
  
  
}
}

