#!/usr/bin/env python3
"""
Detailed analysis of the nanoparticles.bp5 ADIOS2 dataset
"""

import adios2
import numpy as np
import sys
import json
from pathlib import Path

def analyze_nanoparticles_detailed(file_path):
    """Perform detailed analysis of the nanoparticles.bp5 dataset"""
    
    results = {
        "dataset_info": {},
        "variables": {},
        "sample_data": {},
        "summary": {}
    }
    
    try:
        # Initialize ADIOS2 with streaming mode
        adios = adios2.Adios()
        io = adios.declare_io("DetailedAnalysisIO")
        
        # Open file for reading
        engine = io.open(str(file_path), adios2.bindings.Mode.Read)
        
        # Get basic info
        available_vars = io.available_variables()
        results["dataset_info"] = {
            "file_path": str(file_path),
            "num_variables": len(available_vars),
            "variable_names": list(available_vars.keys())
        }
        
        print(f"Dataset: {file_path}")
        print(f"Variables: {list(available_vars.keys())}")
        
        # Analyze each step
        step_count = 0
        sample_steps = []
        
        while True:
            step_status = engine.begin_step()
            if step_status != adios2.bindings.StepStatus.OK:
                break
                
            current_step = engine.current_step()
            print(f"\nProcessing step {current_step} (step_count: {step_count})")
            
            step_data = {"step": current_step, "variables": {}}
            
            # Read scalar variables for this step
            for var_name in available_vars:
                try:
                    variable = io.inquire_variable(var_name)
                    if variable:
                        var_shape = variable.shape()
                        var_type = variable.type()
                        
                        if var_name not in results["variables"]:
                            results["variables"][var_name] = {
                                "type": str(var_type),
                                "shape": var_shape,
                                "is_scalar": len(var_shape) == 0 or (len(var_shape) == 1 and var_shape[0] == 1),
                                "values_across_steps": []
                            }
                        
                        # Read scalar values
                        if len(var_shape) == 0:  # Scalar variable
                            if var_type == adios2.bindings.DataType.Double:
                                value = np.array(0.0, dtype=np.float64)
                                engine.get(variable, value)
                                step_data["variables"][var_name] = float(value)
                            elif var_type == adios2.bindings.DataType.UInt64:
                                value = np.array(0, dtype=np.uint64)
                                engine.get(variable, value)
                                step_data["variables"][var_name] = int(value)
                            elif var_type == adios2.bindings.DataType.Int32:
                                value = np.array(0, dtype=np.int32)
                                engine.get(variable, value)
                                step_data["variables"][var_name] = int(value)
                        
                        elif len(var_shape) == 1 and var_shape[0] == 1:  # Single element array
                            if var_type == adios2.bindings.DataType.UInt64:
                                value = np.empty(var_shape, dtype=np.uint64)
                                engine.get(variable, value)
                                step_data["variables"][var_name] = int(value[0])
                        
                        # For large arrays like 'atoms', just get metadata
                        elif var_name == "atoms":
                            step_data["variables"][var_name] = {
                                "shape": var_shape,
                                "type": str(var_type),
                                "size": np.prod(var_shape) if var_shape else 0
                            }
                
                except Exception as e:
                    print(f"  Error reading variable {var_name}: {e}")
            
            engine.end_step()
            
            # Store sample steps (first 3 and last 3)
            if step_count < 3 or step_count >= max(0, step_count - 3):
                sample_steps.append(step_data)
            
            step_count += 1
            if step_count > 50:  # Limit to prevent excessive processing
                break
        
        engine.close()
        
        results["dataset_info"]["total_steps"] = step_count
        results["sample_data"]["steps"] = sample_steps
        
        # Generate summary statistics
        results["summary"] = {
            "total_steps": step_count,
            "total_variables": len(available_vars),
            "variable_types": {},
            "scalar_variables": [],
            "array_variables": [],
            "time_series_analysis": {}
        }
        
        # Analyze variables
        for var_name, var_info in results["variables"].items():
            var_type = var_info["type"]
            results["summary"]["variable_types"][var_type] = results["summary"]["variable_types"].get(var_type, 0) + 1
            
            if var_info["is_scalar"]:
                results["summary"]["scalar_variables"].append(var_name)
            else:
                results["summary"]["array_variables"].append(var_name)
        
        # Analyze time series data from sample steps
        for var_name in results["summary"]["scalar_variables"]:
            values = []
            steps = []
            for step_data in sample_steps:
                if var_name in step_data["variables"]:
                    values.append(step_data["variables"][var_name])
                    steps.append(step_data["step"])
            
            if len(values) > 1:
                results["summary"]["time_series_analysis"][var_name] = {
                    "min": min(values),
                    "max": max(values),
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "trend": "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "stable"
                }
        
        return results
        
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
        return {"error": str(e)}

def main():
    file_path = Path("data/nanoparticles.bp5")
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return 1
    
    print("Performing detailed analysis of nanoparticles dataset...")
    print("=" * 60)
    
    results = analyze_nanoparticles_detailed(file_path)
    
    if "error" in results:
        print(f"Analysis failed: {results['error']}")
        return 1
    
    # Save results
    output_file = Path("nanoparticles_detailed_analysis.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed analysis complete. Results saved to {output_file}")
    
    # Print comprehensive summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE DATASET SUMMARY")
    print("=" * 60)
    
    info = results["dataset_info"]
    summary = results["summary"]
    
    print(f"File: {info['file_path']}")
    print(f"Total steps: {summary['total_steps']}")
    print(f"Total variables: {summary['total_variables']}")
    
    print(f"\nVariable types distribution:")
    for var_type, count in summary["variable_types"].items():
        print(f"  {var_type}: {count}")
    
    print(f"\nScalar variables ({len(summary['scalar_variables'])}):")
    for var in summary["scalar_variables"]:
        print(f"  - {var}")
    
    print(f"\nArray variables ({len(summary['array_variables'])}):")
    for var in summary["array_variables"]:
        print(f"  - {var}")
    
    print(f"\nTime series analysis (scalar variables):")
    for var_name, stats in summary["time_series_analysis"].items():
        print(f"  {var_name}: {stats['trend']} trend, range=[{stats['min']:.2f}, {stats['max']:.2f}]")
    
    print(f"\nSample data from {len(results['sample_data']['steps'])} steps available in JSON file")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())