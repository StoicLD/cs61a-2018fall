## Lab11 解析
本次lab是对于macro机制的一个探讨
之前我在piazza上问了一个问题和本题相关我也写在这里了。
``` scheme
(define-macro (two p) (begin p p))
(define-macro (two-in p) (list 'begin p p))

(two (print 2))
(two-in (print 2))
```
对于第一个例子 `two` 产生的结果只有一个2
而对于第二个例子产生的结果是两个2
<br>
因为macro这个机制，先不对`(print 2)` 进行任何的evaluate。<br>
***

### 一，那么我们来看第一个例子，
- 首先 `(two (print 2))` 会拓展为 `(begin p p))` 其中 `p` 是 `(print 2)` 
- 接着macro会进行一步 **evaluate！** 导致`begin` 被计算，但是注意这个时候p依旧还是一个 `list` 代表 `(print 2)` ，也就是 `(print 2)` 自身没有被求值，但是 `p` 这个符号被求值了，结果是一个 `list` 代表 `(print 2)`
- 随后macro展开结束，返回值为 `(print 2)` 这个list（后一个list）。
- 就如同 `(begin (list 'print 2) 2)` 这个式子中的`(list 'print 2)` 一样，`begin` 计算了它结果是个是个list，并没有计算 `(print 2)` 本身。
- 最后对macro返回的expression求值，即对 `(print 2)` 求值，得到2。

图示如下：<br>
[two macro](./image/two.png)<br>
[env环境图示范](./image/two-re.png)

### 二，第二个例子
- 同样的第一步macro展开，拓展为 `(list 'begin p p)`, `p` 依旧表示 `(print 2)` 这个 `list`。
- 接着进行一步求值！！！此处表现为计算 `list` ，返回结果为 `(begin (print 2) (print 2))` 这个list。
- 注意不同，和例子一相比，例一返回的是 `(print 2)` 而例二返回的是 `(begin (print 2) (print 2))` 。
- 随后对 `(begin (print 2) (print 2))` 求值，得到结果 
    ```
    2
    2
    ```
图示如下：<br>
[two macro](./image/two-in.png)<br>
[env环境图示范](./image/two-in-re.png)

<a href ="http://scheme.pythonanywhere.com/RemovingMuseumPursuit" >附上图示链接</a>