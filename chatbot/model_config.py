model_kwargs = {
    "n_ctx":32768,    # Context length to use
    "n_threads":4,   # Number of CPU threads to use
    "n_gpu_layers":-1,# Number of model layers to offload to GPU. Set to 0 if only using CPU
    "verbose":False
}

generation_kwargs = {
    "max_tokens":2500, # Max number of new tokens to generate
    "stop":["<|endoftext|>", "</s>"], # Text sequences to stop generation on
    #"echo":False, # Echo the prompt in the output
    "top_k":50
}

model_path = '/Users/nate/.cache/huggingface/hub/models--TheBloke--Mixtral-8x7B-Instruct-v0.1-GGUF/snapshots/fa1d3835c5d45a3a74c0b68805fcdc133dba2b6a/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf'
