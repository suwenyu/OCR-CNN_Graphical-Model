import torch
import torch.nn as nn
import data_loader as dload
import tensorflow as tf
import numpy as np
import sys

class custom2D(nn.Module):
  def __init__(self, in_channels = 1, out_channels = 1, kernel_size = (3,3), padding = False, stride = 1):
    self.in_channels = in_channels
    self.out_channels = out_channels
    self.kernel_size = kernel_size
    self.padding = padding
    self.stride = stride

  def convolution_2d(self, letter, kernel):
    in_channels = self.in_channels
    out_channels = self.out_channels
    if(kernel.shape != self.kernel_size):
      print('Error: kernel passed with shape {}, should be shape {}'.format(kernel.shape, self.kernel_size))
      sys.exit()
    padding = self.padding
    stride = self.stride

    original_shape = letter.shape
    # isLetter = False

    #if it is a letter we are putting into the convolution (this restriction lets us test on assignment prompt matrix)
    if len(letter) == 128:
      # isLetter = True
      letter = letter.reshape([16,8])

    letter_length = letter.shape[0]
    letter_width = letter.shape[1]

    kernel_size = kernel.shape[0] #get the size of the kernel, we assume ours is a square

    #if there is padding, we need to account for it
    # if padding == True or isLetter:
    if padding == True:
      width_out = int(letter.shape[1])
      length_out = int(letter.shape[0])
      pad = (len(kernel) - 1) / 2
    else:
      width_out = int((letter_width - kernel_size)/stride +1)
      length_out = int((letter_length - kernel_size)/stride +1)
      pad = 0

    #make a bunch of zeroes in the form of a matrix that matches expected output
    to_return = np.zeros((int(length_out), int(width_out)))

    #update the to_return object
    for i in range(0,letter.shape[0] - kernel_size + 1, stride):
      for j in range(0, letter.shape[1] - kernel_size + 1, stride):
        section_of_interest = letter[i:i+kernel_size, j:j+kernel_size] #get the small area we want to look at with our kernel

        #for each section of interest, get the summed val for every 1/1 match
        summed_kernel_val = 0
        for k in range(0,kernel_size):
          for l in range(0, kernel_size):
            #add them all up together for that kernel section
            summed_kernel_val += section_of_interest[k,l] * kernel[k,l]

            #put the val into the to return variable
            temp_i = int(i/stride + pad)
            temp_j = int(j/stride + pad)
            to_return[temp_i,temp_j] = summed_kernel_val
    
    #if need to pad back to original shape, reshape back to original shape
    if padding == True:
      to_return = to_return.reshape(original_shape)
    #else return the smaller tensor
    else:
      to_return = to_return.reshape([length_out, width_out])
    return to_return