; scm> (accumulate + 0 5 square)  ; 0 + 1^2 + 2^2 + 3^2 + 4^2 + 5^2
; 55
(define (accumulate combiner start n term)
  (define (helper combiner cur n term)
  (if (<= n 1) 
      (term cur)
      ; (begin (print cur) (print (term cur)) (combiner (term cur) (helper combiner (+ cur 1) (- n 1) term)))))
      (combiner (term cur) (helper combiner (+ cur 1) (- n 1) term))))
  (combiner start (helper combiner 1 n term))
)

; 调用helper的时候处于tail context之中，helper自身也是tail context（if 的最后两个字句）
(define (accumulate-tail combiner start n term)
  (define (helper combiner cur n term total)
    (if (<= n 1) 
      (combiner (term cur) total)
      ; (begin (print cur) (print (term cur)) (combiner (term cur) (helper combiner (+ cur 1) (- n 1) term)))))
      (helper combiner (+ cur 1) (- n 1) term (combiner (term cur) total))))
  (helper combiner 1 n term start)
)

(define (partial-sums stream)
  (define (helper total stream)
      (if (null? stream)
          nil
          (cons-stream (+ (car stream) total) 
            (helper (+ (car stream) total) (cdr-stream stream))))
  )
  (helper 0 stream)
)

(define (rle s)
  (define (helper stream num n)
    (cond ((null? stream) (cons-stream (list num n) nil)) 
        ; ((null? stream) (print (list num n)) (list num n))
        ((= (car stream) num) (helper (cdr-stream stream) num (+ n 1)))       
        ; ((= (car stream) num) (print (list num n)) (print stream) (helper (cdr-stream stream) num (+ n 1)))         
        (else (cons-stream (list num n) (helper stream (car stream) 0)))
        ; (else  (print (list num n)) (cons-stream (list num n) (helper stream (car stream) 0)))
    )
  )
  (if (null? s) nil
    (helper s (car s) 0))
)