## Homework9
### 解析：
#### 这题就是宏展开的拓展，主要是两个方面需要注意
- 第一是for的宏展开写法，参照slide自定义了一个map函数，这个map函数实际上实现了宏展开，然后在定义for的macro
- 对于宏展开，每个原先的括号都要用一个list包起来比如
`(lambda (x) (+ x x))` 应该写成`(list 'lambda (list 'x) (list '+ x x))`
- 还有关于为什么`lamdba` 里面要参数的地方写成 `(list var)` 而不是 `(list 'var)` 因为后面的 `map-expr` 的参数是根据var来的，比如下面的第二个例子里 `(* x x)` 参数是x，而for后面紧接着的迭代参数也是x，所以我们的lambda里面的参数要用已知符号var，而不是写成quote的形式。
- 如果写成quote的形式，就变成了var这个字符本身作为参数，如果是写成 `(list 'x)` 那么可以通过下面这个例子，但是换成别的参数不是x的lambda函数就不能通过了
``` scheme
(list-of (* x x) for x in '(3 4 5) if (odd? x))
; (9 25)

```
<br><br>

Homework9作业完成的代码
``` lisp
; scm> (list-of (* x x) for x in '(3 4 5) if (odd? x))
; (9 25)
; scm> (list-of 'hi for x in '(1 2 3 4 5 6) if (= (modulo x 3) 0))
; (hi hi)
; scm> (list-of (car e) for e in '((10) 11 (12) 13 (14 15)) if (list? e))
; (10 12 14)
(define (map fn expr)
  (if (null? expr)
    ()
    (cons 
      (fn (car expr))
      (map fn (cdr expr)))))

(define-macro (list-of map-expr for var in lst if filter-expr)
  'YOUR-CODE-HERE
  (list 'map (list 'lambda (list var) map-expr) 
          (list 'filter (list 'lambda (list var) filter-expr) lst))
)
```
#### 参考的lecture29 Macro的代码

**Define a macro that evaluates an expression for each value in a sequence**
```lisp
(define (map fn vals)
  (if (null? vals)
      ()
      (cons (fn (car vals))
            (map fn (cdr vals)))))

scm> (map (lambda (x) (* x x)) '(2 3 4 5))
(4 9 16 25)

scm> (for x '(2 3 4 5) (* x x))
(4 9 16 25)

(define-macro (for sym vals expr)
 (list 'lambda (list sym) expr) vals)
```

