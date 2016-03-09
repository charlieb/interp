(let ((tst (lst 1 2 3 4))
      (total (lambda (list) 
               (if (nil? list)
                 0
                 (add (fst list) 
                      (total (rst list)))))))
  (total tst))


