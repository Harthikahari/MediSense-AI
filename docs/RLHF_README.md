# RLHF (Reinforcement Learning from Human Feedback) Pipeline

## Overview

MediSense-AI includes infrastructure for collecting human feedback and using it to improve agent responses through Reinforcement Learning from Human Feedback (RLHF).

## Pipeline Architecture

```
1. Response Generation → 2. Feedback Collection → 3. Reward Model Training → 4. Policy Optimization
```

## Components

### 1. Feedback Collection

#### UI for Clinician Feedback

Clinicians can rate agent responses:
- **Thumbs up/down** (binary)
- **Star rating** (1-5 stars)
- **Comparative** (choose better of two responses)
- **Free-text comments**

#### Feedback Data Format

```json
{
  "feedback_id": "fb_abc123",
  "session_id": "sess_xyz789",
  "agent_name": "prescription_agent",
  "user_query": "Prescribe treatment for hypertension",
  "agent_response": "I recommend starting with lisinopril 10mg...",
  "rating": 5,
  "feedback_type": "positive",
  "clinician_id": 123,
  "timestamp": "2025-01-17T12:00:00Z",
  "comments": "Appropriate first-line treatment"
}
```

#### Preference Pairs Format (for Comparative Feedback)

```jsonl
{"prompt": "What medication for type 2 diabetes?", "chosen": "Metformin 500mg twice daily...", "rejected": "Insulin immediately...", "metadata": {...}}
{"prompt": "Analyze this skin rash", "chosen": "Appears to be contact dermatitis...", "rejected": "Unable to determine from image", "metadata": {...}}
```

### 2. Reward Model Training

#### Dataset Preparation

```python
# backend/app/rlhf/prepare_dataset.py

from datasets import Dataset

def prepare_preference_dataset(feedback_file: str) -> Dataset:
    """
    Load feedback data and create preference pairs.

    Args:
        feedback_file: Path to JSONL file with feedback

    Returns:
        HuggingFace Dataset with preference pairs
    """
    pairs = []
    # Load and process feedback
    # Create (prompt, chosen, rejected) tuples
    return Dataset.from_list(pairs)
```

#### Training Script

```python
# backend/app/rlhf/train_reward_model.py

from transformers import AutoModelForSequenceClassification, TrainingArguments
from trl import RewardTrainer

def train_reward_model(
    base_model: str = "bert-base-uncased",
    dataset_path: str = "rlhf/data/preferences.jsonl",
    output_dir: str = "rlhf/models/reward_model"
):
    """
    Train a reward model from preference data.

    Args:
        base_model: Base transformer model
        dataset_path: Path to preference dataset
        output_dir: Output directory for trained model
    """
    # Load dataset
    dataset = prepare_preference_dataset(dataset_path)

    # Initialize model
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=1  # Regression for reward score
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        learning_rate=2e-5,
        logging_steps=100,
        save_steps=500,
        evaluation_strategy="steps",
        eval_steps=500
    )

    # Initialize trainer
    trainer = RewardTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"]
    )

    # Train
    trainer.train()
    trainer.save_model(output_dir)

    return model
```

### 3. Policy Optimization (PPO)

#### PPO Training Script

```python
# backend/app/rlhf/train_ppo.py

from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead
from transformers import AutoTokenizer

def train_with_ppo(
    base_model: str = "gpt2",
    reward_model_path: str = "rlhf/models/reward_model",
    output_dir: str = "rlhf/models/ppo_model"
):
    """
    Fine-tune agent policy using PPO.

    Args:
        base_model: Base language model
        reward_model_path: Path to trained reward model
        output_dir: Output directory for fine-tuned model
    """
    # Load models
    model = AutoModelForCausalLMWithValueHead.from_pretrained(base_model)
    reward_model = AutoModelForSequenceClassification.from_pretrained(reward_model_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    # PPO configuration
    ppo_config = PPOConfig(
        model_name=base_model,
        learning_rate=1.4e-5,
        batch_size=16,
        mini_batch_size=4,
        gradient_accumulation_steps=1,
        optimize_cuda_cache=True,
        early_stopping=True,
        target_kl=0.1,
        ppo_epochs=4,
        seed=42
    )

    # Initialize PPO trainer
    ppo_trainer = PPOTrainer(
        config=ppo_config,
        model=model,
        ref_model=None,  # Will use frozen copy of model
        tokenizer=tokenizer
    )

    # Training loop
    for epoch in range(ppo_config.ppo_epochs):
        for batch in dataloader:
            # Generate responses
            query_tensors = batch["input_ids"]
            response_tensors = ppo_trainer.generate(query_tensors)

            # Get rewards
            rewards = compute_rewards(
                response_tensors,
                reward_model,
                tokenizer
            )

            # PPO step
            stats = ppo_trainer.step(query_tensors, response_tensors, rewards)

            # Log statistics
            log_ppo_stats(stats)

    # Save fine-tuned model
    ppo_trainer.save_pretrained(output_dir)
```

