;; Extra Scheme Questions ;;

; Q6
(define (remove item lst)
  (filter (lambda (x) (not (= x item))) lst)
)


;;; Tests
(remove 3 nil)
; expect ()
(remove 3 '(1 3 5))
; expect (1 5)
(remove 5 '(5 3 5 5 1 4 5 4))
; expect (3 1 4 4)

; Q7
(define (composed f g)
  (lambda (x) (f (g x)))
)

;;; Tests
(define (add-one a) (+ a 1))
(define (multiply-by-two a) (* a 2))
((composed add-one add-one) 2)

;expect 4

; Q8
(define (max a b) (if (> a b) a b))
(define (min a b) (if (> a b) b a))
(define (gcd a b)
  (cond 
    ((= 0 (min a b)) (max a b))
    (else (gcd (min a b) (modulo (max a b) (min a b))))
  )
)

;;; Tests
(gcd 24 60)
; expect 12
(gcd 1071 462)
; expect 21

; Q9
(define (split-at lst n)
	(cond 
		((null? lst) (cons lst nil))
		((= n 0) (cons nil lst))
		(else (let ((rec (split-at (cdr lst) (- n 1)))
				   )
				   (cons (cons (car lst) (car rec)) (cdr rec))
			  )
		)
	)
)