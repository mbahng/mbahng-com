import java.util.* ; 
import java.util.stream.IntStream;

public class arrays {

    public static void main(String[] args) {
        // create integer array, setting aside 10 values to store ints 
        int[] a1 = new int[10]; 
        a1[0] = 1; // set 0th index to be value 1 
        Arrays.fill(a1, 2); 
        System.out.println(a1[0]); 
        System.out.println(a1.length); 
        System.out.println(Arrays.toString(a1)); 
    
        // String array
        String[] a2 = {"one", "two"}; 
    
        // Sort of like range(1, 11) in python 
        int[] oneTo10 = IntStream.rangeClosed(1, 10).toArray(); 
    
        for (int x : oneTo10) {
          System.out.println(x); 
        }
    
        // Binary search on array for certain value, outputs index of value 
        System.out.println(Arrays.binarySearch(oneTo10, 9)); 
    
        // multiDimensional arrays 
        int[][] a3 = new int[2][2]; 
        String[][] a4 = {{"00", "10"}, 
                         {"01", "11"}}; 
    
        System.out.println(a4[1][1]); 
    
        // copying array into another array 
        int[] a6 = {1, 2, 3}; 
        int[] a7 = Arrays.copyOf(a6, 3);  // which array to copy from and # of values to copy 
    
        // Comparing arrays 
        System.out.println(Arrays.equals(a6, a7)); 
    
        // Sorting arrays
        int[] a8 = {3, 2, 1}; 
        Arrays.sort(a8); 
    
        // Converting arrays to strings
        System.out.println(Arrays.toString(a8)); 
      }
}
