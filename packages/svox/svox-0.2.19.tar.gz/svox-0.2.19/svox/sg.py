"""Spherical Gaussians"""
#  [BSD 2-CLAUSE LICENSE]
#
#  Copyright SVOX Authors 2021
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.


import numpy as np
import math
import torch

def eval_sg(sg_lambda, sg_mu, sg_coeffs, dirs):
    """
    Evaluate spherical gaussians at unit directions
    using learnable SG basis.
    Works with torch.
    ... Can be 0 or more batch dimensions.
    N is the number of SG basis we use.
    :math:`Output = \sigma_{i}{exp ^ {\lambda_i * (\dot(\mu_i, \dirs) - 1)}`

    :param sg_lambda: The sharpness of the SG lobes. (N)
    :param sg_mu: The directions of the SG lobes. (N, 3)
    :param sg_coeffs: The coefficients of the SG (lob amplitude). (..., C, N)
    :param dirs: jnp.ndarray unit directions (..., 3)

    :return: (..., C)
    """
    
    product = torch.einsum(
        "ij,...j->...i", sg_mu, dirs)  # [..., N]
    basis = torch.exp(torch.einsum(
        "i,...i->...i", sg_lambda, product - 1))  # [..., N]
    output = torch.einsum(
        "...ki,...i->...k", sg_coeffs, basis)  # [..., C]
    output /= sg_mu.size(0)
    return output


def eval_sg_bases(sg_lambda, sg_mu, dirs):
    """
    Evaluate spherical gaussians bases at unit directions
    using learnable SG basis,
    without taking linear combination
    Works with torch.
    ... Can be 0 or more batch dimensions.
    N is the number of SG basis we use.
    :math:`Output = \sigma_{i}{exp ^ {\lambda_i * (\dot(\mu_i, \dirs) - 1)}`

    :param sg_lambda: The sharpness of the SG lobes. (N)
    :param sg_mu: The directions of the SG lobes. (N, 3)
    :param dirs: jnp.ndarray unit directions (..., 3)

    :return: (..., N)
    """
    product = torch.einsum(
        "ij,...j->...i", sg_mu, dirs)  # [..., N]
    basis = torch.exp(torch.einsum(
        "i,...i->...i", sg_lambda, product - 1))  # [..., N]
    return basis / sg_mu.size(0)
