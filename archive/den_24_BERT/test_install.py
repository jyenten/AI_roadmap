import transformers
import torch

print("transformesrs verze:", transformers.__version__)
print("torch verze", torch.__version__)
print("CUDA dostupna:", torch.cuda.is_available())