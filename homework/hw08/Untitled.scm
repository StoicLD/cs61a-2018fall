(define (longest-increasing-subsequence lst)
  (define (lis-reversed lst current)
    (cond ((null? lst) current)
      (else (define a (lis-reversed (cdr lst) current))
            (define b (if (or (null? current)
                              (> (car lst) (car current)))
                        (lis-reversed (cdr lst) (cons (car lst) current))
                        nil))
            (if (> (length a) (length b)) a b)
        )
    ))
  (reverse (lis-reversed lst nil))
)

(define-macro (two-m pro)
    (list 'begin pro pro))

(define (two pro)
  (list `begin pro pro))

(define (map fn vals )
  (if (null? vals) vals
      (cons (fn (car vals))
            (map fn (cdr vals)))))

(define-macro (for sym vals expr)
  (list 'map (list `lambda (list `x) expr) vals))

(for x `(2 3 4 5) (* x x))