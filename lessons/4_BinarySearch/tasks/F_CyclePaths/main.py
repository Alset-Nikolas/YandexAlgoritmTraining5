import math


def is_good_width(N, mass, width_test, pre_table):
	if width_test == 0:
		return False
	max_left, min_left, max_right, min_right, info = pre_table
	r = 0
	l = 0
	while l < N:

		while r + 1 < N and mass[r + 1][0] - mass[l][0] < width_test:
			r += 1
			k = 2
			while r + k < N and mass[r + k][0] - mass[l][0] < width_test:
				r += k
				k *= 2

		min_pref_mass, max_pref_mass = min_left[l], max_left[l]
		min_suf_mass, max_suf_mass = min_right[r], max_right[r]
		min_Y, max_Y = min(min_pref_mass, min_suf_mass), max(max_pref_mass, max_suf_mass)

		if 0 <= max_Y - min_Y < width_test:
			return True
		l += info[ mass[l][0]]
		r = max(r, l)
		if r >= N - 1:
			return False
	return False


def bin_search(W: int, H: int, N: int, mass: list, pre_table: list):
	l = 1
	r =  min(W, H)
	ans = -1
	while l <= r:
		m = (l + r) // 2
		if is_good_width(N=N, mass=mass, width_test=m, pre_table=pre_table):
			ans = m
			r = m - 1
		else:
			l = m + 1
	if ans != -1:
		return ans
	return min(W, H)


def pre_calc(N, mass):
	if not mass:
		return [], [], [], []
	max_left = [-math.inf] + [mass[0][1]] * N
	min_left = [math.inf] + [mass[0][1]] * N
	max_right = [mass[-1][1]] * N + [-math.inf]
	min_right = [mass[-1][1]] * N + [math.inf]
	info = dict()
	j = N
	info[mass[0][0]] = 1
	for i in range(2, N+1):
		max_left[i] = max(max_left[i - 1], mass[i-1][1])
		min_left[i] = min(min_left[i - 1], mass[i-1][1])
		max_right[j - (i-1)] = max(max_right[j - i], mass[j - i][1])
		min_right[j - (i-1)] = min(min_right[j - i], mass[j - i][1])

		if mass[i-1][0] not in info:
			info[mass[i-1][0]] = 0
		info[mass[i-1][0]] += 1

	return [max_left, min_left, max_right, min_right, info]


def solution(W: int, H: int, N: int, mass: list) -> (int, int):
	mass.sort()
	pre_table = pre_calc(N, mass)
	print(mass)
	print(pre_table)
	return bin_search(W, H, N, mass, pre_table)


# def read_file_input():
# 	mass = []
# 	with open('input.txt', 'r') as f:
# 		for i, line in enumerate(f.readlines()):
# 			if i == 0:
# 				W, H, N = list(map(int, line.split()))
# 			else:
# 				mass.append(list(map(int, line.split())))
# 	return W, H, N, mass


if __name__ == '__main__':
	W, H, N = list(map(int, input().split()))
	mass = []
	for i in range(N):
		mass.append(list(map(int, input().split())))
	res = solution(W, H, N, mass)
	print(res)
	# start = datetime.datetime.now()
	# print(datetime.datetime.now())
	# res = solution(*read_file_input())
