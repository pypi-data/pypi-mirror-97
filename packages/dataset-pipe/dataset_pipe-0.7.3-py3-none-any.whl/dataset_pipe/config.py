import os

pickle = {
    "w2v_folder": os.environ['W2V_FOLDER'] if 'W2V_FOLDER' in os.environ
    else '/pickle/embeddings/word2vec/allegro'
}