(define repeat k fn )
    (if(> k 1)
        ((fn) (repeat (- k 1) fn))
        (fn)
    )

(define (draw depth)
    ((lambda () (lt 120) (penup) (fd depth) (pendown)))
)

(define (draw_all x d)
    (if (= x 1)
        (draw d)
        ((lambda () (draw d) (draw_all (- x 1) d)))
    )
)

(draw_all 33 64)
