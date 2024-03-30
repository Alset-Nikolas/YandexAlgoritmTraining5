from collections import deque


class MinMaxDeque:
	def __init__(self):
		self.deque = deque()
		self.max_deque = deque()
		self.min_deque = deque()

	def __add_min(self, x):
		if len(self.min_deque) == 0:
			self.min_deque.append(x)
		else:
			last_el = self.min_deque.pop()
			while len(self.min_deque) > 0 and last_el > x:
				last_el = self.min_deque.pop()
			if last_el <= x:
				self.min_deque.append(last_el)
			self.min_deque.append(x)

	def __add_max(self, x):
		if len(self.max_deque) == 0:
			self.max_deque.append(x)
		else:
			last_el = self.max_deque.pop()
			while len(self.max_deque) > 0 and last_el < x:
				last_el = self.max_deque.pop()
			if last_el >= x:
				self.max_deque.append(last_el)
			self.max_deque.append(x)

	def add(self, x):
		self.__add_min(x)
		self.__add_max(x)
		self.deque.append(x)

	def __pop_min(self, x):
		if len(self.min_deque) <= 0:
			return
		start_el = self.min_deque.popleft()
		if start_el != x:
			self.min_deque.appendleft(start_el)

	def __pop_max(self, x):
		if len(self.max_deque) <= 0:
			return
		start_el = self.max_deque.popleft()
		if start_el != x:
			self.max_deque.appendleft(start_el)

	def popleft(self):
		if len(self.deque) == 0:
			return
		x = self.deque.popleft()
		self.__pop_min(x)
		self.__pop_max(x)
		return x

	def show_left(self):
		return self.deque[0]

	def get_min(self):
		if len(self.min_deque) > 0:
			return self.min_deque[0]

	def get_max(self):
		if len(self.max_deque) > 0:
			return self.max_deque[0]


def init_deque(N, mass, width: int):
	k = 0
	deq_X = MinMaxDeque()
	deq_Y = MinMaxDeque()
	while k < N and mass[k][0] - mass[0][0] < width:
		deq_X.add(mass[k][0])
		k += 1
	while k < N:
		deq_Y.add(mass[k][1])
		k += 1
	return [deq_X, deq_Y]


def is_good_width(N, mass, width_test):
	if width_test == 0:
		return False
	deq_X, deq_Y = init_deque(N, mass, width_test)
	if len(deq_Y.max_deque) > 0 and deq_Y.get_max() - deq_Y.get_min() < width_test:
		return True
	k = len(deq_X.deque)
	l = 0
	while k < N:
		x = mass[k]
		while k < N and x[0] == mass[k][0]:
			deq_X.add(x[0])
			deq_Y.popleft()
			k += 1
		while x[0] - deq_X.show_left() >= width_test:
			deq_Y.add(mass[l][1])
			deq_X.popleft()
			l += 1
		while k < N and mass[k][0] - deq_X.show_left() < width_test:
			deq_X.add(mass[k][0])
			deq_Y.popleft()
			k += 1
		if deq_Y.get_max() - deq_Y.get_min() < width_test:
			return True
	return False


def bin_search(W: int, H: int, N: int, mass: list):
	w_min = 0
	w_max = min(W, H) + 1
	w = range(w_min, w_max)
	l = 0
	r = len(w) - 1
	ans = -1
	while l <= r:
		m = (l + r) // 2
		print(l, m, r)
		if is_good_width(N=N, mass=mass, width_test=w[m]):
			ans = w[m]
			r = m - 1
		else:
			l = m + 1
	if ans != -1:
		return ans
	return min(W, H)


def solution(W: int, H: int, N: int, mass: list) -> (int, int):
	# mass.sort()
	return bin_search(W, H, N, mass)

def read_file_input():
	mass = []
	with open('input.txt', 'r') as f:
		for i, line in enumerate(f.readlines()):
			if i == 0:
				print(line)
				W, H, N = list(map(int, line.split()))
			else:
				mass.append(list(map(int, line.split())))
	return W, H, N, mass


if __name__ == '__main__':

	W, H, N = list(map(int, input().split()))
	mass = []
	for i in range(N):
		mass.append(list(map(int, input().split())))
	res = solution(W, H, N, mass)
	# res = solution(*read_file_input())
	print(res)
