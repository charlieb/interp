(define 'make-adder 
  (lambda (n)
    (lambda (x)
      (add n x))))

(let ((add5 (make-adder 5)))
  (add5 10))

