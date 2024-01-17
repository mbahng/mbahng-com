public class exception_handling {

    public static void main(String[] args) {

        // try block 
        try {
            int badInt = 10 / 0; 
        } 
        catch(ArithmeticException ex) {
            System.out.println("Can't divide by 0"); 
            System.out.println(ex.getMessage()); 
            System.out.println(ex.toString()); 
        }

        catch(Exception ex) {
            System.out.println(ex.getMessage()); 
        }

        finally {
            System.out.println("Clearn Up"); 
        }
        
    }
    
    
}
