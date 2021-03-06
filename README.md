# Turing-Machine-Prime
Designed a Turing Machine to determine if the number is prime. Final Project for Automaton and Formal logic, Fall 2019.

## 设计思路
1. 设计除法总体比较麻烦，因为只能通过左右移动“做减法”，比如$$ ￼A/B=C (A, B, C \in \mathbb{Z} )$$，需要对长度为￼的串做￼次“减法”。图灵机的七元组使了它可以靠“$$ L,R $$”和“修改tape里的字符”来实现减法；
一个一进制的实现：输入string $$1^k$$￼，￼是我们要判定的素数；
2. 复杂度在￼$$ O(n^3) $$量级，因此我们很难判定$$ >100 $$￼的整数；
3. 使用_python_里面的字典做transition function ￼，格式为：$$ \delta(q1,a)=(q2,b,L)￼ $$，即(进入状态, 读) : (转移状态, 写, 右移/左移)，其中￼表示向右移动。
4. 大循环：除数从￼开始，如果没有被整除，则除数++￼，进行下一轮的除法。
5. 每次除法前进入一系列特殊状态检查被除数是否已经和除数相等。如果被除数￼等于除数，那么就意味着对除数来说，$$ (\forall n) 1<n<k, (n,k \in \mathbb{Z}) $$￼ ，没有一个可以整除￼的，所以接受￼是素数。
每个小循环判定是否整除：tape设计左边是被除数，右边是除数，如11122，从右向左，首先带头在右，向左将1改成3并把方向转向右，向右把2改成4并把方向转向左。如果所有2用完（第一轮减法完成），则调用新状态将所有4重新改回2，继续向左将1改成3方向转向右，向右把2改成4方向转向左。直到被除数全部用完，带头在最左B处。
能整除时：从最左B移动（顺便把3改回1，4改回2）到右边的B，没有遇到2，halt。 不能整除时：从左向右检查，遇到2，意味着一轮除数没有用完，没有整除，除数++，进入判定（检查被除数是否已经和除数相等，如不相等进入判定整除……）

## Data Structure, Main Function and Call Function
1. 数据结构：字典
2.  用step变量记录步数，这样调试可以输出有限个（比如step = 100为100次操作）
3.  用move变量记录head在哪里，这样可以精巧地找到带头
4.  如果输入的数比1小，输出error

## 备注
1. 调用“compare”状态需要在除数++之后，开始除法之前。我们从2开始除，因此在initial的时候，就调用了一次compare，以判断2是质数的这个corner case.
2. 先向左，后修改，不然先改完右边的，然后发现左边还有一个，又改了，比如被除数是3，除数是2，那么这样如果先改右边的就会遇到halt。
3. 优化方法之一：可以看到我们专门为了判断是不是除数=被除数用了compare，配合compare的有好几个状态。有一个不错的优化方法是，可以不用compare状态，而是在每一次除法的时候，在除数右边的格子做个标记。这个标记可以用来mark是否把除数位置的4换成2过。如果还没有把所有的4换成2，但是被除数和除数已经用完了，就意味着被除数=除数。
4. 优化方法之二：把一进制换成二进制。将要做除法的数字用二进制表示，然后除法也用二进制处理。因为这个时候需要判断0和1，所以可以引入一个真值表。这部分我没有实现，仅仅有个想法。但是如果真的可以实现，复杂度会比现在的版本低一些。
5. _python 2.7_下，需要把第二行的module变动一下，否则无法调用。
