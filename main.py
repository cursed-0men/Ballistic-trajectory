import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
GRAVITY = 9.81    # Acceleration due to gravity (m/s^2)
AIR_DENSITY = 1.225  # Air density at sea level (kg/m^3)
DRAG_COEFFICIENT = 0.47  # Drag coefficient for a spherical projectile
PROJECTILE_RADIUS = 0.05  # Projectile radius (m)
PROJECTILE_MASS = 1.0    # Mass of the projectile (kg)
WIND_VELOCITY = 2.0  # Wind velocity in m/s (horizontal component)

# Function to calculate drag force (with wind effect)
def calculate_drag_force(velocity, wind_velocity=0.0):
    relative_velocity = velocity - wind_velocity  # Adjust velocity for wind
    area = np.pi * PROJECTILE_RADIUS**2  # Cross-sectional area (m^2)
    drag_force = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * area * relative_velocity**2
    return drag_force

# Function to calculate the trajectory of the projectile from a height or inclined launch
def calculate_trajectory(initial_velocity, launch_angle, height=0.0, incline_angle=0.0):
    # Convert angles to radians
    angle_rad = np.radians(launch_angle)
    incline_rad = np.radians(incline_angle)
    
    # Initial velocities in x and y directions (for incline, use angle adjustment)
    initial_velocity_x = initial_velocity * np.cos(angle_rad) * (1 if incline_angle == 0 else np.cos(incline_rad))
    initial_velocity_y = initial_velocity * np.sin(angle_rad) * (1 if incline_angle == 0 else np.sin(incline_rad))
    
    # Time step for simulation
    dt = 0.01
    
    # Initial conditions
    x, y = 0.0, height  # Launch height for heighted case
    velocity_x, velocity_y = initial_velocity_x, initial_velocity_y  # Initial velocities (m/s)
    
    time = 0.0
    positions = []  # To store position values for visualization
    velocities = []  # To store velocity values for each time step
    
    # Max stats
    max_height = height
    max_range = 0
    max_velocity = 0

    # Simulate projectile motion
    while y >= 0:  # Stop if the projectile hits the ground
        velocity = np.sqrt(velocity_x**2 + velocity_y**2)
        drag_force = calculate_drag_force(velocity, WIND_VELOCITY)
        
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

        # Update max stats
        max_height = max(max_height, y)
        max_range = max(max_range, x)
        max_velocity = max(max_velocity, velocity)

    # Calculate final stats at the end of the trajectory
    final_velocity = velocities[-1]  # Final velocity magnitude
    total_time_of_flight = time  # Total time of flight
    
    # Print final stats
    print(f"\033[32m\nFinal Stats:")
    print(f"Max Height: {max_height:.2f} meters")
    print(f"Range: {max_range:.2f} meters")
    print(f"Final Impact Velocity: {final_velocity:.2f} m/s")
    print(f"Total Time of Flight: {total_time_of_flight:.2f} seconds\033[0m")
    
    return positions, velocities, max_height, max_range, max_velocity

# Function to animate the projectile's trajectory with more realistic visuals
def animate_trajectory(positions, velocities, initial_velocity, launch_angle, max_height, max_range, max_velocity, launch_type):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, max([pos[0] for pos in positions]) * 1.1)  # Set x-axis limits
    ax.set_ylim(0, max([pos[1] for pos in positions]) * 1.1)  # Set y-axis limits
    ax.set_title(f"Projectile Trajectory - Velocity: {initial_velocity} m/s, Angle: {launch_angle}°", fontsize=16, fontweight='bold', color='#333')
    ax.set_xlabel('Distance (m)', fontsize=12, color='#444')
    ax.set_ylabel('Height (m)', fontsize=12, color='#444')
    
    # Background gradient
    ax.set_facecolor('#e0f7fa')
    
    # Add grid with subtle lines
    ax.grid(True, which='both', linestyle='-', linewidth=0.3, color='#aaa')
    
    # Customizable styling for annotations
    annotation_style = {'fontsize': 12, 'fontweight': 'bold', 'color': '#2e3d49'}
    
    # Plotting the initial velocity vector
    velocity_vector, = ax.plot([], [], 'g-', lw=2, label="Velocity Vector")
    trajectory_line, = ax.plot([], [], 'r-', label="Trajectory Path", lw=2)
    projectile_marker, = ax.plot([], [], 'ro', label="Projectile", markersize=8, markeredgecolor='black', markerfacecolor='orange')
    
    # Annotating the max height, max range, and max velocity on the plot
    if launch_type == '2':  # Heighted case
        height_offset = 10
        range_offset = 0
    elif launch_type == '3':  # Inclined case
        height_offset = 15
        range_offset = 10  # Slightly further for inclined trajectories
    else:  # Regular case
        height_offset = 5
        range_offset = 0

    ax.annotate(f"Max Height: {max_height:.2f} m", 
                xy=(max_range * 0.5, max_height + height_offset), 
                xytext=(max_range * 0.5, max_height + height_offset + 5),
                arrowprops=dict(facecolor='red', shrink=0.05), 
                **annotation_style)

    # For inclined trajectory, adjust the range annotation placement
    if launch_type == '3':
        ax.annotate(f"Range: {max_range:.2f} m", 
                    xy=(max_range * 0.9, 0),  # Adjusted for inclined trajectory
                    xytext=(max_range * 0.7, 5),
                    arrowprops=dict(facecolor='blue', shrink=0.05), 
                    **annotation_style)
    else:
        ax.annotate(f"Range: {max_range:.2f} m", 
                    xy=(max_range + range_offset, 0), 
                    xytext=(max_range * 0.5, 10),
                    arrowprops=dict(facecolor='blue', shrink=0.05), 
                    **annotation_style)

    ax.annotate(f"Max Speed: {max_velocity:.2f} m/s", 
                xy=(max_range * 0.5, max_height * 0.9), 
                xytext=(max_range * 0.3, max_height * 0.8), 
                **annotation_style)

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
        
        velocity_vector.set_data([positions[frame][0], positions[frame][0] + current_velocity_x],
                                 [positions[frame][1], positions[frame][1] + current_velocity_y])
        
        return trajectory_line, projectile_marker, velocity_vector
    
    # Animate the trajectory
    ani = FuncAnimation(fig, update, frames=len(positions), interval=30, repeat=False)
    
    # Place the legend outside the plot to avoid interrupting the animation view
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, title="Legend", title_fontsize='13', frameon=False)

    plt.show()

# Example usage with user input as before
launch_type = input("Enter launch type (1 for regular, 2 for heighted, 3 for inclined): ")

if launch_type == '2':  # Heighted
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    launch_angle = float(input("Enter the launch angle (degrees): "))
    height = float(input("Enter initial height (m): "))
    incline_angle = 0
elif launch_type == '3':  # Inclined
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    launch_angle = float(input("Enter the launch angle (degrees): "))
    height = 0
    incline_angle = float(input("Enter incline angle (degrees): "))
else:  # Regular
    initial_velocity = float(input("Enter initial velocity (m/s): "))
    launch_angle = float(input("Enter the launch angle (degrees): "))
    height = 0
    incline_angle = 0

# Calculate trajectory
positions, velocities, max_height, max_range, max_velocity = calculate_trajectory(initial_velocity, launch_angle, height, incline_angle)

# Animate the trajectory
animate_trajectory(positions, velocities, initial_velocity, launch_angle, max_height, max_range, max_velocity, launch_type)
