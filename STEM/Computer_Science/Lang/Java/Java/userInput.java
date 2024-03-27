import java.util.* ; 

public class userInput {
    
    static Scanner sc = new Scanner(System.in); 

    public static void main(String[] args) {
        System.out.print("Enter Name : "); 
        
        // conditional checks if input is string 
        if (sc.hasNextLine()) {
            String userName = sc.nextLine(); 
            System.out.println("Hello " + userName); 
        }
    }
}
