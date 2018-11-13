(define (list-change total denoms) 
  (define (helper total denoms current-sum-list)
      (cond 
          ((null? denoms) nil)
          ((zero? total) (list current-sum-list))
          ((> (car denoms) total) (helper total 
                                            (cdr denoms) 
                                            current-sum-list))
          (else (append
                    (helper (- total (car denoms)) 
                            denoms 
                            (cons (car denoms) 
                                  current-sum-list)) 
                    (helper total 
                            (cdr denoms) 
                            current-sum-list)))))
  (map reverse (helper total denoms nil)))