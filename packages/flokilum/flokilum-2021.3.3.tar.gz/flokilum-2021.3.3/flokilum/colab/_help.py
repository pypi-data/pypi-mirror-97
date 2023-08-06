MESSAGE = """
### session info
flokilum.colab.info()

### google drive
gdrive = flokilum.colab.gdrive()

### utils: np, einops, mpl, sns
np = flokilum.colab.numpy()
mpl, plt, sns = flokilum.colab.matplotlib()

%matplotlib inline
plt.style.use("seaborn")
from einops import rearrange

### spacy
spacy = flokilum.colab.spacy()

### spacy english
spacy_ensm = flokilum.colab.spacy_ensm()
spacy_enmd = flokilum.colab.spacy_enmd()
spacy_enlg = flokilum.colab.spacy_enlg()
spacy_entr = flokilum.colab.spacy_entr()

### spacy german
spacy_desm = flokilum.colab.spacy_desm()

### pytorch
torch, device = flokilum.colab.torch()
torchtext = flokilum.colab.torchtext()
torchvision = flokilum.colab.torchvision()

### tensorboard
tensorboard = flokilum.colab.tensorboard()
%load_ext tensorboard
"""

def help():

    print(MESSAGE)
