
; (define (list-change total denoms)
;   ; BEGIN PROBLEM 18
;   (define (helper remain denoms sub-list)
;       (cond 
;           ((null? denoms) nil)
;           ;这里return ((5 4 3 2 1)) 这种形式，也就是一个list里面只有一个元素，这个元素就是一个list
;           ((= remain 0) (list sub-list))
;           ; 这里开始tree recursive
;           ((< remain (car denoms)) (helper remain (cdr denoms) sub-list))
;           (else 
;               (append 
;                   (helper (- remain (car denoms)) denoms (cons (car denoms) sub-list)) 
;                   (helper remain (cdr denoms) sub-list))
;           )
;       )
;   )
;   (helper total denoms nil)  
; )

; (define (list-change total denoms) 
;   (define (helper total denoms current-sum-list)
;       (cond 
;           ((null? denoms) nil)
;           ((zero? total) (list current-sum-list))
;           ((> (car denoms) total) (helper total 
;                                             (cdr denoms) 
;                                             current-sum-list))
;           (else (append
;                     (helper (- total (car denoms)) 
;                             denoms 
;                             (cons (car denoms) 
;                                   current-sum-list)) 
;                     (helper total 
;                             (cdr denoms) 
;                             current-sum-list)))))
; (map reverse (helper total denoms nil)))