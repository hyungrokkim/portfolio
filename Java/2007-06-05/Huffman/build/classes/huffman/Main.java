package huffman;

import java.util.HashMap;
import java.util.TreeMap;
import java.util.Map;

public final class Main {
    private Main() {}
    public static void main(final String... args) {
        final Map<Character, Integer> frequencies =
                new HashMap<Character, Integer>();
        frequencies.put('A', 15);
        frequencies.put('B', 5);
        frequencies.put('C', 12);
        frequencies.put('D', 17);
        frequencies.put('E', 10);
        frequencies.put('F', 25);
        System.out.println(
                new TreeMap<Character, String>(Huffman.code(frequencies)));
    }
}
