import java.util.* ; 

public class arraylists {
    public static void main(String[] args) {
        // Arraylists are used because they provide easy insertion and deletion 
        ArrayList<String> aL1 = new ArrayList<String>(20); // 20 spaces set aside
        aL1.add("Sue"); 
        aL1.add("bob"); // adding extra elements beyond 20 just extends space

        for (String x : aL1) System.out.println(x); 
    
        // You can also generate an arraylist
        // Construct array list of integers 
        ArrayList<Integer> aL2 = new ArrayList<>(Arrays.asList(1, 2, 3, 4)); 
        for (Integer x : aL2) {
          System.out.println(x); 
        }
    
        System.out.println(aL2.get(1));   // Get value at index 1
        aL2.set(1, 5);    // set value 5 at index 1
        System.out.println(aL2); 
        aL2.remove(3); // remove value at index 3
        aL2.clear();   // delete everything in array list

        // Construct an iterator and cycle through it 
        ArrayList<String> aL3 = new ArrayList<>(Arrays.asList("Bob", "John", "Sam", "Kim")); 
        Iterator it = aL3.iterator(); 
        while (it.hasNext()) {
            System.out.println(it.next()); 
        }
      
      }
}
