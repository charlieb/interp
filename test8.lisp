(let ((fn (lambda (x y) (add x y)))
      (a 1)
      (b 2))
    (add (if a a b) (fn 1 2)))

