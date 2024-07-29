package lab10dot2;

import java.util.AbstractSequentialList;
import java.util.Collection;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public final class DoublyLinkedList<E> extends AbstractSequentialList<E> {
    public DoublyLinkedList() {}
    public DoublyLinkedList(final Collection<? extends E> c) {
        addAll(c);
    }
    private Node<E> head;
    private int size;
    private static final class Node<E> {
        private Node<E> previous;
        private Node<E> next;
        private E value;
    }
    @Override public ListIterator<E> listIterator(final int theIndex) {
        return new ListIterator<E>() {
            private int index = theIndex;
            private Node<E> next, previous;
            {
                if(index < 0 || index > size()) throw new IndexOutOfBoundsException();
                next = head;
                int counter = index;
                while(counter-- != 0) {
                    next = next.next;
                    previous = previous == null ? head : previous.next;
                }
            }
            private Node<E> jumpedOver;
            public boolean hasNext() {
                return next != null;
            }
            public E next() {
                if(!hasNext()) throw new NoSuchElementException();
                previous = jumpedOver = next;
                next = next.next;
                index++;
                return jumpedOver.value;
            }
            public boolean hasPrevious() {
                return previous != null;
            }
            public E previous() {
                if(!hasPrevious()) throw new NoSuchElementException();
                next = jumpedOver = previous;
                previous = previous.previous;
                index--;
                return jumpedOver.value;
            }
            public int nextIndex() {
                return index;
            }
            public int previousIndex() {
                return index - 1;
            }
            public void remove() {
                if(jumpedOver == null) throw new IllegalStateException();
                if(jumpedOver == previous) index--;
                previous = jumpedOver.previous;
                next = jumpedOver.next;
                if(previous != null) previous.next = next;
                if(next != null) next.previous = previous;
                jumpedOver = null;
                size--;
                if(previous == null) head = next;
            }
            public void set(final E e) {
                if(jumpedOver == null) throw new IllegalStateException();
                jumpedOver.value = e;
            }
            public void add(final E e) {
                final Node<E> added = new Node<E>();
                if(previous == null) head = added;
                if(previous != null) previous.next = added;
                added.previous = previous;
                previous = added;
                if(next != null) next.previous = previous;
                previous.next = next;
                previous.value = e;
                index++;
                jumpedOver = null;
                size++;
            }
        };
    }
    @Override public int size() {
        return size;
    }
    public void addFirst(final E e) {
        listIterator().add(e);
    }
    public void addLast(final E e) {
        add(e);
    }
    public E getFirst() {
        return get(0);
    }
    public E getLast() {
        return get(size() - 1);
    }
    public E removeFirst() {
        return remove(0);
    }
    public E removeLast() {
        return remove(size() - 1);
    }
    public void printAllElement() {
        for(final E e: this) System.out.println(e);
    }
}