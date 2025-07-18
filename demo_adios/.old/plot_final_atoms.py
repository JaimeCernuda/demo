#!/usr/bin/env python3
"""
Plot the positions of gold atoms at the final timestep of the LAMMPS simulation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_atoms_from_adios():
    """Read atom positions from ADIOS BP5 file at final timestep."""
    try:
        import adios2 as adios
    except ImportError:
        print("Error: adios2 not available. Please install adios2-python.")
        return None
    
    # Create ADIOS2 instance
    adios_instance = adios.Adios()
    
    # Open the BP5 file
    io = adios_instance.declare_io("reader")
    engine = io.open('/home/jcernuda/demo_adios/Lammps-melting-gold.bp5', adios.bindings.Mode.Read)
    
    # Go to the final step (step 26)
    for step in range(27):
        engine.begin_step()
        if step == 26:
            # Read atom data
            atoms_var = io.inquire_variable('atoms')
            atoms = np.zeros(atoms_var.shape(), dtype=np.float64)
            engine.get(atoms_var, atoms)
            
            # Read box dimensions
            boxxlo_var = io.inquire_variable('boxxlo')
            boxxhi_var = io.inquire_variable('boxxhi')
            boxylo_var = io.inquire_variable('boxylo')
            boxyhi_var = io.inquire_variable('boxyhi')
            boxzlo_var = io.inquire_variable('boxzlo')
            boxzhi_var = io.inquire_variable('boxzhi')
            
            boxxlo = np.array([0.0])
            boxxhi = np.array([0.0])
            boxylo = np.array([0.0])
            boxyhi = np.array([0.0])
            boxzlo = np.array([0.0])
            boxzhi = np.array([0.0])
            
            engine.get(boxxlo_var, boxxlo)
            engine.get(boxxhi_var, boxxhi)
            engine.get(boxylo_var, boxylo)
            engine.get(boxyhi_var, boxyhi)
            engine.get(boxzlo_var, boxzlo)
            engine.get(boxzhi_var, boxzhi)
            
            engine.end_step()
            break
        engine.end_step()
    
    engine.close()
    
    # Extract positions (columns 2, 3, 4 are x, y, z coordinates)
    # Note: positions are in scaled coordinates, need to convert to actual coordinates
    atom_ids = atoms[:, 0]
    atom_types = atoms[:, 1]
    x_scaled = atoms[:, 2]
    y_scaled = atoms[:, 3]
    z_scaled = atoms[:, 4]
    
    # Convert scaled coordinates to actual coordinates
    x = x_scaled * (boxxhi[0] - boxxlo[0]) + boxxlo[0]
    y = y_scaled * (boxyhi[0] - boxylo[0]) + boxylo[0]
    z = z_scaled * (boxzhi[0] - boxzlo[0]) + boxzlo[0]
    
    return x, y, z, atom_ids

def plot_atoms(x, y, z, atom_ids):
    """Create 3D scatter plot of atom positions."""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create scatter plot
    scatter = ax.scatter(x, y, z, c=atom_ids, cmap='viridis', s=1, alpha=0.6)
    
    # Set labels and title
    ax.set_xlabel('X Position (Å)')
    ax.set_ylabel('Y Position (Å)')
    ax.set_zlabel('Z Position (Å)')
    ax.set_title('Gold Atom Positions at Final Timestep (t = 26 ps)\n7,813 atoms after heating to 2,500 K')
    
    # Add colorbar
    plt.colorbar(scatter, ax=ax, label='Atom ID', shrink=0.5)
    
    # Set equal aspect ratio
    ax.set_box_aspect([1,1,1])
    
    # Show grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/jcernuda/demo_adios/final_atoms_plot.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function to read data and create plot."""
    print("Reading atom positions from ADIOS BP5 file...")
    
    result = read_atoms_from_adios()
    if result is None:
        return
    
    x, y, z, atom_ids = result
    
    print(f"Successfully read {len(x)} atoms")
    print(f"X range: {x.min():.2f} to {x.max():.2f} Å")
    print(f"Y range: {y.min():.2f} to {y.max():.2f} Å")
    print(f"Z range: {z.min():.2f} to {z.max():.2f} Å")
    
    print("Creating 3D plot...")
    plot_atoms(x, y, z, atom_ids)
    print("Plot saved as 'final_atoms_plot.png'")

if __name__ == "__main__":
    main()