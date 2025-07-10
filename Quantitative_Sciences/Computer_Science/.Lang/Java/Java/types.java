public class types {       // class name should be equal to file name 

    // final = constant variable 
    // double = float
    final double SHORTPI = 3.14159; 

    // types 
    int var1 = 100; 
    int v2, v3; 
    boolean happy = true; 
    char c1 = 'A'; 
    float fNum = 1.111111111111111F; // precision up to 6 decimal points only 


    // Running the file runs everything in the main function 
    // void means that function doesn't return anything 

    public static void main(String[] args) {

        System.out.println("Hello World"); 

        // Converting from double to string 
        String favNum1 = Double.toString(1.618); 
        String favNum2 = Integer.toString(6); 
        System.out.println(favNum1); 
        System.out.println(favNum2); 

        // Converting from string to whatever: use parseType 
        int favStr1 = Integer.parseInt("10"); 
        double favStr2 = Double.parseDouble("1.567");
        System.out.println(favStr1); 
        System.out.println(favStr2); 
    }
}
