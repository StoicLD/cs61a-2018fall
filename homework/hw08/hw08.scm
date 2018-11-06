(define (reverse lst)
    'YOUR-CODE-HERE
    (cond
        ((null? lst) ())
        ( (= (length lst) 1) (list (car lst)))
        (else
            (append (reverse (cdr lst)) (list (car lst)))
        ))
)

(define (longest-increasing-subsequence lst)
    'YOUR-CODE-HERE
    (cond
        ((null? lst) ())
        ((= (length lst) 1) lst)
        (else
            (begin
              (define x (cons (car lst)
                            (longest-increasing-subsequence (filter (lambda (x) (< (car lst) x))
                                    (cdr lst)))))
              (define y (longest-increasing-subsequence (cdr lst)))
              (if(> (length x) (length y)) x y)))))


(define (cadr s) (car (cdr s)))
(define (caddr s) (cadr (cdr s)))


; derive returns the derivative of EXPR with respect to VAR
(define (derive expr var)
  (cond ((number? expr) 0)
        ((variable? expr) (if (same-variable? expr var) 1 0))
        ((sum? expr) (derive-sum expr var))
        ((product? expr) (derive-product expr var))
        ((exp? expr) (derive-exp expr var))
        (else 'Error)))

; Variables are represented as symbols
(define (variable? x) (symbol? x))
(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

; Numbers are compared with =
(define (=number? expr num)
  (and (number? expr) (= expr num)))

; Sums are represented as lists that start with +.
(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list '+ a1 a2))))
(define (sum? x)
  (and (list? x) (eq? (car x) '+)))
(define (addend s) (cadr s))
(define (augend s) (caddr s))

; Products are represented as lists that start with *.
(define (make-product m1 m2)
  (cond ((or (=number? m1 0) (=number? m2 0)) 0)
        ((=number? m1 1) m2)
        ((=number? m2 1) m1)
        ((and (number? m1) (number? m2)) (* m1 m2))
        (else (list '* m1 m2))))
(define (product? x)
  (and (list? x) (eq? (car x) '*)))
(define (multiplier p) (cadr p))
(define (multiplicand p) (caddr p))

(define (derive-sum expr var)
  'YOUR-CODE-HERE
  (make-sum
    (derive (addend expr) var)
    (derive (augend expr) var))
)


(define (derive-product expr var)
  'YOUR-CODE-HERE
  (make-sum
    (make-product (derive (multiplier expr) var) (multiplicand expr))
    (make-product (derive (multiplicand expr) var) (multiplier expr)))
)

; Exponentiations are represented as lists that start with ^.
(define (make-exp base exponent)
  'YOUR-CODE-HERE
  (cond
      ((=number? exponent 0) 1)
      ((=number? exponent 1) base)
      ((and (number? exponent) (number? base))
          (expt base exponent) )
      (else
          (list '^ base exponent))
      )
)

(define (base exp)
  'YOUR-CODE-HERE
  (cadr exp)
)

(define (exponent exp)
  'YOUR-CODE-HERE
  (caddr exp)
)

(define (exp? exp)
  'YOUR-CODE-HERE
  (and  (list? exp)
        (number? (exponent exp))
        (eq? '^ (car exp))
        (= (length exp ) 3) )
)

(define x^2 (make-exp 'x 2))
(define x^3 (make-exp 'x 3))

(define (derive-exp exp var)
  'YOUR-CODE-HERE
  (cond
      ((exp? exp)
          (cond ((= (exponent exp) 1) 1)
            (else
              (make-product (exponent exp) (make-exp (base exp) (- (exponent exp) 1)))
              )
            )
        )
      (else 'Error))
)
