"""
MCP Server for Phishing URL Detection
"""

import logging
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from utils.enhanced_feature_extractor import EnhancedFeatureExtractor
from utils.model_loader import model_loader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

extractor = EnhancedFeatureExtractor()


mcp = FastMCP("phishing-url-detection-server")


@mcp.tool(
    name="extract_features",
    description="Extract 35+ phishing detection features from a URL for model input or analysis.",
)
def extract_features(url: str) -> Dict[str, Any]:
    """Extract 35+ phishing detection features from a given URL.

    Args:
        url: URL to analyze
    Returns:
        dict: Extracted features
    """
    features = extractor.extract_features(url)
    logger.info(f"Extracted features for URL: {url}")
    return features


@mcp.tool(
    name="predict",
    description="Predict phishing probability for a URL using extracted features and the trained model.",
)
def predict(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict phishing probability using the trained model.

    Args:
        features: Features dict as extracted from URL
    Returns:
        dict: Prediction result containing is_phishing, confidence, and details
    """
    result = model_loader.predict(features)
    logger.info(f"Prediction result: {result}")
    return result if result else {"error": "Prediction failed"}


@mcp.tool(
    name="load_model",
    description="Load or reload the phishing detection model and feature columns.",
)
def load_model(
    model_path: str = "models/phishing_model.pkl",
    features_path: str = "models/model_features.json",
) -> Dict[str, Any]:
    """Load or reload the phishing detection model and feature columns.

    Args:
        model_path: Path to the model file
        features_path: Path to the features file
    Returns:
        dict: Load status and feature columns
    """
    success = model_loader.load_model(model_path, features_path)
    logger.info(f"Model loaded: {success}")
    return {"success": success, "features": model_loader.feature_columns}


if __name__ == "__main__":
    mcp.run()
