package kr.hs.ksa.oop;

/**
 * Represents a school subject.
 * @author Hyungrok Kim
 */
public enum Subject {
    DATA_STRUCTURES {
        @Override public String toString() {
            return "DataStruct";
        }
    }, ALGORITHMS {
        @Override public String toString() {
            return "Algorithms";
        }
    }
}
