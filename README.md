# Project Triplet

A comprehensive motion capture (MoCap) to biomechanically adherent movement generation, visualization, and pose estimation system. This project processes raw mocap data through a Python pipeline and visualizes it in a real-time interactive 3D environment using Unity.

## Summary

**Team Members:**
- Sonit Patil (BM23BTECH11023)
- Ojas Kurundkar (BM23BTECH11017)
- Abdul Haseeb (BM23BTECH11001)

**Project Scope:**
Project Triplet is a full-stack mocap processing and visualization system that:
- Processes raw motion capture data from various formats (TXT, C3D)
- Converts mocap data to standardized formats (JSON, BVH)
- Provides real-time 3D visualization and pose estimation
- Enables biomechanically accurate movement analysis

## Project Structure

```
Project Triplet/
├── Code/                           # Python pipeline for mocap data processing
│   ├── main/                       # Main processing pipeline
│   │   ├── libs/                   # Core processing library
│   │   ├── util/                   # Utilities (preprocessing, configs)
│   │   ├── data/                   # Input/output data directory
│   │   ├── bin/                    # Binary/executable files
│   │   ├── README.md               # Detailed pipeline documentation
│   │   └── test.py                 # Test scripts
│   └── mocap_test/                 # Test utilities for mocap
├── Visualization/                  # Unity project for 3D visualization
│   ├── main/                       # Main Unity project
│   │   ├── Assets/                 # Unity assets
│   │   ├── Movement_Visualiser/    # Movement visualization scripts
│   │   └── ProjectSettings/
│   ├── Mocap_Test/                 # Mocap testing environment
│   └── Unity-Tutorial/             # Reference tutorials
├── Notes/                          # Documentation and references
│   ├── FILE_FORMAT.md              # Mocap file format specifications
│   └── MOCAP_MARKERS.md            # MoCap marker protocol definitions
├── Resources/                      # Additional resources (currently empty)
├── Recording (mp4)/                # Video recordings of mocap data
├── SETUP.md                        # Setup instructions
└── README.md                       # This file

```

## Introduction

Motion capture is a technique that records the movement of objects or people, typically using markers placed on joints. Project Triplet creates a complete workflow for:

1. **Data Acquisition**: Processing raw MoCap data from CMU Motion Capture Database or other sources
2. **Data Processing**: Converting between multiple mocap formats (TXT, C3D, JSON, BVH)
3. **Visualization**: Real-time 3D rendering of skeletal animations in Unity
4. **Analysis**: Biomechanical pose estimation and movement validation

### Key Features

- **Multi-format support**: Handle TXT, C3D, JSON, and BVH formats
- **Standardized marker protocol**: Supports industry-standard MoCap marker configurations
- **Real-time visualization**: Interactive 3D movement visualization in Unity
- **Configurable pipeline**: Adjust frame rates, downsampling, and marker extraction
- **Biomechanical validation**: Process data according to biomechanical standards

## How To Run

### Prerequisites

- **Python 3.7+** (for data processing pipeline)
- **Unity 2020+** (for visualization)
- **pip** (Python package manager)

### Data Processing Pipeline

1. **Navigate to the Code/main directory**:
   ```bash
   cd "Project Triplet/Code/main"
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .env
   # Windows:
   .env\Scripts\activate
   # Linux/macOS:
   source .env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pandas numpy scipy pyyaml
   ```

4. **Run the pipeline**:
   ```bash
   python -m libs.run
   # OR
   python libs/run.py
   ```

5. **Output files** are generated in:
   - JSON format: `main/data/mocap_json/`
   - BVH format: `main/data/mocap_bvh/`

### Pipeline Features

The data processing pipeline (`Code/main/libs/process.py`) provides:

- **TXT to JSON Conversion**: Transforms raw mocap data to standardized JSON format
  - Reads marker positions (X, Y, Z coordinates)
  - Normalizes frame rate (default: 120 Hz)
  - Removes duplicate/invalid markers
  - Outputs to `mocap_json/`

- **JSON to BVH Conversion**: Converts to Biovision Hierarchy format (optional)
  - Creates skeleton hierarchy
  - Generates BVH files suitable for animation platforms
  - Outputs to `mocap_bvh/`

### Visualization in Unity

1. **Open the Unity project**:
   ```
   Visualization/main/Movement_Visualiser
   ```

2. **Load mocap data**:
   - Use the generated `mocap.json` file
   - Import through the Movement_Visualiser scripts

3. **Run in Unity Editor** or **Build for standalone execution**

## Configuration

### Data Processing Configuration

Edit `Code/main/util/params/config.yaml` to customize:

```yaml
folders:
  mocap_txt: "main/data/mocap_txt"        # Input directory
  mocap_json: "main/data/mocap_json"      # JSON output directory
  mocap_bvh: "main/data/mocap_bvh"        # BVH output directory
```

### Processing Parameters

