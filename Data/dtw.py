# coding: shift-jis
# dtw.py
# Dynamic Time Warping �������v�Z���� (����͎g�p����)

import numpy as np

inf = float('inf')

# ���K������
def normalize(A, K):
	M = A.shape[1]
	m = A.mean(axis=1)
	sd = A.std(axis=1)
	NA = np.zeros((K, M))
	for k in xrange(K):
		if sd[k] != 0:
			NA[k] = (A[k] - m[k])/sd[k]
		else:
			NA[k] = A[k] - m[k]
	return NA

# 3�_�ł̔��������߂�
def calcDeriv3(A, K):
	ret = []
	M = A.shape[1]
	for k in xrange(K):
		tmp = []
		for t in xrange(M):
			if t - 1 < 0:
				a = A[k, 0]
			else:
				a = A[k, t-1]
			if t + 1 > M - 1:
				b = A[k, M-1]
			else:
				b = A[k, t+1]
			der = (a - b) / 2.0
			tmp.append(der)
		ret.append(tmp)
	return np.array(ret)

# 5�_�ł̔��������߂�
def calcDeriv5(A, K):
	ret = []
	M = A.shape[1]
	for k in xrange(K):
		tmp = []
		for t in xrange(M):
			if t - 2 < 0:
				a1 = A[k, 0]
				a2 = A[k, 0]
			else:
				a1 = A[k, t-2]
				a2 = A[k, t-1]
			if t + 2 > M - 1:
				b1 = A[k, M-1]
				b2 = A[k, M-1]
			else:
				b1 = A[k, t+1]
				b2 = A[k, t+2]
			der = (a1 - 8*a2 + 8*b1 - b2) / 12.0
			tmp.append(der)
		ret.append(tmp)
	return np.array(ret)

# ���I�v��@�ł̃R�X�g���v�Z����
def calcCost(A, B, K):
	M = A.shape[1]
	N = B.shape[1]
	NA = A
	NB = B
	cost = np.zeros((M, N))
	for i in xrange(M):
		for j in xrange(N):
			for k in xrange(K):
				cost[i, j] += abs(NA[k, i] - NB[k, j])
	return cost

# DTW �������v�Z����
def calcDTW(A, B, K, window=None):
	M = A.shape[1]
	N = B.shape[1]

	if window is None:
		window = max(M, N)
	w = max(window, abs(M - N))

	cost = calcCost(A, B, K)
	
	DTW = np.zeros((M+1, N+1))
	for i in xrange(1, M+1):
		DTW[i, 0] = inf
	for j in xrange(1, N+1):
		DTW[0, j] = inf
	DTW[0, 0] = 0.0

	for i in xrange(1, M+1):
		start = max(1, i-w)
		end = min(N+1, i+w)
		for j in xrange(start, end):
			c = cost[i-1, j-1]
			DTW[i, j] = c + min(
				DTW[i-1, j],
				DTW[i, j-1],
				DTW[i-1, j-1],
			)
	return DTW

# ������p���� DTW �������v�Z����
def calcDDTW(A, B, K, d = 3, window=None):
	M = A.shape[1]
	N = B.shape[1]

	if window is None:
		window = max(M, N)
	w = max(window, abs(M - N))

	if d == 3:
		dA = calcDeriv3(A, K)
		dB = calcDeriv3(B, K)
	elif d == 5:
		dA = calcDeriv5(A, K)
		dB = calcDeriv5(B, K)

	cost = calcCost(dA, dB, K)
	
	DTW = np.zeros((M+1, N+1))
	for i in xrange(1, M+1):
		DTW[i, 0] = inf
	for j in xrange(1, N+1):
		DTW[0, j] = inf
	DTW[0, 0] = 0.0

	for i in xrange(1, M+1):
		start = max(1, i-w)
		end = min(N+1, i+w)
		for j in xrange(start, end):
			c = cost[i-1, j-1]
			DTW[i, j] = c + min(
				DTW[i-1, j],
				DTW[i, j-1],
				DTW[i-1, j-1],
			)
	return DTW

# ���Ƃ̐M���Ɣ�����p���� DTW �������v�Z����
def calcSDDTW(A, B, K, d = 3, window=None):
	M = A.shape[1]
	N = B.shape[1]

	if window is None:
		window = max(M, N)
	w = max(window, abs(M - N))

	if d == 3:
		dA = calcDeriv3(A, K)
		dB = calcDeriv3(B, K)
	elif d == 5:
		dA = calcDeriv5(A, K)
		dB = calcDeriv5(B, K)

	new_A = []
	new_B = []
	
	for k in xrange(K):
		new_A.append(A[k])
		new_A.append(dA[k])
		new_B.append(B[k])
		new_B.append(dB[k])
	new_A = np.array(new_A)
	new_B = np.array(new_B)
	cost = calcCost(new_A, new_B, 2*K)
	
	DTW = np.zeros((M+1, N+1))
	for i in xrange(1, M+1):
		DTW[i, 0] = inf
	for j in xrange(1, N+1):
		DTW[0, j] = inf
	DTW[0, 0] = 0.0

	for i in xrange(1, M+1):
		start = max(1, i-w)
		end = min(N+1, i+w)
		for j in xrange(start, end):
			c = cost[i-1, j-1]
			DTW[i, j] = c + min(
				DTW[i-1, j],
				DTW[i, j-1],
				DTW[i-1, j-1],
			)
	return DTW
