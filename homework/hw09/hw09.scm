; scm> (list-of (* x x) for x in '(3 4 5) if (odd? x))
; (9 25)
; scm> (list-of 'hi for x in '(1 2 3 4 5 6) if (= (modulo x 3) 0))
; (hi hi)
; scm> (list-of (car e) for e in '((10) 11 (12) 13 (14 15)) if (list? e))
; (10 12 14)
(define (map fn expr)
  (if (null? expr)
    ()
    (cons 
      (fn (car expr))
      (map fn (cdr expr)))))

(define-macro (list-of map-expr for var in lst if filter-expr)
  'YOUR-CODE-HERE
  (list 'map (list 'lambda (list var) map-expr) 
          (list 'filter (list 'lambda (list var) filter-expr) lst))
)