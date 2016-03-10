(progn 

(define (quote true) 1)
(define (quote false) 0)

(define (quote <) (lambda (x y)
            (if (eq 0 x) true
              (if (eq 0 y) false
                (< (add -1 x)
                   (add -1 y))))))

(define (quote fib) (lambda (n)
              (if (< n 2)
                1
                (add (fib (add n -1))
                     (fib (add n -2))))))

(fib 5)

)
