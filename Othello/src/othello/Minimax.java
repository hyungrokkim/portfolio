package othello;

import java.util.List;

/**
 * An evaluator using the minimax algorithm.
 * @author hk
 */
public class Minimax<T> implements Evaluator<Tree<T>> {
    private final int depth;
    private final int flip;
    private final Evaluator<Tree<T>> base;
    public Minimax(final int depth, final Evaluator<Tree<T>> base) {
        this(depth, base, 1);
    }
    private Minimax(final int depth, final Evaluator<Tree<T>> base,
            final int flip) {
        this.depth = depth;
        this.base = base;
        this.flip = flip;
    }
    public int evaluate(final Tree<T> tree) {
        final List<Tree<T>> children = tree.getChildren();
        if(children.isEmpty() || depth == 0) return base.evaluate(tree);
        
        int best = Integer.MIN_VALUE;
        final Evaluator<Tree<T>> nextEvaluator =
                new Minimax(depth - 1, base, -flip);
        for(final Tree<T> child: tree.getChildren()) {
            int childEvaluation = nextEvaluator.evaluate(child);
            if(flip * best < flip * childEvaluation)
                best = childEvaluation;
        }
        return best;
    }
}
