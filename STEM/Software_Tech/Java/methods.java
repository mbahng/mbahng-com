import java.util.* ; 

public class methods {

    // public means that anybody with access to the class can call the methods

    public static int getSum(int x, int y) {
        return x + y; 
    }

    public static void changeMe(int cNum) {
        cNum = 10; 
    }

    // method with variable number of arguments
    public static int getSum2(int ... nums) {
        int sum = 0; 
        for (int x : nums) {
            sum += x; 
        }
        return sum; 
    }

    // returning an array 
    public static int[] getNext2(int x) {
        int[] vals = new int[2]; 
        vals[0] = x + 1; 
        vals[1] = x + 2; 
        return vals; 
    }

    // Return a general list of objects (most general class) 
    static List<Object> getRandList() {
        String name = "Muchang"; 
        int age = 21; 
        return Arrays.asList(name, age); 
    }

    // Recursive function that calls itself 
    static int factorial(int num) {
        // always have condition where function should stop 
        if (num == 1) {
            return 1; 
        } else {
            int result = num * factorial(num - 1); 
            return result; 
        }
    }

    public static void main(String[] args) {
        System.out.println("5 + 4 = " + getSum(5, 4)); 

        int cNum = 0; 
        changeMe(cNum); // does not actually change since scope is limited 
        System.out.println("cNum = " + cNum); 

        System.out.println(getSum2(1, 2, 3, 4)); 

        int[] multVA = getNext2(5); 
        for (int x : multVA) System.out.println(x); 

        List<Object> randList = getRandList(); 
        System.out.println(randList); 

        System.out.println("4! = " + factorial(4)); 

    }
}
