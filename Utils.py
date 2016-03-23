def on_expose(parent, event=None):
    if parent.parent.os != 'Linux':
        return
    # Center widget on top of parent window
    parent_x = parent.parent.root.winfo_x()
    parent_y = parent.parent.root.winfo_y()
    parent_w = parent.parent.root.winfo_width()
    parent_x_mid = parent_x + (parent_w / 2)
    root_x = parent_x_mid - (parent.root.winfo_width() / 2)
    root_y = parent_y
    parent.root.geometry(
        str(parent.root.winfo_width()) + 'x' + str(parent.root.winfo_height()) + '+' + str(int(root_x)) + '+' + str(
            int(root_y)))

    parent.root.grab_set()
    parent.root.transient(parent.parent.root)


def on_close(parent, event=None):
    parent.root.grab_release()
    parent.root.destroy()
