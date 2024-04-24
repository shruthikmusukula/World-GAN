# Code based on https://github.com/tamarott/SinGAN
import torch
import torch.nn as nn
import torch.nn.functional as F

from .conv_block import ConvBlock


class Level_WDiscriminator(nn.Module):
    """ Patch based Discriminator. Uses Namespace opt. """
    def __init__(self, opt):
        super().__init__()
        self.is_cuda = torch.cuda.is_available()
        N = int(opt.nfc)
        self.N = N
        dim = len(opt.level_shape)
        kernel = tuple(opt.ker_size for _ in range(dim))
        self.head = ConvBlock(opt.nc_current, N, kernel, 0, 1, dim, drop=True)  # Padding is done externally
        self.body = nn.Sequential()

        for i in range(opt.num_layer - 2):
            block = ConvBlock(N, N, kernel, 0, 1, dim, drop=True)
            self.body.add_module("block%d" % (i + 1), block)

        block = ConvBlock(N, N, kernel, 0, 1, dim, drop=True)
        self.body.add_module("block%d" % (opt.num_layer - 2), block)

        if dim == 2:
            self.tail = nn.Conv2d(N, 1, kernel_size=kernel, stride=1, padding=1)
            #self.tail = nn.Linear(1536,1,bias=True)
        elif dim == 3:
            self.tail = nn.Conv3d(N, 1, kernel_size=kernel, stride=1, padding=1)
            #self.tail = nn.Linear(1536,1,bias=True)
        else:
            raise NotImplementedError("Can only make 2D or 3D Conv Layers.")

    def forward(self, x):
        #print("input: ", x.shape)
        #x = x.view(-1, 1, 43, 10, 8, 10)
        #print("input after view: ", x.shape)
        x = self.head(x)
        inner = self.body(x)
        #print("inner: ", inner.shape)

        out = self.tail(inner)
        #print("out: ", out.shape)
        #inner = inner.view(-1, self.N)
        #print("innerafter: ", inner.shape)
        return out, inner
