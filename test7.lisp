(let ((fn (lambda (add a b)))
      (a 1)
      (b 2))
    (add (if a a b) (fn)))

