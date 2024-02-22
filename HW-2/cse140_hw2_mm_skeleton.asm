# Traditional Matrix Multiply program
		.data
matrix_a:
		.word   1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12
		.word  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
		.word  25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36
		.word  37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48
		.word  49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60
		.word  61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72
		.word  73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84
		.word  85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96
		.word  97, 98, 99,100,101,102,103,104,105,106,107,108
		.word 109,110,111,112,113,114,115,116,117,118,119,120
		.word 121,122,123,124,125,126,127,128,129,130,131,132
		.word 133,134,135,136,137,138,139,140,141,142,143,144

matrix_b:
		.word 133,134,135,136,137,138,139,140,141,142,143,144
		.word 121,122,123,124,125,126,127,128,129,130,131,132
		.word 109,110,111,112,113,114,115,116,117,118,119,120
		.word  97, 98, 99,100,101,102,103,104,105,106,107,108
		.word  85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96
		.word  73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84
		.word  61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72
		.word  49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60
		.word  37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48
		.word  25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36
		.word  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
		.word   1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12

matrix_c:
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
		.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0

n:		.word 12

nline:  	.string "\n"			#Define new line string
space:		.string " "
msga: 		.string "Matrix A is: \n"
msgb: 		.string "Matrix B is: \n"
msgc: 		.string "Matrix C=A*B is: \n"
		.text
		.globl main
main:

		la	s1, n
		lw	s1, 0(s1)
		la	s2, matrix_a
		la	s3, matrix_b
		la	s4, matrix_c

		la	a0, msga
		la 	a1, matrix_a
		jal	PRINT_MAT 
		la	a0, msgb
		la 	a1, matrix_b
		jal	PRINT_MAT 

# Your CODE HERE
		add a2, zero, zero # i = 0
		add a3, zero, zero # j = 0
		add a4, zero, zero # k = 0
		
		la t2, matrix_a # Load address of matrix a to t2
		la t3, matrix_b # Load address of matrix b to t3
		la t4, matrix_c # Load address of matrix c to t4
		
For3:		beq a4, s1, For2 # For k
		
		# Formula for finding address of an element
		# (i x row_size x 4) + (j x 4) = new address
		
		mul t5, a2, s1 # i x row_size
		slli t5, t5, 2 # previous x 4
		
		slli t6, a3, 2 # j x 4
		
		add t5, t5, t6 # Address offset
		
		add t5, s4, t5 # Adds the address offset to the address of matrix c
		lw s7,0(t5) # s7 stores the value of C(i,j)
		
		
		mul t5, a2, s1 # i x row_size
		slli t5, t5, 2 # previous x 4
		
		slli t6, a4, 2 # k x 4
		
		add t5, t5, t6 # Address offset
		
		add t5, s2, t5
		lw s5,0(t5) # s5 stores the value of A(i,k)
		
		
		mul t5, a4, s1 # k x row_size
		slli t5, t5, 2 # previous x 4
		
		slli t6, a3, 2 # j x 4
		
		add t5, t5, t6 # Address offset
		
		add t5, s3, t5
		lw s6,0(t5) # s6 stores the value of B(k,j)
		
		mul t5, s5, s6 # a(i,k) x b(k,j)
		add t5, t5, s7 # c(i,j) + previous
		sw t5,0(t4) # Stores the value of c(i,j) + a(i,k) x b(k,j) to matrix c
		
		addi a4, a4, 1 # k++
		b For3
		
For2:		addi a3, a3, 1 # j++
		beq a3, s1, For1 # For j
		add a4, zero, zero # Reset k = 0
		addi t4, t4, 4 # add 4 to the address of matrix c
		b For3
		
For1:		addi a2, a2, 1 # i++
		beq a2, s1, Done # For i
		add a3, zero, zero # Reset j = 0
		add a4, zero, zero # Reset k = 0
		addi t4, t4, 4 # add 4 to the address of matrix c
		b For3
				
Done:


# End CODE

		la	a0, msgc
		la 	a1, matrix_c
		jal	PRINT_MAT 

#   Exit
		li	 a7,10
    		ecall


PRINT_MAT:	li	a7,4
		ecall
		addi 	a2,x0,0	
PL4:		bge	a2,s1,PL1
		addi 	a3,x0,0
PL3:		bge	a3,s1,PL2

		lw	a0,0(a1)
		li	a7,1
		ecall
		la	a0,space
		li	a7,4
		ecall
		addi 	a1,a1,4
		addi 	a3,a3,1
		b 	PL3

PL2:		addi	a2,a2,1
		la	a0,nline
		li	a7,4
		ecall
		b	PL4
PL1:		jr	ra
