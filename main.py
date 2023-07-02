import pygame
import numpy as np

# Simulation parameters
num_particles = 50
container_width = 400
container_height = 300
particle_radius = 3
particle_mass = 1.0
elasticity = 0.1
simulation_speed = 0.1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((container_width, container_height))
clock = pygame.time.Clock()

# Particle class
class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity

        # Particle-wall collisions
        if self.position[0] <= particle_radius or self.position[0] >= container_width - particle_radius:
            self.velocity[0] *= -elasticity
        if self.position[1] <= particle_radius or self.position[1] >= container_height - particle_radius:
            self.velocity[1] *= -elasticity

        # Particle-particle collisions
        for particle in particles:
            if particle != self:
                dist = np.linalg.norm(self.position - particle.position)
                if dist <= 2 * particle_radius:
                    normal = (self.position - particle.position) / dist
                    relative_velocity = self.velocity - particle.velocity
                    impulse = 2 * particle_mass * np.dot(normal, relative_velocity) / (2 * particle_mass)
                    self.velocity -= impulse * normal
                    particle.velocity += impulse * normal

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), self.position.astype(int), particle_radius)

# Create particles
particles = []
for _ in range(num_particles):
    position = np.random.uniform(particle_radius, container_width - particle_radius, size=2)
    velocity = np.random.uniform(-1, 1, size=2)
    particles.append(Particle(position, velocity))

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for particle in particles:
        particle.update()
        particle.draw()

    pygame.display.flip()
    clock.tick(60)
