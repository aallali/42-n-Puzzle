from collections import deque
import copy
import heapq
import time
from .Node import Node


class Puzzle(object):
	def __init__(self, init_state, goal_state, size, g, u, heuristic):
		self.init_state = []
		self.goal_state = []
		self.actions = deque()
		self.states = deque()
		self.heuristic = heuristic
		self.g = g
		self.u = u
		tmp = []

		for i in range(len(init_state)):
			tmp.append(init_state[i])
			if (i + 1) % size == 0:
				self.init_state.append(tmp)
				tmp = []
		tmp = []
		for i in range(len(goal_state)):
			tmp.append(goal_state[i])
			if (i + 1) % size == 0:
				self.goal_state.append(tmp)
				tmp = []

		for i, v in enumerate(self.init_state):
			for j, k in enumerate(v):
				if k == 0:
					self.start_pos = (i, j)
					break

		self.start_node = Node(self.init_state, None, None, self.start_pos, self.goal_state, self.g, self.u, heuristic)

	def swap(self, curr_state, pos, direction):
		temp = curr_state[pos[0]][pos[1]]
		curr_state[pos[0]][pos[1]] = curr_state[pos[0] + direction[0]][pos[1] + direction[1]]
		curr_state[pos[0] + direction[0]][pos[1] + direction[1]] = temp
		return curr_state

	def move(self, curr_state, pos, visited, direction):
		if pos[0] + direction[0] >= len(curr_state) or pos[0] + direction[0] < 0 or pos[1] + direction[1] >= len(
				curr_state[0]) or pos[1] + direction[1] < 0:
			return None, pos
		if str(self.swap(curr_state, pos, direction)) in visited:
			curr_state = self.swap(curr_state, pos, direction)
			return None, pos

		next_state = copy.deepcopy(curr_state)
		curr_state = self.swap(curr_state, pos, direction)
		return next_state, (pos[0] + direction[0], pos[1] + direction[1])

	def solve_A_STAR(self):
		move_directions = {
			(0, 1): 'LEFT',
			(1, 0): 'UP',
			(-1, 0): 'DOWN',
			(0, -1): 'RIGHT'
		}
		visited = set()
		pq = []
		heapq.heappush(pq, self.start_node)
		count = 0
		timestamp1 = time.time()
		maxOpenSet = 1
		while pq:
			maxOpenSet = max(maxOpenSet, len(pq))
			curr_node = heapq.heappop(pq)
			if curr_node.state == self.goal_state:
				break
			if str(curr_node.state) in visited or str(curr_node.state) in pq:
				continue
			visited.add(str(curr_node.state))

			for direction in move_directions.keys():
				next_state, next_pos = self.move(curr_node.state,
				                                 curr_node.pos,
				                                 visited,
				                                 direction)
				if next_state:
					node = Node(next_state,
					            curr_node,
					            move_directions[direction],
					            next_pos,
					            self.goal_state,
					            self.g,
					            self.u,
					            self.heuristic)
					heapq.heappush(pq, node)
					count += 1

		timestamp2 = time.time()

		while curr_node:
			if curr_node.action:
				self.actions.appendleft(curr_node.action)
				self.states.appendleft(curr_node.state)
			curr_node = curr_node.parent

		return self.actions, self.states, count, len(self.actions), maxOpenSet, timestamp2 - timestamp1