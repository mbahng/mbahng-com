public class conditionals {
    public static void main(String[] args) {
        int age = 12; 

        if ((age >= 5 ) && (age <= 6)) {
            System.out.println("Go to Kindergarten"); 
        } else if ((age >= 7) && (age <= 13)) {
            System.out.println("Go to Middle School"); 
        } else if ((age >= 14) && (age <= 18)) {
            System.out.println("Go to high school"); 
        } else {
            System.out.println("Stay home"); 
        }

        System.out.println("true || false : " + (true || false)); 
        System.out.println("!true = " + (!true)); 

        // Ternary operators 
        boolean canVote = (age >= 18) ? true : false;
        System.out.println(canVote); 

        // Using cases 
        String lang = "France"; 
        switch (lang) {
        case "Chile" : case "Cuba" : 
            System.out.println("Hola"); 
            break; 
        case "France" : 
            System.out.println("Bonjour"); 
            break; 
        case "Japan" : 
            System.out.println("Konnichiwa"); 
            break; 
        default: 
            System.out.println("Hello"); 
        }

    }
}
