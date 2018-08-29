; Scheme

(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cddr s))
)

(define (sign x)
    (cond
      ((< x 0) -1)
      ((> x 0) 1)
      ((= x 0) 0)
    )
)

(define (ordered? s)
  (if (null? s)
    True
    (if (null? (cdr s))
      True
      (cond
        ((< (car s) (cadr s)) (ordered? (cdr s)))
        ((= (car s) (cadr s)) (ordered? (cdr s)))
        (else False)
      )
    )
  )
)

(define (nodots s)
  (cond
    ((null? s) s)
    ((integer? s) (cons s nil))
    ((null? (cdr s)) s)

    ((and (pair? (car s)) (pair? (cdr s))) (cons (nodots (car s)) (nodots (cdr s))))
    ((and (pair? (car s)) (not (pair? (cdr s)))) (cons (nodots (car s)) (nodots (cdr s))))
    ((pair? s) (cons (car s) (nodots (cdr s))))

  )
)
; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond ((empty? s) false)
          ((> (car s) v) false) ; replace this line
          ((= (car s) v) true)
          (else (contains? (cdr s) v))
    )
)

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return s is Link.empty
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)

(define (add s v)
    (cond ((empty? s) (list v))
          ((contains? s v) s)
          ((> (car s) v) (cons v s)) ; replace this line
          ((< (car s) v) (cons (car s) (add (cdr s) v))
          )
    )
)

(define (intersect s t)
    (cond ((or (empty? s) (empty? t)) nil)
          ((= (car s) (car t)) (cons (car s) (intersect (cdr s) (cdr t))))
          ((< (car s) (car t)) (intersect (cdr s) t))
          ((> (car s) (car t)) (intersect s (cdr t)))
    )
)
; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
    (cond ((empty? s) t)
          ((empty? t) s) 
          ((= (car s) (car t)) (cons (car s) (union (cdr s) (cdr t))))
          ((< (car s) (car t)) (cons (car s) (union (cdr s) t)))
          ((> (car s) (car t)) (cons (car t) (union s (cdr t))))
    )
)

; Tail-Calls in Scheme

(define (exp-recursive b n)
  (if (= n 0)
      1
      (* b (exp-recursive b (- n 1)))))

(define (exp b n)
  ;; Computes b^n.
  ;; b is any number, n must be a non-negative integer.
  (define (exp-optimized n total)
    (if (= n 0)
        total
        (exp-optimized (- n 1) (* total b))))
  (exp-optimized n 1))


(define (filter pred lst)
    (define (helper pred start result)
        (cond ((null? start) result)
              ((pred (car start)) (helper pred (cdr start) (append result (list (car start)))))
              ((not (pred (car start))) (helper pred (cdr start) result))
        ) 
    )
    (helper pred lst '())
)

