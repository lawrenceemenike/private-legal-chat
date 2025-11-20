from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from src.core.config import settings
import os

def get_llm():
    """
    Initializes and returns the LlamaCpp LLM instance.
    Ensures the model file exists before attempting to load.
    """
    if not os.path.exists(settings.MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at {settings.MODEL_PATH}. "
            "Please download the GGUF model and place it in the 'models' directory."
        )

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=settings.MODEL_PATH,
        n_ctx=settings.N_CTX,
        n_gpu_layers=settings.N_GPU_LAYERS,
        temperature=settings.TEMPERATURE,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        streaming=True,
    )
    
    return llm
