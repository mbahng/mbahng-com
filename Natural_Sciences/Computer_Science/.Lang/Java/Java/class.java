public class Warrior {

    // List attributes that a warrior would have
    protected String name = "Warrior"; 
    public int health = 0; 
    public int attkMax = 0; 
    public int blockMax = 0; 

    // Make constructor, which has same name as your class 
    public Warrior() {

    } 

    public Warrior(String name, int health, int attkMax, int blockMax) {
        this.setName(name); 
        this.health = health; 
        this.attkMax = attkMax; 
        this.blockMax = blockMax; 
    }

    public String getName() {
        return name; 
    }

    public void setName(String name) {
        this.name = name; 
    }
}
