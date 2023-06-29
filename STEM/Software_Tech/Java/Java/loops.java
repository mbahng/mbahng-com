import java.util.* ; 

public class loops {
    
    public static void main(String[] args) {
        
        // for loops 
        for (int i = 0; i < 5; i++) {
            System.out.println(i); 
        }
    
        int wL = 0; 
        while (wL < 20) {
            if (wL % 2 == 0) {
                System.out.println(wL); 
                wL ++; 
                continue; 
            } 

            if (wL >= 10){
                break; 
            }
            wL++;  
        }
    }

}
