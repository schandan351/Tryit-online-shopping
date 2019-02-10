from django.shortcuts import render

# importing models
from .utils import *
from .model_builder import *
from .my_cnn_model import *
from .shades import *

# Create your views here.

def tryit(request):
    import tensorflow as tf 
    tf.reset_default_graph() 
    df=detectface()
    context={
        'df':df,
    }
    return render(request,'face.html',context)

