#!/usr/bin/env python3
"""
Plot the positions of gold atoms at the final timestep of the LAMMPS melting simulation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from adios2 import FileReader

def plot_final_positions():
    """Read and plot atom positions at the final timestep."""
    
    # Open the BP5 file
    with FileReader("/home/jcernuda/demo_adios/Lammps-melting-gold.bp5") as reader:
        
        # Get available variables to understand the data structure
        vars_info = reader.available_variables()
        print("Available variables:")
        for name, info in vars_info.items():
            print(f"  {name}: {info}")
        
        # Get the number of steps
        steps = int(vars_info['ntimestep']['AvailableStepsCount'])
        print(f"\nTotal steps available: {steps}")
        
        # Read the final timestep number
        final_step = steps - 1
        ntimestep = reader.read("ntimestep", step_selection=[final_step, 1])
        print(f"Final timestep: {ntimestep[0]}")
        
        # Read atom positions at the final step
        # Note: atoms variable contains [id, type, xs, ys, zs] where xs, ys, zs are scaled coordinates
        atoms = reader.read("atoms", step_selection=[final_step, 1])
        
        # Read box dimensions
        boxxlo = reader.read("boxxlo", step_selection=[final_step, 1])[0]
        boxxhi = reader.read("boxxhi", step_selection=[final_step, 1])[0]
        boxylo = reader.read("boxylo", step_selection=[final_step, 1])[0]
        boxyhi = reader.read("boxyhi", step_selection=[final_step, 1])[0]
        boxzlo = reader.read("boxzlo", step_selection=[final_step, 1])[0]
        boxzhi = reader.read("boxzhi", step_selection=[final_step, 1])[0]
        
        print(f"Box dimensions: x=[{boxxlo}, {boxxhi}], y=[{boxylo}, {boxyhi}], z=[{boxzlo}, {boxzhi}]")
        
        # Extract atom data
        atom_ids = atoms[:, 0]
        atom_types = atoms[:, 1]
        xs_scaled = atoms[:, 2]  # scaled x coordinates
        ys_scaled = atoms[:, 3]  # scaled y coordinates
        zs_scaled = atoms[:, 4]  # scaled z coordinates
        
        # Convert scaled coordinates to real coordinates
        x_real = xs_scaled * (boxxhi - boxxlo) + boxxlo
        y_real = ys_scaled * (boxyhi - boxylo) + boxylo
        z_real = zs_scaled * (boxzhi - boxzlo) + boxzlo
        
        print(f"Number of atoms: {len(atom_ids)}")
        print(f"Coordinate ranges:")
        print(f"  X: [{x_real.min():.2f}, {x_real.max():.2f}] Å")
        print(f"  Y: [{y_real.min():.2f}, {y_real.max():.2f}] Å")
        print(f"  Z: [{z_real.min():.2f}, {z_real.max():.2f}] Å")
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot atoms as points
        scatter = ax.scatter(x_real, y_real, z_real, c=atom_ids, cmap='viridis', 
                           alpha=0.6, s=1)
        
        # Add colorbar
        plt.colorbar(scatter, ax=ax, label='Atom ID', shrink=0.5)
        
        # Set labels and title
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_zlabel('Z (Å)')
        ax.set_title(f'Gold Atom Positions at Final Timestep ({int(ntimestep[0])})\n'
                    f'Temperature: ~2500K (Melted State)')
        
        # Set equal aspect ratio
        ax.set_box_aspect([1,1,1])
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Show plot
        plt.tight_layout()
        plt.savefig('/home/jcernuda/demo_adios/final_positions.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create a 2D projection view (XY plane)
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        scatter2 = ax2.scatter(x_real, y_real, c=z_real, cmap='plasma', alpha=0.6, s=1)
        plt.colorbar(scatter2, ax=ax2, label='Z coordinate (Å)')
        ax2.set_xlabel('X (Å)')
        ax2.set_ylabel('Y (Å)')
        ax2.set_title(f'Gold Atom Positions - XY Projection (Final Timestep)\n'
                     f'Color represents Z coordinate')
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        
        plt.tight_layout()
        plt.savefig('/home/jcernuda/demo_adios/final_positions_xy.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return x_real, y_real, z_real, ntimestep[0]

if __name__ == "__main__":
    x, y, z, timestep = plot_final_positions()
    print(f"\nPlot saved as 'final_positions.png' and 'final_positions_xy.png'")
    print(f"Final timestep: {int(timestep)}")