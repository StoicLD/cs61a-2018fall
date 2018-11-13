;;; Test cases for Scheme.
;;;
;;; In order to run only a prefix of these examples, add the line
;;;
;;; (exit)
;;;
;;; after the last test you wish to run.

;;; ********************************
;;; *** Add your own tests here! ***
;;; ********************************
; BEGIN PROBLEM 0

;;; TEST for Q13
(begin (+ 1 1) (+ 2 3) 4)
; expect 4

(define (zip pairs)
  ; (print pairs)
  (cond
    ((null? pairs) (list nil nil))
    ((null? (car pairs)) nil)
    (else (cons (map car pairs) 
                (zip (map cdr pairs)))
    )
  )
)

(zip (list '(a b) '(1 2)))
; expect ((a 1) (b 2))
; END PROBLEM 0
(exit)
