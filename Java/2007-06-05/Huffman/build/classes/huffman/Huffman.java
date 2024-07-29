package huffman;

import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;

public final class Huffman {
    private Huffman() {}
    public static final <T> Map<T, String> code(final Map<? extends T, Integer> freq) {
        final Queue<Node<T>> q = new PriorityQueue<Node<T>>();
        for(final T o: freq.keySet())
            q.add(new Node.Simple<T>(o, freq.get(o)));
        while(q.size() > 1)
            q.add(new Node.Compound<T>(q.poll(), q.poll()));
        return q.isEmpty() ? new HashMap<T, String>() : q.poll().toMap();
    }
}
