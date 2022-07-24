from torch import nn


class ResBlock(nn.Module):
    """
    construct a two-layers basic Res block
    """

    def __init__(self, ch_in, ch_out, kernel_size=3, padding=1, dilation=1, stride=1, norm=nn.BatchNorm2d):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size, stride,
                      padding, dilation, bias=False),
            norm(ch_out),
            nn.ReLU(True),
            nn.Conv2d(ch_out, ch_out, kernel_size, stride,
                      padding, dilation, bias=False),
            norm(ch_out),
        )
        self.shortcut = nn.Sequential()
        if stride != 1 or ch_in != ch_out:
            self.shortcut = nn.Sequential(
                nn.Conv2d(ch_in, ch_out, kernel_size=1,
                          stride=stride, bias=False),
                nn.BatchNorm2d(ch_out)
            )

    def forward(self, x):
        return nn.ReLU(True)(self.shortcut(x)+self.conv1(x))


class transResBlock(nn.Module):
    """
    construct a two-layers transConv Res block
    """

    def __init__(self, ch_in, ch_out, kernel_size=3, padding=1, stride=1, norm=nn.BatchNorm2d):
        super(transResBlock, self).__init__()
        self.conv1 = nn.Sequential(
            nn.ConvTranspose2d(ch_in, ch_out, kernel_size=kernel_size,
                               stride=stride, padding=padding, bias=False),
            norm(ch_out),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(ch_out, ch_out, kernel_size=kernel_size,
                               stride=stride, padding=padding, bias=False),
            norm(ch_out),
        )
        self.shortcut = nn.Sequential()
        if stride != 1 or ch_in != ch_out:
            self.shortcut = nn.Sequential(
                nn.Conv2d(ch_in, ch_out, kernel_size=1,
                          stride=stride, bias=False),
                nn.BatchNorm2d(ch_out)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.shortcut(x) + self.conv1(x))
