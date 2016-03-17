(define 'make-adder 
  (lambda (n)
    (lambda (x)
      (add n x))))

(let ((add5 (make-adder 5)))
  (DEBUG-ON)
  (add5 10)
  (DEBUG-OFF))

