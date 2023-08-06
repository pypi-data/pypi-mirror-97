def resize(orig, limitation, upscale=False):
    """
    Return resized resolution.

    Arguments:
        orig: (w, h)
        limitation: (w, h)

    Keyword Arguments:
        upscale: Bool
            True: upscale if orig < limitation
            False: not upscale [default]

    Returns:
        (w, h)
    """
    Orig_w = orig[0]
    Orig_h = orig[1]
    Lmt_w = limitation[0]
    Lmt_h = limitation[1]

    if Lmt_w == 0:
        if Orig_h < Lmt_h and upscale == False:
            return (Orig_w, Orig_h)
        else:
            return (Orig_w*(Lmt_h/Orig_h), Lmt_h)
    elif Lmt_h == 0:
        if Orig_w < Lmt_w and upscale == False:
            return (Orig_w, Orig_h)
        else:
            return (Lmt_w, Orig_h*(Lmt_w/Orig_w))
    else:
        if Orig_w/Orig_h > Lmt_w/Lmt_h:
            if Orig_w < Lmt_w and upscale == False:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_w, Orig_h*(Lmt_w/Orig_w))
        elif Orig_w/Orig_h < Lmt_w/Lmt_h:
            if Orig_h < Lmt_h and upscale == False:
                return (Orig_w, Orig_h)
            else:
                return (Orig_w*(Lmt_h/Orig_h), Lmt_h)
        else:
            if Orig_w < Lmt_w and upscale == False:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_w, Lmt_h)
