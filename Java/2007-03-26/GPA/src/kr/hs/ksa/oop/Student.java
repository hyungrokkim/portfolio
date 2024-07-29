package kr.hs.ksa.oop;
import java.beans.ConstructorProperties;
import java.io.Serializable;
import java.util.*;

/**
 * Represents a student with one or more subjects and corresponding grades.
 * @author Hyungrok Kim
 */
public class Student implements Serializable, Cloneable {
    
    public Student() {
        this("", new EnumMap<Subject, Integer>(Subject.class));
    }
    
    @ConstructorProperties({"name", "subjectMap"})
    public Student(final String name,
            final Map<Subject, Integer> subjectMap) {
        setName(name);
        setSubjectMap(subjectMap);
    }
    
    private String name = "";
    private final Map<Subject, Integer> subjectMap =
            new EnumMap<Subject, Integer>(Subject.class);

    public String getName() {
        return name;
    }

    public void setName(final String name) {
        if(name == null)
            throw new NullPointerException("Null name");
        this.name = name;
    }
    
    public void addSubject(final Subject subject, final int grade) {
        getSubjectMap().put(subject, grade);
    }
    
    public Set<Subject> getSubjectSet() {
        return getSubjectMap().keySet();
    }
    
    public int getGrade(final Subject subject) {
        return getSubjectMap().get(subject);
    }
    
    public boolean isTakingSubject(final Subject subject) {
        return getSubjectMap().containsKey(subject);
    }

    public Map<Subject, Integer> getSubjectMap() {
        return Collections.unmodifiableMap(subjectMap);
    }

    public void setSubjectMap(final Map<Subject, Integer> subjectMap) {
        if(subjectMap == null)
            throw new NullPointerException("Null subjectMap");
        this.subjectMap.clear();
        this.subjectMap.putAll(subjectMap);
    }
    
    public int getTotal() {
        int total = 0;
        for(final Subject subject: getSubjectSet())
            total += getGrade(subject);
        return total;
    }
    
    public double getGPA() {
        if(getSubjectSet().size() == 0)
            throw new java.lang.IllegalStateException("No subjects added");
        return Double.valueOf(getTotal()) / getSubjectSet().size();
    }
    
    @Override public int hashCode() {
        return 31*getName().hashCode() + getSubjectSet().hashCode();
    }
    
    @Override public boolean equals(final Object object) {
        if(!(object instanceof Student))
            throw new IllegalArgumentException(object + " isn't a Student");
        final Student student = (Student) object;
        return student.getName().equals(getName()) &&
                student.getSubjectMap().equals(getSubjectMap());
    }
    
    @Override public Student clone() {
        final Student clone;
        try {
            clone = (Student) super.clone();
        } catch (final CloneNotSupportedException ex) {
            throw new AssertionError(ex);
        }
        clone.setName(getName());
        clone.setSubjectMap(getSubjectMap());
        return clone;
    }
    
    private static final long serialVersionUID = 0;
}
