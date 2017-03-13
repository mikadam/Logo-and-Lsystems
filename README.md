#LOGO Motion

######Interpreted turtle language with L-system module

![Screenshot](https://github.com/mikadam/Logo-and-Lsystems/blob/master/screen_shot.png)


I wrote this around 2014 to discover how someone might go about writing an interpreted language and seeing how far can I push it without implementing more features. For example although functions don't support returning values  explicitly (and values can't be returned using globals due to scoping) it can be acomplished using the special variables (which I discovered after writing it). Similarly if statments can be implemented using zero length loops
 
I've also added an [L-systems](https://en.wikipedia.org/wiki/L-system) parser to explore fractals.

##Basic Turtle Commands:

	fd n: move forwards n pixels
	tr n: turn n degrees left
	pu: pen up
	pd: pen down
	st: push current location onto stack
	rc: pop location from stack
	cl: clear 
	pr n: print n to console

##Other Language features:

	x = 15; set variable x equal to 15
	x 10{ ... }; loop code in brackets with x varying from 0 to 10
	func x y ={pr x; pr y};defines a function func which 
	prints its two arguments in sequence
	
####Special variables 
`#x` - current x position
`#y` - current y position
`#a` - current angle
`#p` - current pen state


##Function Examples:

	ngon n s={x n{fd s;tr 360/n}}; Draws a polygon with n sides of length s
	
	circle radius={temp=#p;pu;fd radius;tr 90;pd;x 360{fd 2*3.1416*radius/360;tr 1};tr 90;pu;fd radius;pd;tr 180,#p=temp}
	; draws circle of radius circle
	
	square n={#x=n*n} ; defining square function with hacky return value
	pu; temp=#x; square 5; output=#x; #x=temp; pd; calling square function

##L-system Examples:
<pre>
	<b>Koch Snowflake</b> (a=60):
	Initial: f++f++f
	f:f-f++f-f
	
	<b>Tree</b> (a=15-40):
	Initial: p
	f:ff
	p:f[+p]f[+p][-p]
	
	<b>Sierpinski Triangle</b> (a=60):
	Initial: p
	p:[p]f[p]f++f[p]f++ff
	f:ff
	
	<b>Dragon Curve</b> (a=90):
	Initial: k
	k:fl-fk
	l:fl+fk
	f:s
	
	<b>Hilbert</b> (a=90):
	Initial: p
	p:-lf+pfp+fl-
	l:+pf-lfl-fp+
	
	<b>Penrose Tiling</b> (a=36):
	Initial :[N]++[N]++[N]++[N]++[N]
	M:fOA++PA----NA[-OA----MA]++
	N:f+OA--PA[---MA--NA]+
	O:f-MA++NA[+++OA++PA]-
	P:f--OA++++MA[+PA++++NA]--NA
	A:f
	f:j
</pre>


Michal Adamkiewicz 2017