#!/usr/bin/env python3
"""
Script to analyze the nanoparticles.bp5 ADIOS2 dataset
"""

import adios2
import numpy as np
import sys
import json
from pathlib import Path

def analyze_nanoparticles_bp5(file_path):
    """Analyze the nanoparticles.bp5 ADIOS2 dataset"""
    
    results = {
        "dataset_info": {},
        "variables": {},
        "steps": [],
        "summary": {}
    }
    
    try:
        # Initialize ADIOS2
        adios = adios2.Adios()
        
        # Open the BP5 file for reading
        io = adios.declare_io("AnalysisIO")
        engine = io.open(str(file_path), adios2.bindings.Mode.ReadRandomAccess)
        
        # Get available variables
        variables = io.available_variables()
        print(f"Available variables: {list(variables.keys())}")
        
        # Get number of steps
        steps = engine.steps()
        print(f"Number of steps: {steps}")
        
        results["dataset_info"]["file_path"] = str(file_path)
        results["dataset_info"]["num_steps"] = steps
        results["dataset_info"]["num_variables"] = len(variables)
        
        # Analyze each variable
        for var_name, var_info in variables.items():
            print(f"\nAnalyzing variable: {var_name}")
            
            var_data = {
                "name": var_name,
                "type": var_info.get("Type", "Unknown"),
                "shape": var_info.get("Shape", "Unknown"),
                "min": var_info.get("Min", "Unknown"),
                "max": var_info.get("Max", "Unknown"),
                "single_value": var_info.get("SingleValue", "Unknown")
            }
            
            results["variables"][var_name] = var_data
            
            # Try to read the variable at different steps
            try:
                variable = io.inquire_variable(var_name)
                if variable:
                    print(f"  Type: {variable.type()}")
                    print(f"  Shape: {variable.shape()}")
                    print(f"  Steps: {variable.steps()}")
                    
                    # Update variable data with more detailed info
                    var_data["detailed_type"] = str(variable.type())
                    var_data["detailed_shape"] = variable.shape()
                    var_data["variable_steps"] = variable.steps()
                    
                    # Try to read a small sample of data
                    if variable.steps() > 0:
                        engine.begin_step()
                        try:
                            if variable.type() == adios2.DataType.Double:
                                data = np.empty(variable.shape(), dtype=np.float64)
                                engine.get(variable, data)
                                engine.end_step()
                                
                                var_data["sample_stats"] = {
                                    "mean": float(np.mean(data)),
                                    "std": float(np.std(data)),
                                    "min": float(np.min(data)),
                                    "max": float(np.max(data)),
                                    "shape": data.shape
                                }
                                
                            elif variable.type() == adios2.DataType.Int32:
                                data = np.empty(variable.shape(), dtype=np.int32)
                                engine.get(variable, data)
                                engine.end_step()
                                
                                var_data["sample_stats"] = {
                                    "mean": float(np.mean(data)),
                                    "std": float(np.std(data)),
                                    "min": int(np.min(data)),
                                    "max": int(np.max(data)),
                                    "shape": data.shape
                                }
                        except Exception as e:
                            print(f"  Error reading data: {e}")
                            if engine.begin_step():
                                engine.end_step()
                            
            except Exception as e:
                print(f"  Error inquiring variable: {e}")
        
        # Get step information
        for step in range(min(steps, 5)):  # Analyze first 5 steps
            try:
                engine.begin_step()
                step_info = {
                    "step": step,
                    "variables_available": len(engine.available_variables())
                }
                results["steps"].append(step_info)
                engine.end_step()
            except Exception as e:
                print(f"Error reading step {step}: {e}")
        
        # Generate summary
        results["summary"] = {
            "total_variables": len(variables),
            "total_steps": steps,
            "variable_types": {},
            "recommendations": []
        }
        
        # Count variable types
        for var_name, var_data in results["variables"].items():
            var_type = var_data.get("detailed_type", var_data.get("type", "Unknown"))
            results["summary"]["variable_types"][var_type] = results["summary"]["variable_types"].get(var_type, 0) + 1
        
        # Add recommendations
        if steps > 100:
            results["summary"]["recommendations"].append("Large number of time steps - consider temporal analysis")
        
        if len(variables) > 10:
            results["summary"]["recommendations"].append("Multiple variables available - consider correlation analysis")
        
        engine.close()
        
        return results
        
    except Exception as e:
        print(f"Error analyzing dataset: {e}")
        return {"error": str(e)}

def main():
    file_path = Path("data/nanoparticles.bp5")
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return 1
    
    print(f"Analyzing nanoparticles dataset: {file_path}")
    print("=" * 50)
    
    results = analyze_nanoparticles_bp5(file_path)
    
    if "error" in results:
        print(f"Analysis failed: {results['error']}")
        return 1
    
    # Save results to JSON file
    output_file = Path("nanoparticles_analysis.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis complete. Results saved to {output_file}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("DATASET SUMMARY")
    print("=" * 50)
    
    print(f"File: {results['dataset_info']['file_path']}")
    print(f"Number of steps: {results['dataset_info']['num_steps']}")
    print(f"Number of variables: {results['dataset_info']['num_variables']}")
    
    print("\nVariables:")
    for var_name, var_data in results["variables"].items():
        print(f"  - {var_name}: {var_data.get('detailed_type', var_data.get('type'))}")
        if "sample_stats" in var_data:
            stats = var_data["sample_stats"]
            print(f"    Shape: {stats['shape']}, Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
    
    print(f"\nVariable types: {results['summary']['variable_types']}")
    
    if results['summary']['recommendations']:
        print(f"\nRecommendations:")
        for rec in results['summary']['recommendations']:
            print(f"  - {rec}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())