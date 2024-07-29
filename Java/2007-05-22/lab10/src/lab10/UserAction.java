package lab10;

import java.util.Vector;

public enum UserAction {
  CAPACITY {
    @Override public void perform(Vector<Integer> vector) {
      System.out.println(vector.capacity());
    }
  }
  , SIZE { 
    @Override public void perform(Vector<Integer> vector) {
      System.out.println(vector.size());
    }
  }, ADD { 
    @Override public void perform(Vector<Integer> vector) {
      vector.add(Integer.decode(System.console().readLine("Enter a number: ")));
    }
  }, GET_REMOVE { 
    @Override public void perform(Vector<Integer> vector) {
      vector.remove(Integer.parseInt(System.console().readLine("Enter a number: ")));
    }
  }, GET { 
    @Override public void perform(Vector<Integer> vector) {
      System.out.println(vector.get(Integer.parseInt(System.console().readLine("Enter a number: "))));
    }
  }, INDEX_OF { 
    @Override public void perform(Vector<Integer> vector) {
      System.out.println(vector.indexOf(Integer.decode(System.console().readLine("Enter a number: "))));
    }
  }, FIND_REMOVE { 
    @Override public void perform(Vector<Integer> vector) {
      vector.remove(Integer.decode(System.console().readLine("Enter a number: ")));
    }
  }, REPLACE { 
    @Override public void perform(Vector<Integer> vector) {
      vector.set(Integer.parseInt(System.console().readLine("Enter a number: ")),
              Integer.decode(System.console().readLine("Enter another number: ")));
    }
  }, ADD_BEFORE { 
    @Override public void perform(Vector<Integer> vector) {
      vector.add(Integer.parseInt(System.console().readLine("Enter a number: ")),
              Integer.decode(System.console().readLine("Enter another number: ")));
    }
  }, ADD_AFTER { 
    @Override public void perform(Vector<Integer> vector) {
      vector.add(Integer.parseInt(System.console().readLine("Enter a number: "))+1,
              Integer.decode(System.console().readLine("Enter another number: ")));
    }
  }, CLEAR { 
    @Override public void perform(Vector<Integer> vector) {
      vector.clear();
    }
  }, PRINT {
    public void perform(Vector<Integer> vector) {
      System.out.println(vector);
    }
  }, QUIT { 
    @Override public void perform(Vector<Integer> vector) {
      System.exit(0);
    }
  };
  public void perform(Vector<Integer> list) {};
}