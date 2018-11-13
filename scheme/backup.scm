(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.
; ((2 3) (4 5)) --> ((1 2 3) (1 4 5))

(define (cons-all first rests)
  (map (lambda (x) (cons first x)) rests)
)

(define (bool? x) 
  (if (or (eq? x true) (eq? x false)) true false)
)

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

; (define (reverse s)
;   (define (helper s reversed)
;       (cond
;           ((null? s) reversed)
;           (else (helper (cdr s) 
;                 (cons (car s) 
;                       reversed)))))
;   (helper s nil))

;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
    (define (with-index s index)
     (if (null? s) 
      ()
      (cons (list index (car s)) (with-index (cdr s) (+ index 1)))
     ))
  (with-index s 0)
)
; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (cons-all first rests)
  (map (lambda (x) (cons first x)) rests)
)
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
  (cond
    ((or (null? denoms) (< total 0)) nil)
    ((= 0 total) (cons nil nil))
    (else
      (append 
        (cons-all (car denoms) (list-change (- total (car denoms)) denoms))
        (list-change total (cdr denoms))
      )
    )
  )
)

(list-change 10 '(25 10 5 1))
; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         (list expr)
         ; END PROBLEM 19
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (form params)
           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19           
           (print values)
           (print body)
           (define pairs (zip values))
           (print pairs)
           (list (list 'lambda (car pairs) body) (cdar pairs))
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )))