Adjustable in `Code/main/libs/process.py`:
- `skip_header_rows`: Metadata rows to skip (default: 5)
- `downsample_factor`: Frame reduction factor (default: 1)
- `frame_rate`: Output frame rate in Hz (default: 120)
- `scale`: Marker position scaling (default: 1.0)

## Data Formats

### Input Formats (TXT)
- Tab-separated values
- 5 header rows (metadata)
- Marker data: `MarkerName_X`, `MarkerName_Y`, `MarkerName_Z`
- One row per frame

### Processing Formats (JSON)
```json
{
  "markers": ["marker1", "marker2", ...],
  "frames": [[x1, y1, z1, x2, y2, z2, ...], ...],
  "frame_rate": 120
}
```

### Output Formats (BVH)
- Standard Biovision Hierarchy format
- Compatible with: Blender, Maya, MotionBuilder, Unity, other 3D software

### Supported Markers

Refer to `Notes/MOCAP_MARKERS.md` for complete marker definitions:
- **Head**: LBHD, LFHD, RBHD, RFHD (skull orientation)
- **Spine/Torso**: C7, T10, STRN, CLAV (trunk orientation)
- **Pelvis**: LBWT, RBWT, LFWT, RFWT (pelvis orientation)
- **Upper Limbs**: LSHO, RSHO, LUPA, RUPA, LELB, RELB (arm segments)
- **Wrists/Hands**: LWRA, LWRB, RWRA, RWRB, LFIN (hand markers)

For detailed marker protocol, see `Notes/MOCAP_MARKERS.md`.

## Setup

For detailed setup instructions, refer to [SETUP.md](SETUP.md).

### Quick Setup Checklist

- [ ] Clone/download the repository
- [ ] Install Python 3.7+ and pip
- [ ] Set up virtual environment in `Code/main/`
- [ ] Install dependencies: `pandas`, `numpy`, `scipy`, `pyyaml`
- [ ] Configure `util/params/config.yaml` with data paths
- [ ] Place raw TXT mocap files in `main/data/mocap_txt/`
- [ ] Run pipeline: `python -m libs.run`
- [ ] Open Unity project in `Visualization/main/`
- [ ] Load generated JSON data for visualization

## Documentation

Additional documentation:
- **File Formats**: See `Notes/FILE_FORMAT.md` for all supported mocap formats
- **Marker Protocol**: See `Notes/MOCAP_MARKERS.md` for standard marker definitions
- **Pipeline Details**: See `Code/main/README.md` for detailed processing pipeline documentation
- **Data Loading**: `Code/main/util/preprocessing/dataloader.py` - TXT data loader
- **BVH Generation**: `Code/main/util/preprocessing/bvhmaker.py` - BVH format generator

## Troubleshooting

### Pipeline Issues

**Import Errors**
```bash
# Ensure virtual environment is activated and dependencies installed
pip install pandas numpy scipy pyyaml
```

**File Not Found**
- Verify input files in `main/data/mocap_txt/`
- Check `config.yaml` paths are correct
- Run from project root directory

**Data Processing Issues**
- Verify TXT format: tab-separated with expected header rows
- Confirm marker naming: `MarkerName_X/Y/Z`
- Check console output for specific errors

### Unity Visualization Issues

- Ensure JSON mocap file is properly generated
- Check movement data paths in Unity scripts
- Verify Unity version compatibility (2020+)

## Examples

### Data Processing Example

```python
from libs.process import MotionPipeline

# Define paths
pipeline = MotionPipeline(
    "main/data/mocap_txt",
    "main/data/mocap_json",
    "main/data/mocap_bvh"
)

# Run conversions
pipeline.convert_txt_to_json()
pipeline.convert_json_to_bvh()
```

### Custom Processing

```python
# Adjust processing parameters
from util.preprocessing.dataloader import DataLoader

loader = DataLoader(
    skip_header_rows=5,
    downsample_factor=2,  # Skip every 2nd frame
    frame_rate=60  # Output at 60 Hz
)
data = loader.load_from_file("mocap.txt")
```

## References

1. **CMU Motion Capture Database**: https://mocap.cs.cmu.edu/search.php?subjectnumber=18&trinum=1
   - Tool selection validation and sample data source
2. **BVH Format Specification**: Standard Biovision Hierarchy format for skeletal animation
3. **Motion Capture Marker Protocols**: Industry-standard marker placement and nomenclature

## Future Enhancements

- [ ] Support for additional input formats (FBX, streaming protocols)
- [ ] Real-time motion streaming capabilities
- [ ] Advanced motion filtering and smoothing
- [ ] Skeleton mapping customization
- [ ] Batch processing with progress tracking
- [ ] Web-based visualization interface
- [ ] Motion database and analysis tools

## License

[Add your license info here]

## Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review source code documentation:
   - `Code/main/libs/process.py` - Main pipeline orchestration
   - `Code/main/util/preprocessing/dataloader.py` - Data loading logic
   - `Code/main/util/preprocessing/bvhmaker.py` - BVH generation
3. Refer to `Notes/` documentation
4. Check `Code/main/README.md` for detailed pipeline docs
