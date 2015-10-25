import numpy as np


class Maze():

    dir1 = np.array([+1,  0,  0, -1], dtype=int)
    dir2 = np.array([ 0, +1, -1,  0], dtype=int)


    def __init__(self, start, target, pMap):

        self.start  = start
        self.target = target

        self.pMap = np.zeros((pMap.shape[0]+1, pMap.shape[1]+1), dtype=bool)
        self.pMap[:~0, :~0] = pMap[:, :]  # Make map with 0-padding.
        self.nMapWidth = pMap.shape[1]

        self.directions = np.zeros((4, 2), dtype=int)


    def solve(self, nOutBufferSize):

        self.currentBest = np.inf
        self.currentBestSnake = []
        self.nOutBufferSize = nOutBufferSize
        self.set_direction(self.start)
        self.forward([self.start])

        if np.isinf(self.currentBest):
            return None
        else:
            return self.currentBestSnake[1:]


    def forward(self, snake):

        # print np.array(snake).tolist()  # Print current snake.
        for prevPos in snake[:~0]:
            if (snake[~0] == prevPos).all():
                # Been here before.
                # print "Been here before: %s" % str(prevPos)
                return
        best_possibility = len(snake) + np.abs(self.target - snake[~0]).sum()
        if best_possibility >= self.currentBest:
            # A better solution cannot be found anymore.
            # print "A better solution cannot be found anymore."
            return
        elif best_possibility > self.nOutBufferSize:
            # Snake is too long.
            # print "Snake is too long."
            return
        elif (snake[~0] == self.target).all():
            # Victory!
            # print "Victory!"
            self.currentBest = len(snake)
            self.currentBestSnake = list(snake)
            return

        for direction in self.directions:
            newPos = snake[~0] + direction
            if self.pMap[newPos[0], newPos[1]]:  # if open path
                self.forward(snake + [newPos])  # continue moving


    def set_direction(self, head):

        direction = self.target - head
        i = np.argmax(np.abs(direction))

        if direction[i] >= 0:
            self.directions[:, i] = +self.dir1
        else:
            self.directions[:, i] = -self.dir1
        if direction[not i] >= 0:
            self.directions[:, not i] = +self.dir2
        else:
            self.directions[:, not i] =  -self.dir2
