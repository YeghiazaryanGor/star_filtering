import csv, math, sys, datetime

ra = 45  # float(input("Write Ra "))
dec = 44  # float(input("Write Dec "))
N = 10  # int(input("Write amount of stars "))
fov_h = 64  # float(input("Write horizontal field of view "))
fov_v = 78  # float(input("Write vertical field of view "))

with open("small_dataset.tsv") as file:
    tsv_file = csv.reader(file, delimiter='\t')
    tsv_file_data = list(tsv_file)


def filtering_dataset(dataset: list, *columns: str) -> list:
    """
      Selecting the columns that we will use during the task
     """
    necessary_data = []
    for i in range(2, len(dataset)):
        try:
            necessary_data.append([float(dataset[i][dataset[1].index(col)])
                                   for col in columns])
            necessary_data[-1].insert(0,i-1)
        except ValueError:
            raise
    return necessary_data


stars_parameters = filtering_dataset(tsv_file_data, "ra_ep2000",
                                     "dec_ep2000", "b")


def selecting_and_filtering_stars_in_fov(horizontal_view: float,
                                         vertical_view: float):
    """
       Selecting the stars that are in our field of view and
       sorting them by their brightness(from dimmest to brightest).
    """
    filtered_stars = []
    fov_right_edge = ra + horizontal_view / 2
    fov_left_edge = ra - horizontal_view / 2
    fov_upper_edge = dec + vertical_view / 2
    fov_bottom_edge = dec - vertical_view / 2
    for i in range(len(stars_parameters)):  # Selecting the stars in the fov
        if fov_left_edge <= stars_parameters[i][1] <= fov_right_edge and \
                fov_bottom_edge <= stars_parameters[i][2] <= fov_upper_edge:
            filtered_stars.append(stars_parameters[i])

    for i in range(len(filtered_stars) - 1):  # Sorting stars by brightness
        for j in range(len(filtered_stars) - i - 1):
            if filtered_stars[j][3] < filtered_stars[j + 1][3]:
                filtered_stars[j], filtered_stars[j + 1] = \
                    filtered_stars[j + 1], filtered_stars[j]

    return filtered_stars[-N - 1:-1] if filtered_stars else \
        sys.exit('There are no stars in the fov, please try again!')


stars_in_fov = selecting_and_filtering_stars_in_fov(fov_h, fov_v)

print(stars_in_fov)
