;;; General Lisp Utilities

(defun nshuffle (seq)
  "Shuffle a sequence in place and return it"
  ;; Use Fisher-Yates shuffle
  (loop for i from (length seq) above 0
        do (rotatef (elt seq (1- i)) (elt seq (random i))))
  seq)

(defun shuffle (seq)
  "Return a shuffled copy of a sequence"
  (nshuffle (copy-seq seq)))


(defun load-dictionary (filename)
  "Read data from file and return alist of word-definition pairs"
  (with-open-file (file filename)
    (loop for word = (read-line file nil)
          for defn = (read-line file nil)
          until (null word)
          collect (cons word defn))))

(defun load-dictionary-relative (filename)
  "Same as LOAD-DICTIONARY, with relative filenames"
  (load-dictionary (pathname filename)))

(defun test (dict)
  "Test an alist of word-definition pairs"
  (let ((missed
        (loop for (word . defn) in dict
          do (format t "~&What word means '~a'? " defn)
             (finish-output)
          if (equal (read-line) word)
            do (format t "~&Correct!~&")
          else
            collect (cons word defn)
            and do (format t "~&Wrong! The answer was '~a'.~&" word))))
    (when missed
      (format t "~&You missed ~r word~:p.~&" (length missed))
      (test missed))))

; association list of word / definition pairs
(defparameter *dict* nil)


(defun hangman (word)
  (let ((partial-word (make-string (length word)
                                   :initial-element #\_)))
    (loop for input = nil then (prog1 (read-char) (clear-input))
          while (find #\_ partial-word)
          count (and input (null (find input word)))
          do
            (loop for letter across word
                  for i from 0 below (length word)
                  when (eql letter input)
                    do (setf (elt partial-word i) input))
            (format t "~&~a " partial-word))))

(defun prompt ()
  (princ "Which file to open? ")
  (finish-output)
  (setq *dict* (load-dictionary (read-line)))
  (loop
   (format t "~&TESTER> ")
   (case (read)
     (:t (test (shuffle *dict*)))
     (:h (format t "~%You missed ~a.~%"
                 (hangman (car (elt *dict*
                                    (random (length *dict*)))))))
     (:q (return)))))
