import java.awt.Color;

public class Main1 {
    public static void main (String[] args){
        //In addition to calling out the constructor we also have to add the new keyword to create a new tree from our tree class
        // To save the tree variable 
        Tree myFavoriteOakTree = new Tree(101,5,TreeType.OAK);
        Tree TheMapleTree  = new Tree (90,30,TreeType.MAPLE);
        myFavoriteOakTree.talltreeannounce();
        TheMapleTree.talltreeannounce();
         /* System.out.println(myFavoriteOakTree.treetype);
        if (myFavoriteOakTree.heightFt>100){
            System.out.println("This is a tall " + 
            myFavoriteOakTree.treetype  + " tree!");
        if (TheMapleTree.heightFt>100){
            System.out.println("This is a tall tree"); 
        }
        }*/
        System.out.println( Tree.TRUNK_COLOR);
        Tree.announceTree();
        Color myDefaultWhite = Color.WHITE;
        Color myDefaultBlue  = Color.BLUE;
        System.out.println(myFavoriteOakTree.getheightFt());
        System.out.println(TheMapleTree.gettrunkDiameterInches());
        System.out.println(myFavoriteOakTree.gettreetype());
        myFavoriteOakTree.grow();
    }
}
