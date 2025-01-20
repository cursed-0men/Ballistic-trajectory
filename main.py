import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
GRAVITY = 9.81    # Acceleration due to gravity (m/s^2)
AIR_DENSITY = 1.225  # Air density at sea level (kg/m^3)
DRAG_COEFFICIENT = 0.47  # Drag coefficient for a spherical projectile
PROJECTILE_RADIUS = 0.05  # Projectile radius (m)
PROJECTILE_MASS = 1.0    # Mass of the projectile (kg)

# Function to calculate drag force
def calculate_drag_force(velocity):
    area = np.pi * PROJECTILE_RADIUS**2  # Cross-sectional area (m^2)
    drag_force = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * area * velocity**2
    return drag_force

# Function to calculate the trajectory of the projectile
def calculate_trajectory(initial_velocity, launch_angle):
    # Convert angle to radians
    angle_rad = np.radians(launch_angle)
    
    # Initial velocities in x and y directions
    initial_velocity_x = initial_velocity * np.cos(angle_rad)
    initial_velocity_y = initial_velocity * np.sin(angle_rad)
    
    # Time step for simulation
    dt = 0.01
    
    # Initial conditions
    x, y = 0.0, 0.0  # Initial horizontal and vertical positions (m)
    velocity_x, velocity_y = initial_velocity_x, initial_velocity_y  # Initial velocities (m/s)
    
    time = 0.0
    positions = []  # To store position values for visualization
    velocities = []  # To store velocity values for each time step
    
    # Simulate projectile motion
    while y >= 0:  # Stop if the projectile hits the ground
        velocity = np.sqrt(velocity_x**2 + velocity_y**2)
        drag_force = calculate_drag_force(velocity)
        
        # Calculate drag accelerations
        drag_acceleration_x = drag_force * (velocity_x / velocity) / PROJECTILE_MASS
        drag_acceleration_y = drag_force * (velocity_y / velocity) / PROJECTILE_MASS
        
        # Update velocities due to gravity and drag
        velocity_x -= drag_acceleration_x * dt
        velocity_y -= (GRAVITY + drag_acceleration_y) * dt
        
        # Update positions
        x += velocity_x * dt
        y += velocity_y * dt
        
        # Store the position and velocity at each time step
        positions.append((x, y))
        velocities.append(np.sqrt(velocity_x**2 + velocity_y**2))
        time += dt
    
    return positions, velocities

# Function to animate the projectile's trajectory with more realistic visuals
# Function to animate the projectile's trajectory with more realistic visuals
def animate_trajectory(positions, velocities, initial_velocity, launch_angle):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, max([pos[0] for pos in positions]) * 1.1)  # Set x-axis limits
    ax.set_ylim(0, max([pos[1] for pos in positions]) * 1.1)  # Set y-axis limits
    ax.set_title(f"Projectile Trajectory - Velocity: {initial_velocity} m/s, Angle: {launch_angle}°", fontsize=14)
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Height (m)')
    
    # Add grid and background
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_facecolor('lightblue')
    
    # Plotting the initial velocity vector
    velocity_vector, = ax.plot([], [], 'g-', lw=2, label="Velocity Vector")
    trajectory_line, = ax.plot([], [], 'r-', label="Trajectory Path")
    projectile_marker, = ax.plot([], [], 'bo', label="Projectile")
    
    # Function to update the animation
    def update(frame):
        # Update the projectile's position and the velocity vector
        trajectory_line.set_data([pos[0] for pos in positions[:frame]], [pos[1] for pos in positions[:frame]])
        
        # Use lists even for a single point
        projectile_marker.set_data([positions[frame][0]], [positions[frame][1]])
        
        # Dynamically update velocity vector based on the current velocity direction
        velocity_x, velocity_y = positions[frame][0] - positions[frame-1][0], positions[frame][1] - positions[frame-1][1]
        velocity_angle = np.arctan2(velocity_y, velocity_x)
        velocity_magnitude = velocities[frame]
        
        # Update velocity vector with dynamic angle
        current_velocity_x = velocity_magnitude * np.cos(velocity_angle)
        current_velocity_y = velocity_magnitude * np.sin(velocity_angle)
        
        velocity_vector.set_data([positions[frame][0], positions[frame][0] + current_velocity_x * 0.2], 
                                 [positions[frame][1], positions[frame][1] + current_velocity_y * 0.2])
        
        return trajectory_line, velocity_vector, projectile_marker

    # Creating the animation (set blit=False for simpler updates)
    ani = FuncAnimation(fig, update, frames=len(positions), interval=50, blit=False)
    
    # Show the animation
    plt.legend()
    plt.show()


    # Creating the animation
    ani = FuncAnimation(fig, update, frames=len(positions), interval=50, blit=True)
    
    # Show the animation
    plt.legend()
    plt.show()

# Main function
if __name__ == "__main__":
    # Input: Initial velocity and launch angle
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    launch_angle = float(input("Enter launch angle (degrees): "))
    
    # Calculate trajectory and velocities
    positions, velocities = calculate_trajectory(initial_velocity, launch_angle)
    
    # Animate the projectile's trajectory and velocity
    animate_trajectory(positions, velocities, initial_velocity, launch_angle)
