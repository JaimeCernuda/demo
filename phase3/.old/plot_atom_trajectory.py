#!/usr/bin/env python3
"""
Plot the trajectory of a single atom over time from nanoparticles.bp5 dataset
"""

import adios2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import sys

def plot_atom_trajectory(file_path, atom_id, output_file="atom_trajectory.png"):
    """Plot the trajectory of a specific atom over time"""
    
    try:
        # Initialize ADIOS2
        adios = adios2.Adios()
        io = adios.declare_io("TrajectoryIO")
        
        # Open file for reading
        engine = io.open(str(file_path), adios2.bindings.Mode.Read)
        
        # Storage for trajectory data
        trajectory_data = {
            'steps': [],
            'x': [],
            'y': [],
            'z': [],
            'time': []
        }
        
        step_count = 0
        timestep_size = 0.001  # ps, from documentation
        
        print(f"Reading trajectory data for atom {atom_id}...")
        
        while True:
            step_status = engine.begin_step()
            if step_status != adios2.bindings.StepStatus.OK:
                break
            
            current_step = engine.current_step()
            
            # Get atoms data for this step
            atoms_var = io.inquire_variable("atoms")
            if atoms_var:
                atoms_shape = atoms_var.shape()
                print(f"Step {current_step}: atoms shape = {atoms_shape}")
                
                # Read atoms data
                atoms_data = np.empty(atoms_shape, dtype=np.float64)
                engine.get(atoms_var, atoms_data)
                
                # Find the specific atom
                atom_found = False
                for i, atom in enumerate(atoms_data):
                    if len(atom) >= 5 and int(atom[0]) == atom_id:
                        # atom format: [id, type, x, y, z]
                        trajectory_data['steps'].append(current_step)
                        trajectory_data['x'].append(atom[2])
                        trajectory_data['y'].append(atom[3])
                        trajectory_data['z'].append(atom[4])
                        trajectory_data['time'].append(current_step * timestep_size)
                        atom_found = True
                        break
                
                if not atom_found:
                    print(f"Warning: Atom {atom_id} not found in step {current_step}")
            
            engine.end_step()
            step_count += 1
            
            # Limit processing for testing
            if step_count > 50:
                break
        
        engine.close()
        
        if not trajectory_data['steps']:
            print(f"Error: No data found for atom {atom_id}")
            return False
        
        print(f"Found {len(trajectory_data['steps'])} data points for atom {atom_id}")
        
        # Create the plot
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Atom {atom_id} Trajectory Analysis', fontsize=16)
        
        # 3D trajectory
        ax1 = axes[0, 0]
        ax1.plot(trajectory_data['x'], trajectory_data['y'], 'b-', alpha=0.6, linewidth=1)
        ax1.scatter(trajectory_data['x'][0], trajectory_data['y'][0], color='green', s=100, label='Start', zorder=5)
        ax1.scatter(trajectory_data['x'][-1], trajectory_data['y'][-1], color='red', s=100, label='End', zorder=5)
        ax1.set_xlabel('X (Å)')
        ax1.set_ylabel('Y (Å)')
        ax1.set_title('XY Trajectory')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.axis('equal')
        
        # X, Y, Z coordinates vs time
        ax2 = axes[0, 1]
        ax2.plot(trajectory_data['time'], trajectory_data['x'], 'r-', label='X', linewidth=2)
        ax2.plot(trajectory_data['time'], trajectory_data['y'], 'g-', label='Y', linewidth=2)
        ax2.plot(trajectory_data['time'], trajectory_data['z'], 'b-', label='Z', linewidth=2)
        ax2.set_xlabel('Time (ps)')
        ax2.set_ylabel('Position (Å)')
        ax2.set_title('Position vs Time')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Distance from origin
        distances = np.sqrt(np.array(trajectory_data['x'])**2 + 
                           np.array(trajectory_data['y'])**2 + 
                           np.array(trajectory_data['z'])**2)
        ax3 = axes[1, 0]
        ax3.plot(trajectory_data['time'], distances, 'purple', linewidth=2)
        ax3.set_xlabel('Time (ps)')
        ax3.set_ylabel('Distance from Origin (Å)')
        ax3.set_title('Distance from Origin vs Time')
        ax3.grid(True, alpha=0.3)
        
        # Displacement from initial position
        initial_pos = np.array([trajectory_data['x'][0], trajectory_data['y'][0], trajectory_data['z'][0]])
        displacements = []
        for i in range(len(trajectory_data['x'])):
            current_pos = np.array([trajectory_data['x'][i], trajectory_data['y'][i], trajectory_data['z'][i]])
            displacement = np.linalg.norm(current_pos - initial_pos)
            displacements.append(displacement)
        
        ax4 = axes[1, 1]
        ax4.plot(trajectory_data['time'], displacements, 'orange', linewidth=2)
        ax4.set_xlabel('Time (ps)')
        ax4.set_ylabel('Displacement (Å)')
        ax4.set_title('Displacement from Initial Position')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Trajectory plot saved to {output_file}")
        
        # Print summary statistics
        print("\n" + "="*50)
        print("TRAJECTORY SUMMARY")
        print("="*50)
        print(f"Atom ID: {atom_id}")
        print(f"Total time steps: {len(trajectory_data['steps'])}")
        print(f"Time range: {trajectory_data['time'][0]:.3f} - {trajectory_data['time'][-1]:.3f} ps")
        print(f"Initial position: ({trajectory_data['x'][0]:.3f}, {trajectory_data['y'][0]:.3f}, {trajectory_data['z'][0]:.3f}) Å")
        print(f"Final position: ({trajectory_data['x'][-1]:.3f}, {trajectory_data['y'][-1]:.3f}, {trajectory_data['z'][-1]:.3f}) Å")
        print(f"Total displacement: {displacements[-1]:.3f} Å")
        print(f"Average displacement: {np.mean(displacements):.3f} Å")
        print(f"Maximum displacement: {np.max(displacements):.3f} Å")
        
        return True
        
    except Exception as e:
        print(f"Error plotting trajectory: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_available_atoms(file_path, max_steps=5):
    """Get a list of available atom IDs from the dataset"""
    
    try:
        adios = adios2.Adios()
        io = adios.declare_io("AtomListIO")
        engine = io.open(str(file_path), adios2.bindings.Mode.Read)
        
        atom_ids = set()
        step_count = 0
        
        while step_count < max_steps:
            step_status = engine.begin_step()
            if step_status != adios2.bindings.StepStatus.OK:
                break
            
            atoms_var = io.inquire_variable("atoms")
            if atoms_var:
                atoms_shape = atoms_var.shape()
                atoms_data = np.empty(atoms_shape, dtype=np.float64)
                engine.get(atoms_var, atoms_data)
                
                for atom in atoms_data:
                    if len(atom) >= 1:
                        atom_ids.add(int(atom[0]))
            
            engine.end_step()
            step_count += 1
        
        engine.close()
        return sorted(list(atom_ids))
        
    except Exception as e:
        print(f"Error getting atom list: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Plot atom trajectory from nanoparticles.bp5 dataset')
    parser.add_argument('--atom-id', type=int, help='Atom ID to plot trajectory for')
    parser.add_argument('--output', default='atom_trajectory.png', help='Output PNG file name')
    parser.add_argument('--list-atoms', action='store_true', help='List available atom IDs')
    
    args = parser.parse_args()
    
    file_path = Path("data/nanoparticles.bp5")
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return 1
    
    if args.list_atoms:
        print("Getting available atom IDs...")
        atom_ids = get_available_atoms(file_path)
        if atom_ids:
            print(f"Available atom IDs: {atom_ids[:20]}...")  # Show first 20
            print(f"Total atoms: {len(atom_ids)}")
        else:
            print("No atoms found")
        return 0
    
    # If no atom ID provided, use the first available atom
    if args.atom_id is None:
        print("Getting first available atom ID...")
        atom_ids = get_available_atoms(file_path)
        if atom_ids:
            args.atom_id = atom_ids[0]
            print(f"Using atom ID: {args.atom_id}")
        else:
            print("Error: No atoms found in dataset")
            return 1
    
    success = plot_atom_trajectory(file_path, args.atom_id, args.output)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())