package othello;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

/**
 * Lazily initialized tree.
 * @param T the value this tree holds
 * @author Hyungrok Kim
 */
public final class Tree<T> implements Iterable {
    public Tree(final T value, Generator<T> generator) {
        this.value = value;
        this.generator = generator;
    }
    private final T value;

    public T getValue() {
        return value;
    }
    private final Generator<T> generator;
    private List<Tree<T>> children;
    public List<Tree<T>> getChildren() {
        if(children==null) {
            List<T> childrenValues = generator.generate(value);
            children=new ArrayList<Tree<T>>(childrenValues.size());
            for(final T childValue: childrenValues)
                children.add(new Tree(childValue, generator));
        }
        return Collections.unmodifiableList(children);
    }
    @Override public Iterator iterator() {
        return children.iterator();
    }
    public static interface Generator<T> {
        public List<T> generate(T obj);
    }
}
