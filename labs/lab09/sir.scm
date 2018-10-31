(define (repeat k fn )
    (if(> k 1)
        (begin (fn) (repeat (- k 1) fn))
        (fn)
    )
)

(define (tri fn)
    (repeat 3 (lambda () (fn) (lt 120)))
)

(define (seir d k)
    (tri
        (lambda ()
            (if
                (= k 1)
                (fd d)
                (draw d k)
            )
        )
    )
)

(define (draw d k)
    (seir (/ d 2) (- k 1))
    (penup)
    (fd d)
    (pendown)
)

(seir 500 6)
