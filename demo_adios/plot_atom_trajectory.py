#!/usr/bin/env python3
"""
Plot the trajectory of a single atom over time in the LAMMPS melting simulation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from adios2 import FileReader
import argparse
import sys

def plot_atom_trajectory(atom_id, output_file=None):
    """
    Plot the trajectory of a single atom over time.
    
    Parameters:
    atom_id (int): The ID of the atom to track
    output_file (str): Optional output filename for the plot
    """
    
    # Open the BP5 file
    with FileReader("/home/jcernuda/demo_adios/Lammps-melting-gold.bp5") as reader:
        
        # Get available variables
        vars_info = reader.available_variables()
        steps = int(vars_info['ntimestep']['AvailableStepsCount'])
        
        print(f"Tracking atom {atom_id} over {steps} timesteps...")
        
        # Initialize arrays to store trajectory
        timesteps = []
        x_positions = []
        y_positions = []
        z_positions = []
        
        # Read data for each timestep
        for step in range(steps):
            # Read timestep number
            ntimestep = reader.read("ntimestep", step_selection=[step, 1])[0]
            
            # Read atom data for this step
            atoms = reader.read("atoms", step_selection=[step, 1])
            
            # Read box dimensions for this step
            boxxlo = reader.read("boxxlo", step_selection=[step, 1])[0]
            boxxhi = reader.read("boxxhi", step_selection=[step, 1])[0]
            boxylo = reader.read("boxylo", step_selection=[step, 1])[0]
            boxyhi = reader.read("boxyhi", step_selection=[step, 1])[0]
            boxzlo = reader.read("boxzlo", step_selection=[step, 1])[0]
            boxzhi = reader.read("boxzhi", step_selection=[step, 1])[0]
            
            # Find the specific atom
            atom_indices = np.where(atoms[:, 0] == atom_id)[0]
            
            if len(atom_indices) == 0:
                print(f"Warning: Atom {atom_id} not found at timestep {ntimestep}")
                continue
            
            # Extract atom data (id, type, xs, ys, zs)
            atom_data = atoms[atom_indices[0]]
            xs_scaled = atom_data[2]
            ys_scaled = atom_data[3]
            zs_scaled = atom_data[4]
            
            # Convert scaled coordinates to real coordinates
            x_real = xs_scaled * (boxxhi - boxxlo) + boxxlo
            y_real = ys_scaled * (boxyhi - boxylo) + boxylo
            z_real = zs_scaled * (boxzhi - boxzlo) + boxzlo
            
            # Store trajectory data
            timesteps.append(ntimestep)
            x_positions.append(x_real)
            y_positions.append(y_real)
            z_positions.append(z_real)
            
            if step % 5 == 0:  # Print progress every 5 steps
                print(f"  Step {step}/{steps-1}: t={ntimestep} ps, pos=({x_real:.2f}, {y_real:.2f}, {z_real:.2f}) Å")
        
        # Convert to numpy arrays
        timesteps = np.array(timesteps)
        x_positions = np.array(x_positions)
        y_positions = np.array(y_positions)
        z_positions = np.array(z_positions)
        
        # Convert timesteps to picoseconds (timestep * 0.001)
        time_ps = timesteps * 0.001
        
        # Create the plot
        fig = plt.figure(figsize=(16, 12))
        
        # 3D trajectory plot
        ax1 = fig.add_subplot(2, 2, 1, projection='3d')
        
        # Color points by time
        colors = plt.cm.viridis(np.linspace(0, 1, len(timesteps)))
        
        # Plot trajectory as a line
        ax1.plot(x_positions, y_positions, z_positions, 'b-', alpha=0.6, linewidth=1)
        
        # Plot points colored by time
        scatter = ax1.scatter(x_positions, y_positions, z_positions, c=time_ps, 
                             cmap='viridis', s=20, alpha=0.8)
        
        # Mark start and end points
        ax1.scatter(x_positions[0], y_positions[0], z_positions[0], 
                   c='red', s=100, marker='o', label='Start')
        ax1.scatter(x_positions[-1], y_positions[-1], z_positions[-1], 
                   c='blue', s=100, marker='s', label='End')
        
        ax1.set_xlabel('X (Å)')
        ax1.set_ylabel('Y (Å)')
        ax1.set_zlabel('Z (Å)')
        ax1.set_title(f'3D Trajectory of Atom {atom_id}')
        ax1.legend()
        
        # Add colorbar for time
        cbar = plt.colorbar(scatter, ax=ax1, shrink=0.5)
        cbar.set_label('Time (ps)')
        
        # X vs time
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(time_ps, x_positions, 'r-', linewidth=2)
        ax2.set_xlabel('Time (ps)')
        ax2.set_ylabel('X Position (Å)')
        ax2.set_title(f'X Position vs Time - Atom {atom_id}')
        ax2.grid(True, alpha=0.3)
        
        # Y vs time
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(time_ps, y_positions, 'g-', linewidth=2)
        ax3.set_xlabel('Time (ps)')
        ax3.set_ylabel('Y Position (Å)')
        ax3.set_title(f'Y Position vs Time - Atom {atom_id}')
        ax3.grid(True, alpha=0.3)
        
        # Z vs time
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(time_ps, z_positions, 'b-', linewidth=2)
        ax4.set_xlabel('Time (ps)')
        ax4.set_ylabel('Z Position (Å)')
        ax4.set_title(f'Z Position vs Time - Atom {atom_id}')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        if output_file is None:
            output_file = f'/home/jcernuda/demo_adios/atom_{atom_id}_trajectory.png'
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nTrajectory plot saved as: {output_file}")
        
        # Calculate and print statistics
        print(f"\nTrajectory Statistics for Atom {atom_id}:")
        print(f"  Simulation time: {time_ps[0]:.3f} to {time_ps[-1]:.3f} ps")
        print(f"  Initial position: ({x_positions[0]:.2f}, {y_positions[0]:.2f}, {z_positions[0]:.2f}) Å")
        print(f"  Final position: ({x_positions[-1]:.2f}, {y_positions[-1]:.2f}, {z_positions[-1]:.2f}) Å")
        
        # Calculate displacement
        displacement = np.sqrt((x_positions[-1] - x_positions[0])**2 + 
                             (y_positions[-1] - y_positions[0])**2 + 
                             (z_positions[-1] - z_positions[0])**2)
        print(f"  Total displacement: {displacement:.2f} Å")
        
        # Calculate average velocity
        total_distance = 0
        for i in range(1, len(x_positions)):
            step_distance = np.sqrt((x_positions[i] - x_positions[i-1])**2 + 
                                  (y_positions[i] - y_positions[i-1])**2 + 
                                  (z_positions[i] - z_positions[i-1])**2)
            total_distance += step_distance
        
        avg_velocity = total_distance / (time_ps[-1] - time_ps[0])
        print(f"  Average speed: {avg_velocity:.2f} Å/ps")
        
        # Calculate positional variance (measure of mobility)
        x_var = np.var(x_positions)
        y_var = np.var(y_positions)
        z_var = np.var(z_positions)
        print(f"  Positional variance: X={x_var:.2f}, Y={y_var:.2f}, Z={z_var:.2f} Å²")
        
        return timesteps, x_positions, y_positions, z_positions

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Plot trajectory of a single atom in LAMMPS simulation')
    parser.add_argument('atom_id', type=int, help='ID of the atom to track')
    parser.add_argument('-o', '--output', type=str, help='Output filename for the plot')
    
    args = parser.parse_args()
    
    # Check if atom ID is valid (should be between 1 and 7813)
    if args.atom_id < 1 or args.atom_id > 7813:
        print(f"Error: Atom ID must be between 1 and 7813")
        sys.exit(1)
    
    # Plot the trajectory
    plot_atom_trajectory(args.atom_id, args.output)

if __name__ == "__main__":
    main()