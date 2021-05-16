import pygame
import random

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Snake:
    should_grow = False
    can_move = True
    def __init__(self, position,world_size,color=GREEN,size=16):
        self.body = [position]
        direction = random.choice([[0,size],[size,0],[0,-size],[-size,0]])
        self.vy = direction[0]
        self.vx = direction[1]
        self.color = color
        self.size = size
        self.world_size = world_size

    def new_pos(self):
        y = self.body[0][0]+self.vy
        x = self.body[0][1]+self.vx
        if y < 0:
            y = self.world_size-self.size
        elif y>= self.world_size:
            y = 0

        if x < 0:
            x = self.world_size-self.size
        elif x>= self.world_size:
            x = 0

        return (y,x)

    def update(self):
        if self.should_grow:
            self.body = [self.new_pos()]+self.body
            self.should_grow = False
        else:
            self.body = [self.new_pos()]+self.body[:-1]

    def changeMovement(self,option):
        if self.can_move:
            if option == 0 and self.vx != self.size:
                self.vx = -self.size
                self.vy = 0
                can_move = False
            elif option == 1 and self.vy != self.size:
                self.vx = 0
                self.vy = -self.size
                can_move = False
            elif option == 2 and self.vx != -self.size:
                self.vx = self.size
                self.vy = 0
                can_move = False
            elif option ==3 and self.vy != -self.size:
                self.vx = 0
                self.vy = self.size
                can_move = False

    def allow_move(self):
        self.can_move = True


    def check_collision_self(self):
        if self.body[0] in self.body[1:]:
            return True
        return False

    def check_collision_food(self, food_pos):
        if self.body[0] == food_pos:
            self.grow()
            return True
        return False

    def check_collision_snake(self, snake):
        if self.body[0] in snake.body[1:]:
            return True
        if self.body[0] == snake.body[0] and not (self.vx == -snake.vx or self.vy == -snake.vy):
            return True
        return False

    def grow(self):
        self.should_grow = True

    def draw(self,surface):
        for element in self.body:
            pygame.draw.rect(surface,self.color, pygame.Rect(element[1],element[0],self.size,self.size))

class Food():
    def __init__(self, world_size,snake_body,size=16):
        self.N = world_size//size
        self.size=size
        self.init_position(snake_body)
        self.color = RED

    def init_position(self, snake_body):
        positions = []
        for i in range(self.N):
            for j in range(self.N):
                pos = (i,j)
                if pos not in snake_body:
                    positions += [pos]
        position = random.choice(positions)
        self.position = (position[0]*self.size,position[1]*self.size)

    def update(self):
        return

    def draw(self, surface):
        pygame.draw.rect(surface,self.color, pygame.Rect(self.position[1],self.position[0],self.size,self.size))


if __name__ == "__main__":

    successes, failures = pygame.init()

    size = 32
    world_size = size*22

    screen = pygame.display.set_mode((world_size, world_size))  # Notice the tuple! It's not 2 arguments.
    clock = pygame.time.Clock()
    FPS = 15  # This variable will define how many frames we update per second.

    snake1 = Snake((world_size-size*2, size),world_size,size=size)
    snake2 = Snake((size, world_size-size*2),world_size,color=BLUE,size=size)
    food = Food(world_size,snake1.body+snake2.body,size=size)

    elements = [snake1, snake2,food]

    while True:
        clock.tick(FPS)

        snake1.allow_move()
        snake2.allow_move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    snake1.changeMovement(0)
                elif event.key == pygame.K_w:
                    snake1.changeMovement(1)
                elif event.key == pygame.K_d:
                    snake1.changeMovement(2)
                elif event.key == pygame.K_s:
                    snake1.changeMovement(3)

                elif event.key == pygame.K_LEFT:
                    snake2.changeMovement(0)
                elif event.key == pygame.K_UP:
                    snake2.changeMovement(1)
                elif event.key == pygame.K_RIGHT:
                    snake2.changeMovement(2)
                elif event.key == pygame.K_DOWN:
                    snake2.changeMovement(3)

        screen.fill(BLACK)

        # update
        for el in elements:
            el.update()

        # check collision
        if snake1.check_collision_self():
            break
        if snake1.check_collision_food(food.position):
            food.init_position(snake1.body+snake2.body)
        if snake1.check_collision_snake(snake2):
            print("blue snake wins")
            break

        if snake2.check_collision_self():
            break
        if snake2.check_collision_food(food.position):
            food.init_position(snake1.body+snake2.body)
        if snake2.check_collision_snake(snake1):
            print("green snake wins")
            break

        # draw
        for el in elements:
            el.draw(screen)

        pygame.display.update()  # Or 'pygame.display.flip()'.
