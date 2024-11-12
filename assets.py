import numpy as np
import helpers


# Creatures medatata
INITIAL_ENERGY_LEVEL = 100
ENERGY_GETTING_FROM_EATING_FOOD = 0.3 # 30% of the food energy is transferred to the creature
ENERGY_REQUIRED_TO_REPRODUCE = 0.5 # 50% of the energy is transferred to the offspring
MATURITY_AGE = 3 
FIELD_OF_VIEW = 150 # degrees
FIELD_OF_VIEW_DISTANCE = 50 # pixels


class Creature:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.radius = 5
        self.x = np.random.randint(5, grid_size-5)
        self.y = np.random.randint(5, grid_size-5)

        self.direction = np.random.randint(0, 360)
        self.age = 0
        self.energy = INITIAL_ENERGY_LEVEL
        self.INITIAL_ENERGY = INITIAL_ENERGY_LEVEL


    def get_position(self):
        return self.x, self.y
    
    def get_radius(self):
        return self.radius
    
    def get_direction(self):
        return self.direction
    
    def detect_food_in_view(self, food_supply):
        # Initialize sectors for the 150-degree field of view (75 degrees on each side of the direction)
        sectors = [FIELD_OF_VIEW_DISTANCE] * 150  # Default to inf if no food is within range

        # Define the starting and ending angles of the field of view
        # Calculate the start and end angles for the field of view
        half_fov = FIELD_OF_VIEW / 2
        start_angle = (self.direction - half_fov + 360) % 360
        end_angle = (self.direction + half_fov) % 360
        total_food_in_view = 0
        # Loop through each food item to check if it's within the field of view and distance
        for food_item in food_supply.get_food_items():
            food_x, food_y = food_item.get_position()
            distance = helpers.calculate_distance(self.x - food_x, self.y - food_y)
            
            if distance <= FIELD_OF_VIEW_DISTANCE:
                # Calculate the angle to the food relative to the creature's direction
                angle_to_food = np.degrees(np.arctan2(food_y - self.y, food_x - self.x))
                angle_to_food = (angle_to_food + 360) % 360  # Normalize angle to [0, 360) range

                # Check if the angle to food is within the creature's field of view
                if start_angle <= angle_to_food <= end_angle or (
                    start_angle > end_angle and (angle_to_food >= start_angle or angle_to_food <= end_angle)
                ):
                    # Calculate the sector index within the field of view range (0 to 149)
                    sector_index = int((angle_to_food - start_angle + 360) % 360) % 150
                    total_food_in_view += 1
                    # Update the sector with the minimum distance if food is found closer
                    sectors[sector_index] = min(sectors[sector_index], distance)
        print("Total food in view: ", total_food_in_view)
        print(sectors)
        return sectors

    def move(self, food_supply):

        self.age += 1

        
        

        x_delta = np.random.randint(-1, 2)
        y_delta = np.random.randint(-1, 2)
        self.x += x_delta
        self.y += y_delta

        new_direction = np.random.randint(0, 360)
        self.direction = new_direction

        distance_moved = helpers.calculate_distance(x_delta, y_delta)
        self.energy -= distance_moved
        sectors = self.detect_food_in_view(food_supply)
        self.x = int(np.clip(self.x, self.radius, self.grid_size - self.radius))
        self.y = int(np.clip(self.y, self.radius, self.grid_size - self.radius))


    def check_if_starved(self):
        # print(self.energy)
        if self.energy <= 0:
            return True
        return False


    


class Population:
    def __init__(self, grid_size, population_size):
        self.population_size = population_size
        self.creatures = [Creature(grid_size) for _ in range(population_size)]


    def get_creatures(self):
        return self.creatures
    

    def pass_a_day(self, food_supply):
        dead_creatures = []
        for i, creature in enumerate(self.creatures):
            creature.move(food_supply)
            if creature.check_if_starved():
                dead_creatures.append(i)
        
        for i in reversed(dead_creatures):
            self.creatures.pop(i)
            

    def eat(self, food_supply):
        eaten_food_idx = []
        for creature in self.creatures:
            for i, food_item in enumerate(food_supply.get_food_items()):
                if i in eaten_food_idx:
                    continue
                x, y = creature.get_position()
                food_x, food_y = food_item.get_position()
                distance = helpers.calculate_distance(x-food_x, y-food_y)
                if distance <= creature.get_radius() + food_item.get_radius():
                    creature.energy += creature.INITIAL_ENERGY * ENERGY_GETTING_FROM_EATING_FOOD
                    eaten_food_idx.append(i)
                    break
        return eaten_food_idx            

class FoodItem:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.radius = 3
        self.x = np.random.randint(self.radius, grid_size-self.radius)
        self.y = np.random.randint(self.radius, grid_size-self.radius)

    def get_position(self):
        return self.x, self.y
    
    def get_radius(self):
        return self.radius


class FoodSupply:
    def __init__(self, grid_size, food_growth_rate):
        self.grid_size = grid_size
        self.food_growth_rate = food_growth_rate

        self.food_items = [FoodItem(grid_size) for _ in range(food_growth_rate)]


    def get_food_items(self):
        return self.food_items

    def pass_a_day(self):
        self.food_items.extend([FoodItem(self.grid_size) for _ in range(self.food_growth_rate)])
        
    def remove_food_items(self, eaten_food_idx):
        for i in reversed(eaten_food_idx):
            self.food_items.pop(i)
    
    