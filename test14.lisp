(define 'cond-fn
  (lambda (body)
    (if (nil? body)
      (lst)
      (let ((first (fst body))
            (rest (rst body)))
        (let ((condition (fst first))
              (expression (fst (rst first))))
          (lst 'if condition expression (cond-fn rest)))))))

(defmacro 'cond 
  (lambda (body)
    (cond-fn body)))

(DEBUG-ON)
(cond ((0 (list 10)) (1 20)))
