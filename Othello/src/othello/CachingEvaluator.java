package othello;

import java.util.IdentityHashMap;

// Assumes that the evaluation for T does not change
public class CachingEvaluator<T> implements Evaluator<T> {
    public CachingEvaluator(final Evaluator evaluator) {
        this.evaluator = evaluator;
    }
    private final Evaluator evaluator;
    private final IdentityHashMap<T, Integer> cache =
            new IdentityHashMap<T, Integer>();
    @Override public int evaluate(final T obj) {
        if(!cache.containsKey(obj)) {
            cache.put(obj, evaluator.evaluate(obj));
        }
        return cache.get(obj);
    }
}
