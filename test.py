from sentence_transformers.models import Pooling, Transformer, Normalize
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os
load_dotenv()

module = Transformer('vinai/phobert-base-v2', max_seq_length=256)

pooling_layer = Pooling(
    word_embedding_dimension=module.get_word_embedding_dimension(),
    pooling_mode_mean_tokens=False,
    pooling_mode_cls_token=True,
    pooling_mode_max_tokens=False
)


model = SentenceTransformer(modules=[module, pooling_layer])


# model.save('model')

# model = SentenceTransformer('model')

# for x in model.named_modules():                                               
#     print(x)
    
print(model.encode("Thời_tiết đẹp"))

# model.push_to_hub('tanbinh2210/phobert-st', token=os.environ['HF_ADMIN_TOKEN'])