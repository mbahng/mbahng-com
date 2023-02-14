import java.util.* ; 

public class linkedlists {
    public static void main(String[] args) {

        // Instantiate linked list
        LinkedList<Integer> iL1 = new LinkedList<Integer>(); 

        // Add one at a time and multiple elements with array
        iL1.add(1); iL1.add(2); iL1.add(3); 
        iL1.addAll(Arrays.asList(1, 2, 3, 4)); 
        iL1.addFirst(0); // Add to first 

        // Getter and setter methods (Set 0th index value to 2 )
        System.out.println("0th Index : " + iL1.get(0)); 
        iL1.set(0, 2); 
        System.out.println("0th Index : " + iL1.get(0)); 

        // Check if linked list contains an element 
        System.out.println("Contains 4? : " + iL1.contains(4)); 

        // Check the index of element 
        System.out.println("Index of 4 : " + iL1.indexOf(4)); 
        
        // Get length of Linked list 
        System.out.println(iL1.size()); 

        // Remove the 1st index 
        iL1.remove(1); 
        System.out.println(iL1.get(1)); 

        for (Integer x : iL1) {
            System.out.print(x + " "); 
        }

        // Convert Linked list to array. Object array is most general 
        Object[] arr = iL1.toArray(); 

    }
}
