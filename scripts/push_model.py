#!/usr/bin/env python3
"""
Optimized script for uploading trained models to Hugging Face Hub.
"""

import os
import logging
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login, HfApi
import torch
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_model_to_hub(
    model_path: str,
    repo_name: str,
    hf_token: str = None,
    private: bool = False,
    use_auth_token: bool = True,
    torch_dtype: torch.dtype = torch.float16,
    device_map: str = "auto",
    trust_remote_code: bool = True
):
    """
    Upload a trained model to Hugging Face Hub with optimizations.
    
    Args:
        model_path: Local path to the model
        repo_name: Repository name on Hugging Face Hub
        hf_token: Hugging Face token (optional if set in environment)
        private: Whether to make the repository private
        use_auth_token: Whether to use authentication token
        torch_dtype: Data type for model loading
        device_map: Device mapping strategy
        trust_remote_code: Whether to trust remote code execution
    """
    
    # Validate inputs
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model path does not exist: {model_path}")
    
    # Get token from parameter or environment
    token = hf_token or os.getenv('HF_TOKEN') or os.getenv('hf_token')
    if not token:
        raise ValueError("Hugging Face token not found. Set HF_TOKEN environment variable or pass hf_token parameter.")
    
    try:
        # Login to Hugging Face
        logger.info("Logging in to Hugging Face Hub...")
        login(token=token)
        
        # Initialize HF API for repository management
        api = HfApi()
        
        # Create repository if it doesn't exist
        try:
            api.create_repo(repo_id=repo_name, private=private, exist_ok=True)
            logger.info(f"Repository '{repo_name}' ready")
        except Exception as e:
            logger.warning(f"Repository creation warning: {e}")
        
        # Load tokenizer first (lighter operation)
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            trust_remote_code=trust_remote_code
        )
        
        # Load model with optimizations
        logger.info("Loading model with optimizations...")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch_dtype,
            device_map=device_map,
            trust_remote_code=trust_remote_code,
            low_cpu_mem_usage=True  # Reduce CPU memory usage during loading
        )
        
        # Upload tokenizer first
        logger.info("Uploading tokenizer...")
        tokenizer.push_to_hub(
            repo_name,
            use_auth_token=use_auth_token,
            private=private
        )
        
        # Upload model
        logger.info("Uploading model...")
        model.push_to_hub(
            repo_name,
            use_auth_token=use_auth_token,
            private=private,
            safe_serialization=True  # Use safetensors format
        )
        
        repo_url = f"https://huggingface.co/{repo_name}"
        logger.info(f"✅ Model successfully uploaded to: {repo_url}")
        return repo_url
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise

def main():
    """Main execution function."""
    
    # Configuration
    MODEL_PATH = '/home/hoang.minh.an/anhalu-data/learning/cashbox/qwen-baseline-time-function-calling-v3'
    REPO_NAME = "anhalu/qwen-baseline-time-function-calling-v3"
    
    # Check if CUDA is available for potential optimizations
    if torch.cuda.is_available():
        logger.info(f"CUDA available: {torch.cuda.get_device_name()}")
    else:
        logger.info("CUDA not available, using CPU")
    
    try:
        # Upload model
        repo_url = upload_model_to_hub(
            model_path=MODEL_PATH,
            repo_name=REPO_NAME,
            private=True,  # Set to True if you want a private repository
        )
        
        print(f"\n🎉 Upload completed successfully!")
        print(f"Model URL: {repo_url}")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())