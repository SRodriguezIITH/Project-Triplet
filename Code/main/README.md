# MoCap Data Processing Pipeline

A Python-based pipeline for processing and converting motion capture (mocap) data between multiple formats. This tool handles the conversion of raw mocap data from TXT format to JSON and finally to BVH (Biovision Hierarchy - FUTURE NOT CURRENTLY) format for use in animation and simulation applications like Unity.

NOTE: Use mocap.json for initializing unity animation

## Project Overview

This project provides a complete motion capture processing workflow:
- **Input**: Raw mocap data in TXT format (tab-separated marker position data)
- **Processing**: Data normalization, down-sampling, and marker extraction
- **Output**: Standardized BVH (skeletal animation) format suitable for animation platforms

## Project Structure

```
.
├── __init__.py              # Package initialization
├── test.py                  # Test file
├── bin/                     # Binary/executable files
├── data/                    # Data directory (mocap files)
│   ├── mocap.json
│   ├── walk_shake_hands.c3d
│   ├── mocap_bvh/          # BVH output files
│   ├── mocap_c3d/           # C3D format mocap files
│   ├── mocap_json/          # JSON intermediate format
│   └── mocap_txt/           # Raw TXT mocap data
├── libs/                    # Core processing library
│   ├── __init__.py
│   ├── process.py          # Main MotionPipeline class
│   └── run.py              # Entry point script
├── util/                    # Utilities
│   ├── preprocessing/       # Data preprocessing
│   │   ├── bvhmaker.py     # BVH format generator
│   │   └── dataloader.py   # TXT data loader
│   └── params/
│       └── config.yaml     # Configuration file
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the repository**:
```bash
cd /path/to/Project\ Triplet/Code/main
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv .env
```

3. **Activate the virtual environment**:
   - **Linux/macOS**:
     ```bash
     source .env/bin/activate
     ```
   - **Windows**:
     ```bash
     .env\Scripts\activate
     ```

4. **Install required dependencies**:
```bash
pip install pandas numpy scipy pyyaml
```

### Dependencies

- `pandas`: Data manipulation and CSV/tabular data handling
- `numpy`: Numerical computing and array operations
- `scipy`: Scientific computing (used for rotation calculations)
- `pyyaml`: YAML configuration file parsing

## Configuration

The pipeline configuration is defined in `util/params/config.yaml`:

```yaml
folders:
  mocap_txt: "main/data/mocap_txt"        # Input directory with raw TXT files
  mocap_json: "main/data/mocap_json"      # Output directory for JSON files
  mocap_bvh: "main/data/mocap_bvh"        # Final output directory for BVH files
```

Modify this file to change input/output paths as needed.

## Usage

### Running the Pipeline

Execute the main pipeline from the project root directory:

```bash
python -m libs.run
```

Or directly:
```bash
python libs/run.py
```

### What the Pipeline Does

[USE THIS]
1. **TXT to JSON Conversion** (`convert_txt_to_json`):
   - Reads raw mocap data from TXT files in `mocap_txt/`
   - Skips metadata header rows (default: 5 rows)
   - Extracts marker positions (X, Y, Z coordinates)
   - Removes duplicate and invalid markers
   - Exports normalized data to JSON format in `mocap_json/`
   - Frame rate: 120 Hz (configurable)


2. **JSON to BVH Conversion** (`convert_json_to_bvh`) [NOT NECESSARY FOR CURRENT UNITY STRUCTURE] :
   - Reads processed marker data from JSON files
   - Creates skeleton hierarchy from marker data
   - Generates BVH format files suitable for animation platforms
   - Outputs to `mocap_bvh/`

### Processing Parameters

You can adjust processing parameters in the code:

**DataLoader parameters** (in `libs/process.py`):
- `skip_header_rows`: Number of metadata rows before the column headers (default: 5)
- `downsample_factor`: Downsampling factor for frame reduction (default: 1, no downsampling)
- `frame_rate`: Output frame rate in Hz (default: 120)

**BVHMaker parameters**:
- `scale`: Scaling factor for marker positions (default: 1.0)

## Data Format Specifications

### Input Format (TXT)

Tab-separated values with:
- 5 header rows (metadata)
- Marker data with column names formatted as: `MarkerName_X`, `MarkerName_Y`, `MarkerName_Z`
- One row per frame

### Intermediate Format (JSON)

```json
{
  "markers": ["marker1", "marker2", ...],
  "frames": [
    [x1, y1, z1, x2, y2, z2, ...],
    ...
  ],
  "frame_rate": 120
}
```

### Output Format (BVH)

Standard Biovision Hierarchy format compatible with:
- Blender
- Maya
- MotionBuilder
- Unity (via additional plugins)
- Other 3D animation software

## Troubleshooting

### Import Errors
If you encounter import errors, ensure the virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### File Not Found Errors
- Verify that input files exist in the directory specified in `config.yaml`
- Check that the directory paths are correct (relative to project root)
- Ensure you're running the script from the project root directory

### Data Processing Issues
- Verify TXT file format (tab-separated, expected header rows)
- Check that marker columns follow the naming convention: `MarkerName_X/Y/Z`
- Review console output for specific error messages during processing

## Output Location

Processed files are saved to:
- **JSON files**: `main/data/mocap_json/`
- **BVH files**: `main/data/mocap_bvh/`

## Example Workflow

```python
# Example: Custom processing with modified parameters
from libs.process import MotionPipeline
import os

# Define paths
folder_path = "main/data/mocap_txt"
json_folder = "main/data/mocap_json"
bvh_folder = "main/data/mocap_bvh"

# Initialize pipeline
pipeline = MotionPipeline(folder_path, json_folder, bvh_folder)

# Run conversions
pipeline.convert_txt_to_json()
pipeline.convert_json_to_bvh()
```

## Future Enhancements

- Support for additional input formats (C3D, FBX)
- Real-time motion streaming
- Motion data filtering and smoothing
- Skeleton mapping customization
- Batch processing with progress tracking

## License

[Add your license info here]

## Support

For issues or questions, please check the troubleshooting section or review the source code documentation in:
- `libs/process.py` - Main pipeline orchestration
- `util/preprocessing/dataloader.py` - Data loading and conversion logic
- `util/preprocessing/bvhmaker.py` - BVH format generation

