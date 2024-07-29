package kr.hs.ksa.oop;
import java.beans.ConstructorProperties;
import java.io.*;
import java.util.*;

/**
 * Command-line interface for adding students.
 * @author Hyungrok Kim
 */
public class StudentReader {
    public StudentReader() {
        this(System.out, System.in);
    }
    
    @ConstructorProperties({"out", "in"})
    public StudentReader(final OutputStream outputStream,
            final InputStream inputStream) {
        setOut(outputStream);
        setIn(inputStream);
    }
    
    private PrintStream printStream;
    private InputStream inputStream;
    private Scanner scanner;
    
    public List<Student> readStudents(int number) {
        final List<Student> students = new ArrayList<Student>();
        while(number-- > 0)
            students.add(readStudent());
        return students;
    }
    
    public Student readStudent() {
        printStream.print("Name: ");
        printStream.flush();
        String name = "";
        while(name.isEmpty())
            name = scanner.nextLine();
        final EnumMap<Subject, Integer> subjects =
                new EnumMap<Subject, Integer>(Subject.class);
        for(final Subject subject: Subject.values()) {
            printStream.print("Grade for " + subject + ": ");
            printStream.flush();
            int grade = 101;
            while(true) {
                try {
                    grade = scanner.nextInt();
                } catch(final InputMismatchException inputMismatchException) {
                    printStream.println("\nCannot parse grade: must be integer");
                    printStream.flush();
                    scanner.reset();
                    scanner.nextLine();
                    continue;
                }
                if(grade > 100) {
                    printStream.println("\nIncorrect grade: must be <100");
                    printStream.flush();
                } else break;
            }
            subjects.put(subject, grade);
        }
        return new Student(name, subjects);
    }

    public OutputStream getOut() {
        return printStream;
    }

    public void setOut(final OutputStream outputStream) {
        if(outputStream == null)
            throw new NullPointerException("printStream is null");
        printStream = outputStream instanceof PrintStream ?
            (PrintStream) outputStream : new PrintStream(outputStream);
    }

    public InputStream getIn() {
        return inputStream;
    }

    public void setIn(final InputStream inputStream) {
        this.inputStream = inputStream;
        scanner = new Scanner(inputStream);
    }
}
