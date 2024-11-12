import pygame
import assets
import time
import math

GRID_SIZE = 200 # pixels

POPULATION_SIZE = 1 # number of cells
FOOD_GROWTH_RATE = 1 # number of cells per day

CREATURE_COLOR = (22, 24, 140)
FOOD_COLOR = (67, 163, 42)
DIRECTION_LINE_COLOR = (57, 216, 247)  # Color for the direction line
FIELD_OF_VIEW_DISTANCE = 30  # pixels
FIELD_OF_VIEW = 150  # degrees
FOV_LINE_COLOR = (0, 255, 0)  # Color for the field of view lines
FOV_ARC_COLOR = (0, 255, 0, 100)  # Color for the field of view arc with transparency


pygame.init()


class World:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cells = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.screen = pygame.display.set_mode((grid_size, grid_size))
        pygame.display.set_caption('Game of Life')

    def update(self, population, food_supply):
        # Fill the background color
        self.screen.fill((255, 255, 255))

        # Draw each creature as a circle
        for creature in population.get_creatures():
            x, y = creature.get_position()
            radius = creature.get_radius()
            direction = creature.get_direction()

            pygame.draw.circle(self.screen, CREATURE_COLOR, (x, y), radius)

            # Calculate the endpoint of the direction line
            end_x = x + radius * math.cos(math.radians(direction))
            end_y = y - radius * math.sin(math.radians(direction))  # Subtract to handle pygame's y-axis orientation

            # Draw the direction line
            pygame.draw.line(self.screen, DIRECTION_LINE_COLOR, (x, y), (end_x, end_y), 2)  # 2 is the line thickness

            # Draw the field of view arc
            arc_rect = (x - FIELD_OF_VIEW_DISTANCE, y - FIELD_OF_VIEW_DISTANCE,
                        FIELD_OF_VIEW_DISTANCE * 2, FIELD_OF_VIEW_DISTANCE * 2)
            start_angle = math.radians(direction - FIELD_OF_VIEW / 2)
            end_angle = math.radians(direction + FIELD_OF_VIEW / 2)
            pygame.draw.arc(self.screen, FOV_ARC_COLOR, arc_rect, start_angle, end_angle, 2)

            # Calculate and draw the direction line
            end_x = x + radius * math.cos(math.radians(direction))
            end_y = y - radius * math.sin(math.radians(direction))
            pygame.draw.line(self.screen, DIRECTION_LINE_COLOR, (x, y), (end_x, end_y), 2)

        # Draw each food item as a circle
        for food_item in food_supply.get_food_items():
            x, y = food_item.get_position()
            radius = food_item.get_radius()
            pygame.draw.circle(self.screen, FOOD_COLOR, (x, y), radius)


        pygame.display.flip()


def main():
    world = World(GRID_SIZE)

    population = assets.Population(GRID_SIZE, POPULATION_SIZE)
    food_supply = assets.FoodSupply(GRID_SIZE, FOOD_GROWTH_RATE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        population.pass_a_day(food_supply)
        food_supply.pass_a_day()

        eaten_food_idx = population.eat(food_supply)
        food_supply.remove_food_items(eaten_food_idx)

        world.update(population, food_supply)

        time.sleep(5)
    pygame.quit()

if __name__ == '__main__':
    main()