## Data Collection Infrastructure

### API Endpoints

```python
# backend/app/api/v1/routes_rlhf.py

@router.post("/feedback")
async def submit_feedback(
    session_id: str,
    agent_name: str,
    rating: int,
    comments: str = None,
    user_id: int = Depends(get_current_user_id)
):
    """Submit feedback for an agent response."""
    # Store feedback in database
    # Trigger reward model retraining if threshold reached
    pass

@router.post("/preference")
async def submit_preference(
    prompt: str,
    response_a: str,
    response_b: str,
    preferred: str,  # "a" or "b"
    user_id: int = Depends(get_current_user_id)
):
    """Submit preference between two responses."""
    # Store preference pair
    # Add to training dataset
    pass
```

### Database Schema

```sql
CREATE TABLE rlhf_feedback (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR UNIQUE NOT NULL,
    session_id VARCHAR NOT NULL,
    agent_name VARCHAR NOT NULL,
    user_query TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_type VARCHAR,  -- 'positive', 'negative', 'neutral'
    clinician_id INTEGER REFERENCES users(id),
    comments TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE rlhf_preferences (
    id SERIAL PRIMARY KEY,
    preference_id VARCHAR UNIQUE NOT NULL,
    prompt TEXT NOT NULL,
    response_a TEXT NOT NULL,
    response_b TEXT NOT NULL,
    preferred CHAR(1) CHECK (preferred IN ('a', 'b')),
    clinician_id INTEGER REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);
```

## Training Workflow

### 1. Collect Feedback

```bash
# Continuous collection through UI and API
# Target: 1000+ feedback samples before first training
```

### 2. Prepare Dataset

```bash
cd backend
python -m app.rlhf.prepare_dataset \
    --feedback-db postgresql://... \
    --output rlhf/data/preferences.jsonl
```

### 3. Train Reward Model

```bash
python -m app.rlhf.train_reward_model \
    --base-model bert-base-uncased \
    --dataset rlhf/data/preferences.jsonl \
    --output rlhf/models/reward_model \
    --epochs 3 \
    --batch-size 16
```

### 4. Fine-tune with PPO

```bash
python -m app.rlhf.train_ppo \
    --base-model gpt2 \
    --reward-model rlhf/models/reward_model \
    --output rlhf/models/ppo_model \
    --epochs 4
```

### 5. Deploy Fine-tuned Model

```bash
# Update MCP configuration to use fine-tuned model
# Monitor performance metrics
# A/B test against baseline
```

## Cloud Training (Optional)

For large-scale training, use cloud compute:

### AWS SageMaker

```python
from sagemaker.huggingface import HuggingFace

# Configure training job
huggingface_estimator = HuggingFace(
    entry_point='train_reward_model.py',
    source_dir='./rlhf',
    instance_type='ml.p3.2xlarge',
    instance_count=1,
    role=role,
    transformers_version='4.26',
    pytorch_version='1.13',
    py_version='py39',
    hyperparameters={
        'epochs': 3,
        'batch_size': 16
    }
)

# Start training
huggingface_estimator.fit({'training': 's3://bucket/rlhf/data'})
```

## Monitoring & Evaluation

### Metrics to Track

1. **Feedback Volume**: Feedback samples per day
2. **Rating Distribution**: Distribution of 1-5 star ratings
3. **Agreement Rate**: Inter-rater reliability
4. **Model Performance**:
   - Reward model accuracy on held-out test set
   - PPO policy improvement over baseline

### A/B Testing

```python
# Randomly assign users to baseline vs. fine-tuned model
# Compare metrics:
# - User satisfaction ratings
# - Task completion rate
# - Response quality scores
```

## Best Practices

1. **Diverse Feedback**: Collect from multiple clinicians
2. **Quality Control**: Review feedback for consistency
3. **Regular Retraining**: Retrain every 1000 new feedback samples
4. **Gradual Rollout**: A/B test before full deployment
5. **Monitor Degradation**: Watch for performance drops
6. **Ethical Review**: Ensure fairness and safety

## Privacy Considerations

- **Anonymize Feedback**: Remove PHI from training data
- **Consent**: Obtain consent for feedback usage
- **Secure Storage**: Encrypt feedback data at rest
- **Access Control**: Limit access to training data

## Future Enhancements

1. **Active Learning**: Strategically request feedback on uncertain responses
2. **Multi-modal RLHF**: Include image/document quality feedback
3. **Real-time Learning**: Continuous online learning
4. **Federated Learning**: Privacy-preserving distributed training
5. **Constitutional AI**: Align with explicit safety principles

---

**Version**: 1.0.0
**Last Updated**: 2025-01-17

**Note**: This RLHF pipeline is a starting point. For production deployment, consult with ML engineers and ethicists to ensure robust, safe, and fair implementation.
