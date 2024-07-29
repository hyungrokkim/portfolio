package kr.hs.ksa.oop;
import java.beans.ConstructorProperties;
import java.io.PrintStream;
import java.util.*;

/**
 * Nicely formats a list of students and their grades
 * @author Hyungrok Kim
 */
public class StudentListFormatter {
    
    public StudentListFormatter() {
        this(new ArrayList<Student>());
    }
    
    @ConstructorProperties({"students"})
    public StudentListFormatter(final List<Student> students) {
        this(students,
                  "0123456789012345678901234567890123456789012345678901234\n"
                + "================== Student Points =====================\n"
                + "0123456789012345678901234567890123456789012345678901234\n");
    }
    
    @ConstructorProperties({"students", "header"})
    public StudentListFormatter(final List<Student> students,
            final String header) {
        setHeader(header);
        setStudents(students);
    }
    
    public void print(final PrintStream printStream) {
        printStream.print(getHeader());
        printStream.format("%6s ", "Name");
        for(final Subject subject: Subject.values())
            printStream.format("%11s ", subject);
        printStream.println("Total          Mean");
        for(final Student student: students) {
            printStream.format("%-6s ", student.getName());
            for(final Subject subject: Subject.values())
                printStream.format(" %2d         ",
                    student.isTakingSubject(subject) ?
                    student.getGrade(subject) : "");
            printStream.format("%2d             %4.1f", student.getTotal(),
                    student.getGPA());
            printStream.println();
        }
    }
    
    public void print() {
        print(System.out);
    }
    
    private String header;
    
    private List<Student> students;

    public String getHeader() {
        return header;
    }

    public void setHeader(final String header) {
        if(header == null)
            throw new NullPointerException("header is null");
        this.header = header;
    }

    public List<Student> getStudents() {
        return Collections.unmodifiableList(students);
    }

    public void setStudents(final List<Student> students) {
        if(students == null)
            throw new NullPointerException("students is null");
        this.students = new ArrayList<Student>(students);
    }
    
    public void addStudent(final Student student) {
        if(student == null)
            throw new NullPointerException("attempting to add null Student");
        students.add(student);
    }
    
    public boolean removeStudent(final Student student) {
        if(student == null)
            throw new NullPointerException("attempting to remove null Student");
        return students.remove(student);
    }
}
