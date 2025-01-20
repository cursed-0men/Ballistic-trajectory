import numpy as np
import matplotlib.pyplot as plt

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

# Function to plot the trajectory and velocity
def plot_trajectory_and_velocity(positions, velocities):
    x_vals, y_vals = zip(*positions)
    
    # Plotting trajectory
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(x_vals, y_vals, label="Projectile Trajectory", color="r")
    plt.title("Projectile Trajectory")
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.grid(True)
    plt.legend()

    # Plotting velocity
    time_vals = np.linspace(0, len(velocities)*0.01, len(velocities))  # Time values for the plot
    plt.subplot(1, 2, 2)
    plt.plot(time_vals, velocities, label="Velocity (m/s)", color="b")
    plt.title("Projectile Velocity Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function
if __name__ == "__main__":
    # Input: Initial velocity and launch angle
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    launch_angle = float(input("Enter launch angle (degrees): "))
    
    # Calculate trajectory and velocities
    positions, velocities = calculate_trajectory(initial_velocity, launch_angle)
    
    # Plot the trajectory and velocity over time
    plot_trajectory_and_velocity(positions, velocities)
