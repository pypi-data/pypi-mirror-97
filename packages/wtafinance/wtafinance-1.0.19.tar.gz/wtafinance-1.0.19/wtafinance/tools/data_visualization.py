import matplotlib.pyplot as plt


def show(data):

    table = plt.table(cellText=data.to_numpy().tolist(), colLabels=list(data.columns), loc='center',
                      cellLoc='center')
    table.auto_set_font_size(False)
    h = table.get_celld()[(0, 0)].get_height()
    w = table.get_celld()[(0, 0)].get_width()

    # Create an additional Header
    header = [table.add_cell(-1, pos, w, h, loc="center", facecolor="none") for pos in [1, 2, 3]]
    header[0].visible_edges = "TBL"
    header[1].visible_edges = "TB"
    header[2].visible_edges = "TBR"
    header[1].get_text().set_text("Header Header Header Header")

    plt.axis('off')
    plt.show()



if __name__ == '__main__':
    data = [[1,2,3,4],[6,5,4,3],[1,3,5,1]]


