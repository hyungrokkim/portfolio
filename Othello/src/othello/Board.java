package othello;

import java.util.ArrayList;
import java.util.List;

/**
 * An immutable board.
 * @author Hyungrok Kim
 */
public final class Board {
    // represent empty with null value
    public enum State {
        WHITE, BLACK;
        public final State opponent() {
            return this == WHITE ? BLACK : WHITE;
        }
    }
    private final State[][] values;
    private final State turn;
    private Board(final State[][] values, final State turn) {
        this.values = values;
        this.turn = turn;
    }
    public static final Board INITIAL;
    static {
        final State[][] values = new State[8][8];
        values[3][4] = values[4][3] = State.WHITE;
        values[3][3] = values[4][4] = State.BLACK;
        INITIAL = new Board(values, State.BLACK);
    }
    public State getState(int x, int y) {
        return values[x][y];
    }
    private boolean isValid(final int i) {
        return i >= 0 && i < 8;
    }
    public Board move(final int x, final int y) {
        if(!isValid(x) || isValid(y))
            throw new IndexOutOfBoundsException("invalid indices: " + x + ", " + y);
        for(int i=-1; i<=1; i++) for(int j=-1; j<=1; j++) {
            for(int x2=x+i, y2=y+j; isValid(x2) && isValid(y2); x2+=i, y2+=j) {
                if(values[x2][y2] == turn && (x2 != x+i || y2 != y+j)) {
                    final State[][] newValues = new State[8][8];
                    for(int k = 0; k < 8; k++ ) {
                        newValues[k] = values[k].clone();
                    }
                    for(int x3 = x+i, y3 = y+j; x3 != x2 || y3 != y2; x3+=i, y3+=j) {
                        newValues[x3][y3] = turn;
                    }
                    return new Board(newValues, turn.opponent());
                }
            }
        }
        throw new IllegalStateException("illegal play: " + x + ", " + y);
    }
    
    @Override public String toString() {
        final StringBuilder stringBuilder = new StringBuilder();
        for(int i = 0; i < 7; i++) {
            for(int j = 0; j < 7; j++) {
                switch(getState(i, j)) {
                case WHITE:
                    stringBuilder.append('O');
                    break;
                case BLACK:
                    stringBuilder.append('#');
                    break;
                default:
                    stringBuilder.append('_');
                }
                stringBuilder.append(' ');
            }
            stringBuilder.append('\n');
        }
        return stringBuilder.toString();
    }
    
    public static final class Generator implements Tree.Generator<Board> {
        @Override public List<Board> generate(final Board board) {
            final List<Board> possibleNextBoards =
                    new ArrayList<Board>();
            for(int x = 0; x < 8 ; x++) for(int y = 0; y < 8; y++) {
                try {
                    possibleNextBoards.add(board.move(x, y));
                } catch (final IllegalStateException e) {}
            }
            return possibleNextBoards;
        }
    }
}
