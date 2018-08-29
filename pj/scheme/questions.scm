(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdar x)))
; Some utility functions that you may find useful to implement.
(define (map proc items)
  (if (null? items) 
      nil
      (cons (proc (car items)) (map proc (cdr items)))
  )
)

(define (cons-all first rests)
  (if (null? rests)
      nil
      (cons (cons first (car rests)) (cons-all first (cdr rests)))
  )
)


(define (zip pairs)
  (if (null? pairs) '(() ())
  (cons (z_A pairs) (cons (z_B pairs) nil))))

(define (z_A pairs)
  (if (null? pairs)
      nil
      (cons (caar pairs) (z_A (cdr Pairs)))
  )
)

(define (z_B pairs)
  (if (null? pairs)
      nil
      (cons (cadar pairs) (z_B (cdr Pairs)))
  )
)


;(define (zip pairs)
;  (if (null? pairs)
;      (cons nil (cons nil nil))
;      (cons
;        (cons (caar pairs) (car (zip (cdr pairs))))
;        (cons (cons (car (cdar pairs)) (cadr (zip (cdr pairs))) nil))
;      ) 
;  )
;)


;(cons (cons first (cons (car s) nil) (enu-help (+ 1 first) (cdr s)))

;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (define (enu-help first s)
    (if (null? s)
      nil
      (cons (cons first (cons (car s) nil)) (enu-help (+ 1 first) (cdr s)))
    )
  )
  (enu-help 0 s)
)
  ; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
    (cond
      ((= total 0) '(()))
      ((or (< total 0) (null? denoms)) '())
      (else (append
              (map (lambda (l) (cons (car denoms) l)) (list-change (- total (car denoms)) denoms))
              (list-change total (cdr denoms))
            )
      )
    )
)
  ; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (append
              (list form params)
              (map let-to-lambda body))

           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (cons (append 
                    (append (list 'lambda) (list (car (zip values)))) 
                        (map let-to-lambda body))   
                    (map let-to-lambda (cadr (zip values)))
          )
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
         (map let-to-lambda expr)
         ; END PROBLEM 19
         )))
