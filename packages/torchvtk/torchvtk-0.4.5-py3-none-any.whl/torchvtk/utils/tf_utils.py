#%%
import torch
import torch.nn.functional as F
import numpy as np

from xml.dom import minidom
try:
    from torchinterp1d import Interp1d
except ImportError:
    _has_torchinterp1d = False
else:
    _has_torchinterp1d = True


def requires_torchinterp1d(func):
    def _dummy(*args, **kwargs):
        raise ImportError('You need to install torchinterp1d using:\n pip install git+https://github.com/aliutkus/torchinterp1d.git@master#egg=torchinterp1d')
    if _has_torchinterp1d: return func
    else:                  return _dummy




def read_inviwo_tf(fn):
    xmldoc = minidom.parse(str(fn))
    def parse_point(point):
        pos  = float(point.getElementsByTagName('pos')[0].getAttribute('content'))
        _, rgba = zip(*point.getElementsByTagName('rgba')[0].attributes.items())
        return pos, list(map(float, rgba))
    points = sorted(map(parse_point, xmldoc.getElementsByTagName('Point')))
    flat_points = list(map(lambda t: [t[0]] + t[1], points))

    return torch.cat([torch.zeros(5)[None], torch.tensor(flat_points), torch.eye(5)[None, 0]], dim=0)

def tex_from_pts(tf_pts, resolution=4096):
    ''' Interpolates `tf_pts` to generate a TF texture of shape (N, C, resolution) with C determined by the TF '''
    if isinstance(tf_pts, np.ndarray):
        tf_pts = torch.from_numpy(tf_pts)
    if torch.is_tensor(tf_pts):
        if tf_pts.ndim == 3:
            return torch.stack([tex_from_pts(tfp, resolution) for tfp in tf_pts])
        else:
            return apply_tf_torch(
            torch.linspace(0.0, 1.0, resolution,
                dtype=tf_pts.dtype, device=tf_pts.device),
            tf_pts)
    elif isinstance(tf_pts, (list, tuple)) and torch.is_tensor(tf_pts[0]):
        return torch.stack([tex_from_pts(tfp, resolution) for tfp in tf_pts])

@requires_torchinterp1d
def apply_tf_tex_torch(vol, tf_tex):
    ''' Applies a (batch of) transfer function textures `tf_tex` to a (batch of) volume `vol`

    Args:
        vol (torch.Tensor): ([N,] 1, D, H, W) volume with intensity values
        tf_tex (torch.Tensor): ([N,] C, R) transfer function texture with C channels and resolution R

    Returns:
        The preclassified volume of shape ([N,] C, D, H, W)
    '''
    nc, res = tf_tex.size(-2), tf_tex.size(-1)
    tf_tex = tf_tex.to(vol.device).to(torch.float32)
    out_shape = list(vol.shape)
    out_shape[-4] = nc
    tf_flat  = tf_tex.reshape(-1, res)
    x_flat   = torch.linspace(0, 1, res, device=vol.device, dtype=torch.float32).expand(tf_flat.size(0), -1)
    vol_flat = vol.expand(out_shape).reshape(tf_flat.size(0), -1).to(torch.float32)
    return Interp1d()(x_flat, tf_flat, vol_flat).reshape(out_shape).to(vol.dtype)

@requires_torchinterp1d
def apply_tf_torch(x, tf_pts):
    ''' Applies the TF described by points `tf_pts` (N x [0,1]^C+1 with x pos and C channels) to `x`. The operation always computes on torch.float32. The output is cast to `x.dtype`

    Args:
        x (torch.Tensor): The intensity values to apply the TF on. Assumed shape is ([N,] 1, ...) (optionally with batch size N, must match length of tf_pts list)
        tf_pts (torch.Tensor, List of such): Tensor of shape (N, (1+C)) containing N points consisting of x coordinate and mapped features (e.g. RGBO)

    Returns:
        torch.Tensor: Tensor with TF applied of shape (N, C, ...) with batch size N (same as `x`) and number of channels C (same as `tf_pts`)
    '''
    if isinstance(tf_pts, list) and x.ndim == 5:
        return torch.stack([apply_tf_torch(vol, tf) for vol, tf in zip(x, tf_pts)]) # If tf_pts is in a list, perform for each item in that list
    assert x.ndim < 5 and torch.is_tensor(tf_pts)
    dev = x.device
    tf_pts = tf_pts.to(dev)
    npt, nc = tf_pts.shape
    x_shap = tuple(x.shape)
    x_out_shap = (nc-1, *x_shap[-3:])
    x_acc   = torch.empty(x_out_shap,        dtype=torch.float32, device=dev)
    pts_acc = torch.empty((npt * (nc-1), 2), dtype=torch.float32, device=dev)
    for i in range(1,nc):
        x_acc[i-1] = x + (i-1) # make intensity volume of shape (nc, D,H,W), with intensity values offset by 1 for each channel
        pts_acc[(i-1)*npt:i*npt] = tf_pts[:, [0,i]] + torch.Tensor([[i-1,0.0]]).to(dev) # offset TF values (xRGBO) similarly to get all channels aligned to intensity [0, nc-1]
    return Interp1d()(pts_acc[:,0].float().contiguous(),
                      pts_acc[:,1].float().contiguous(),
                      x_acc.float().reshape(-1).contiguous()
                ).reshape(x_out_shap).to(x.dtype).contiguous() # Interp on flattened volume, reshape

class TransferFunctionApplication(torch.nn.Module):
    def __init__(self, as_pts=False):
        ''' A torch.nn.Module that applies a transfer function differentiably

        Args:
            as_pts (bool): Wether the given TF will be in point form (True) or 1D texture (False).
        '''
        super().__init__()
        self.as_pts     = as_pts

    def forward(self, x, tf):
        ''' Applies the transfer function `tf` to the volume `x`

        Args:
            x (torch.Tensor): Tensor depicting a volume with intensity values (N, 1, D, H, W)
            tf (torch.Tensor, list of such): If `as_pts` a list of Tensors (NumPoints, Channels) is expected with len(list) == batch_size. If False a torch.Tensor (N, Channels, TF_resolution).

        Returns:
            (torch.Tensor): Tensor with the TF applied. New shape (N, Channels, D, H, W)
        '''
        if self.as_pts: return apply_tf_torch(x, tf)
        else:           return apply_tf_tex_torch(x, tf)
