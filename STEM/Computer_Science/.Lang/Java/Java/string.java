public class string {
    
    public static void main(String[] args ) {
        String name = "Muchang"; 
        String fName = name + " Bahng"; 
        fName += " is my name."; 
        String drsDog = "K" + 9;  // Automatic conversion of ints to strings 

        System.out.println(drsDog); 

        System.out.println(fName.charAt(0));  // output char at index 0 
        System.out.println(fName.contains("Muchang")); // check whether it contains substring 
        System.out.println(fName.indexOf("Muchang")); 
        System.out.println(fName.length()); 

        // Comparing strings. DO NOT use == 
        System.out.println("dog equals cat : " + ("dog".equals("cat"))); 
        
        // Comparing strings disregarding case 
        System.out.println("dog equals cat : " + ("dog".equalsIgnoreCase("cat"))); 

        // Replace substrings 
        System.out.println(fName.replace("Muchang", "Bob")); 

        // Get substrings
        System.out.println(fName.substring(0, 7)); 

        // Iterate every character through string 
        for (int i = 0; i < 7; i++) {
            System.out.println(fName.charAt(i)); 
        }

        // Iterate through every word of string using split 
        for (String x : fName.split(" ")) {
            System.out.println(x); 
        }

        // Trim function removes whitespace from beginning and end 
        String bad_string = " efad "; 
        System.out.println(bad_string.trim()); 

        // Convert all to uppercase or lowercase 
        String low = "lowercase"; 
        String up = "UPPERCASE"; 
        System.out.println(low.toUpperCase() + " " + up.toLowerCase()); 

        // StringBuilder types allow you to modify strings efficiently 
        StringBuilder sb = new StringBuilder("I'm a string builder."); 
        System.out.println(sb.length());    
        System.out.println(sb.capacity());    // size that is set aside for str builder 
        System.out.println(sb.append(" Yeah")); 
        System.out.println(sb.insert(6, "Big ")); // insert string at index 
        System.out.println(sb.replace(6, 9, "wig")); // replacing substrings
        System.out.println(sb.substring(6, 10)); 
        System.out.println(sb.delete(6, 10)); 
        System.out.println(sb.charAt(4)); 
        System.out.println(sb.indexOf("i")); // gives specific index of string 
    }
}
