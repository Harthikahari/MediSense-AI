# Sample Medical Images

This directory contains sample/placeholder images for testing the MediSense-AI image analysis features.

## Image Categories

### Dermatology Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `skin_rash_001.jpg` | Contact dermatitis on forearm | contact_dermatitis (87%) |
| `mole_back_001.jpg` | Suspicious mole on back | melanocytic_nevus (62%) |
| `scalp_001.jpg` | Seborrheic dermatitis | seborrheic_dermatitis (85%) |

### Wound Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `foot_wound_001.jpg` | Diabetic foot ulcer | diabetic_foot_ulcer (78%) |

### ENT Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `throat_001.jpg` | Viral pharyngitis | pharyngitis_viral (72%) |
| `tongue_001.jpg` | White patches on tongue | pending analysis |

### Eye Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `eye_001.jpg` | Bacterial conjunctivitis | conjunctivitis_bacterial (55%) |

### Endocrine Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `neck_swelling_001.jpg` | Thyroid goiter | thyroid_nodule (68%) |

### Musculoskeletal Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `knee_001.jpg` | Osteoarthritis flare | osteoarthritis_flare (75%) |

### Radiology Images
| Image | Description | Expected AI Prediction |
|-------|-------------|----------------------|
| `chest_xray_001.jpg` | Mild cardiomegaly | cardiomegaly_mild (65%) |

## Image Specifications

For production use, images should meet these requirements:

- **Format**: JPEG or PNG
- **Resolution**: Minimum 640x480 pixels
- **Size**: Maximum 10MB
- **Color**: RGB color space
- **Lighting**: Well-lit, clear focus

## Privacy Notice

All images in this directory are synthetic/placeholder images for testing purposes only.
No actual patient images or PHI are stored in this repository.

## Usage in Development

```python
# Example: Load and analyze an image
from app.agents.image_agent import ImageAgent

agent = ImageAgent()
result = await agent.run({
    "query": "analyze image",
    "context": {
        "image_path": "/sample_data/images/skin_rash_001.jpg",
        "body_part": "forearm",
        "symptom_description": "Red, itchy rash"
    },
    "session_id": "test_session"
})

print(result.response)
# Output: {"prediction": "contact_dermatitis", "confidence": 0.87}
```

## Adding New Sample Images

1. Add image file to this directory
2. Update the `image_analyses` table in the SQL seed data
3. Document the image in this README
4. Ensure no PHI is included in image metadata
