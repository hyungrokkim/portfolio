package huffman;

import java.util.HashMap;
import java.util.Map;

public abstract class Node<T> implements Comparable<Node<T>> {
    private Node() {}
    public abstract int getFrequency();
    public abstract Map<T, String> toMap();
    public final int compareTo(final Node<T> o) {
        return Integer.valueOf(getFrequency()).compareTo(o.getFrequency());
    }
    public static final class Simple<T> extends Node<T> {
        public Simple(final T element, final int frequency) {
            this.element = element;
            this.frequency = frequency;
        }
        private final T element;
        private final int frequency;
        public T getElement() {
            return element;
        }
        @Override public int getFrequency() {
            return frequency;
        }
        @Override public Map<T, String> toMap() {
            final Map<T, String> map = new HashMap<T, String>();
            map.put(getElement(), "");
            return map;
        }
    }
    public static final class Compound<T> extends Node<T> {
        private final Node<T> left, right;
        public Node<T> getLeft() {
            return left;
        }
        public Node<T> getRight() {
            return right;
        }
        public Compound(final Node<T> left, final Node<T> right) {
            this.left = left;
            this.right = right;
        }
        @Override public int getFrequency() {
            return left.getFrequency() + right.getFrequency();
        }
        @Override public Map<T, String> toMap() {
            final Map<T, String> map = new HashMap<T, String>();
            final Map<T, String> left = getLeft().toMap();
            for(final T key: left.keySet())
                map.put(key, 0 + left.get(key));
            final Map<T, String> right = getRight().toMap();
            for(final T key: right.keySet())
                map.put(key, 1 + right.get(key));
            return map;
        }
    }
}
