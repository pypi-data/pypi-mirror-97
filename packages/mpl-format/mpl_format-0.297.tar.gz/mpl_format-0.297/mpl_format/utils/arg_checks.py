def check_h_align(h_align: str):

    if h_align not in ('left', 'center', 'right'):
        raise ValueError("h_align not in ('left', 'center', 'right')")


def check_v_align(h_align: str):

    if h_align not in ('top', 'center', 'bottom'):
        raise ValueError("v_align not in ('top', 'center', 'bottom')")
