##自动机与形式逻辑 大作业：判断素数图灵机
###清华大学 物理系 物理61班 张锦苏 2014012919

###设计思路
1. 设计除法总体比较麻烦，因为只能通过左右移动“做减法”，比如$$ ￼A/B=C (A, B, C \in \mathbb{Z} )$$，需要对长度为￼的串做￼次“减法”。图灵机的七元组使了它可以靠“$$ L,R $$”和“修改tape里的字符”来实现减法；
一个一进制的实现：输入string $$1^k$$￼，￼是我们要判定的素数；
2. 复杂度在￼$$ O(n^3) $$量级，因此我们很难判定$$ >100 $$￼的整数；
3. 使用_python_里面的字典做transition function ￼，格式为：$$ \delta(q1,a)=(q2,b,L)￼ $$，即(进入状态, 读) : (转移状态, 写, 右移/左移)，其中￼表示向右移动。
4. 大循环：除数从￼开始，如果没有被整除，则除数++￼，进行下一轮的除法。
5. 每次除法前进入一系列特殊状态检查被除数是否已经和除数相等。如果被除数￼等于除数，那么就意味着对除数来说，$$ (\forall n) 1<n<k, (n,k \in \mathbb{Z}) $$￼ ，没有一个可以整除￼的，所以接受￼是素数。
每个小循环判定是否整除：tape设计左边是被除数，右边是除数，如11122，从右向左，首先带头在右，向左将1改成3并把方向转向右，向右把2改成4并把方向转向左。如果所有2用完（第一轮减法完成），则调用新状态将所有4重新改回2，继续向左将1改成3方向转向右，向右把2改成4方向转向左。直到被除数全部用完，带头在最左B处。
能整除时：从最左B移动（顺便把3改回1，4改回2）到右边的B，没有遇到2，halt。 不能整除时：从左向右检查，遇到2，意味着一轮除数没有用完，没有整除，除数++，进入判定（检查被除数是否已经和除数相等，如不相等进入判定整除……）

###Data Structure, Main Function and Call Function
1. 数据结构：字典
2.  用step变量记录捕鼠，这样调试可以输出有限个（比如step = 100为100次操作）
3.  用move变量记录head在哪里，这样可以精巧地找到带头
4.  如果输入的数比1小，输出error

###备注
1. 调用“compare”状态需要在除数++之后，开始除法之前。我们从2开始除，因此在initial的时候，就调用了一次compare，以判断2是质数的这个corner case.
2. 先向左，后修改，不然先改完右边的，然后发现左边还有一个，又改了，比如被除数是3，除数是2，那么这样如果先改右边的就会遇到halt。
3. 优化方法之一：可以看到我们专门为了判断是不是除数=被除数用了compare，配合compare的有好几个状态。有一个不错的优化方法是，可以不用compare状态，而是在每一次除法的时候，在除数右边的格子做个标记。这个标记可以用来mark是否把除数位置的4换成2过。如果还没有把所有的4换成2，但是被除数和除数已经用完了，就意味着被除数=除数。
4. 优化方法之二：把一进制换成二进制。将要做除法的数字用二进制表示，然后除法也用二进制处理。因为这个时候需要判断0和1，所以可以引入一个真值表。这部分我没有实现，仅仅有个想法。但是如果真的可以实现，复杂度会比现在的版本低一些。
5. _python 2.7_下，需要把第二行的module变动一下，否则无法调用。


		from Tkinter import *


### Code

		import math
		from tkinter import *
	
		window = Tk()
	
		window.title('图灵机判断素数')
	
		window.geometry('800x600')
	
		v1 = StringVar()
		v2 = StringVar()
		e1 = Entry(window, width=10, textvariable=v1)
		e1.pack(padx=10, pady=10)
		e2 = Entry(window, width=10, textvariable=v2, state='readonly')
		e2.pack()
	
		box = Listbox(window, height=20, width=50)
		box.pack()
	
		transition2 = {
	    	('start', '1') : ('start', '1', 1),
	    	('start', 'B') : ('creatediv', '2', 1),
	    	('creatediv', 'B') : ('stopcreate', '2', 1),
	    	('stopcreate', 'B' ) : ('compare', 'B', -1),
	    	('moveleft', '2') : ('moveleft', '2', -1),
	    	('moveleft', '4') : ('moveleft', '4', -1),
	    	('moveleft', '3') : ('moveleft', '3', -1),
	    	('moveleft', '1') : ('moveright', '3', 1), #change direction, mark
	    	('moveright', '3') : ('moveright', '3', 1),
	    	('moveright', '4') : ('moveright', '4', 1),
	    	('moveright', '2') : ('moveleft', '4', -1), #change direction, mark
	    	('moveright', 'B') : ('touchbound', 'B', -1),
	    	('touchbound', '4') : ('rewash', '2', -1),
	    	('rewash', '4') : ('rewash', '2', -1),
	    	('rewash', '3') : ('addback', '3', 1),
	    	('addback', '2') : ('moveleft', '4', -1),
	    	('moveleft', 'B') : ('check', 'B', 1),# check if halt
	    	('check', '3') : ('check', '1', 1),
	    	('check', '4') : ('check', '2', 1),
	    	('check', '2') : ('restart', '2', -1),
	    	('check', 'B') : ('halt', 'B', 0),
	    	('restart', '2') : ('restart', '2', 1),
	    	('restart', 'B') : ('div++', '2', 1),
	    	('div++', 'B') : ('compare', 'B', -1),
	    	('compare', '2') : ('compare', '2', -1),
	    	('compare', '3') : ('compare', '3', -1),
	    	('backhead2', '1') : ('backhead2', '1', -1),
	    	('backhead2', 'B') : ('restart2', 'B', 1),
	    	('restart2', '1') : ('restart2', '1', 1),
	    	('restart2', '2') : ('restart2', '2', 1),
	    	('restart2', 'B') : ('moveleft', 'B', -1),
	    	('compare', 'B') : ('accept', 'B', 0),
	    	('compare', '4') : ('compare', '4', -1),
	    	('compare', '1') : ('compare2', '3', 1),
	    	('compare2', '3') : ('compare2', '3', 1),
	    	('compare2', '4') : ('compare2', '4', 1),
	    	('compare2', '2') : ('compare', '4', -1),
	    	('compare2', 'B') : ('backhead2', 'B', -1),
	    	('backhead2', '4') : ('backhead2', '2', -1),
	    	('backhead2', '3') : ('backhead2', '1', -1),
		}
	
		def simulation(transition2, input):
	    	head = 0
	    	tape = input
	    	state = 'start'
	    	steps = 0
	    	while state !='accept' and state != 'halt':
	        	state, tape[head], move = transition2[(state, tape[head])]
	        	head += move
	        if head < 0:
	            tape.insert(0, 'B')
	            head += 1
	        if head >= len(tape):
	            tape.append('B')
	        steps += 1
	        box.insert(steps - 1, ''.join(tape[:head]) + '*' + ''.join(tape[head:]))
	    	v2.set(str(state))
	
		def error():
    		v2.set('error')
    

		def call():
    		x = int(v1.get())
    		if x > 1:
        	y = x
        	simulation(transition2, ['1'] *  y)
    	else:
        	error()
	   
		button = Button(window, text="计算是否素数", command=call)
		button.pack()
	
		window.mainloop()
