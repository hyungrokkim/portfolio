package othello;

public class Heuristic implements Evaluator<Tree<Board>> {
    private final Board.State self;
    public Heuristic(final Board.State self) {
        this.self = self;
    }
    public int evaluate(final Tree<Board> tree) {
        final Board board = tree.getValue();
        int value = 0;
        for(int i = 0; i < 8; i++) for(int j = 0; j < 8; j++) {
            int dist = Math.min(Math.min(i, 7 - i), Math.min(j, 7 - i));
            boolean isDiagonal = Math.min(i, 7 - i) == Math.min(j, 7 - i);
            final int sign =
                    board.getState(i, j) == self ? 1
                    : board.getState(i, j) == null ? 0 : -1;
            switch(dist) {
            case 0:
                value += sign * (isDiagonal ? 20 : 5);
            case 1:
                value += sign * (isDiagonal ? 1 : -5);
            case 2:
                value += sign * 2;
            case 3:
                value += sign * 1;
            }
        }
        return value;
    }

}
