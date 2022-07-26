import csv, datetime


class EmptyFov(Exception):
    pass


def main():
    ra = float(input("Write Ra "))
    dec = float(input("Write Dec "))
    N = int(input("Write amount of stars "))
    fov_h = float(input("Write horizontal field of view "))
    fov_v = float(input("Write vertical field of view "))

    with open("small_dataset.tsv") as file:
        tsv_file = csv.reader(file, delimiter='\t')
        tsv_file_data = list(tsv_file)

    def filtering_dataset_by_columns(dataset: list, *columns: str) -> list:
        necessary_data = []
        for i in range(2, len(dataset)):
            try:
                necessary_data.append([float(dataset[i][dataset[1].index(col)])
                                       for col in columns])
                necessary_data[-1].insert(0, i - 1)
            except ValueError:
                raise ValueError("The cell is empty or has an invalid type of "
                                 "value. Please check the dataset and the row - "
                                 + str(i)) from None
        return necessary_data

    stars_parameters = filtering_dataset_by_columns(tsv_file_data, "ra_ep2000",
                                                    "dec_ep2000", "b")

    def selecting_stars_in_fov_and_filtering_by_brightness(horizontal_view: float,
                                                           vertical_view: float) -> list:
        filtered_stars = []
        fov_right_edge = (ra + horizontal_view / 2) % 360
        fov_left_edge = (ra - horizontal_view / 2) % 360
        fov_upper_edge = (dec + vertical_view / 2) % 360
        fov_bottom_edge = (dec - vertical_view / 2) % 360

        if fov_upper_edge > 90:
            raise ValueError("The upper edge of fov cannot "
                             "be more than 90 degrees")
        elif fov_bottom_edge < -90:
            raise ValueError("The bottom edge of fov cannot "
                             "be less than -90 degrees")

        for i in range(len(stars_parameters)):
            is_the_star_in_fovh = (fov_left_edge < 0 and
                                   (360 + fov_left_edge <= stars_parameters[i][1]
                                    <= 360)) or \
                                  (fov_left_edge >= 0 and
                                   (fov_left_edge <= stars_parameters[i][1]
                                    <= fov_right_edge))
            if is_the_star_in_fovh and \
                    fov_bottom_edge <= stars_parameters[i][2] <= fov_upper_edge:
                filtered_stars.append(stars_parameters[i])

        for i in range(len(filtered_stars) - 1):
            for j in range(len(filtered_stars) - i - 1):
                if filtered_stars[j][3] < filtered_stars[j + 1][3]:
                    filtered_stars[j], filtered_stars[j + 1] = \
                        filtered_stars[j + 1], filtered_stars[j]
        if filtered_stars:
            return filtered_stars[-N - 1:-1]
        else:
            raise EmptyFov("There are no stars in this fov, please try again")

    stars_in_fov = selecting_stars_in_fov_and_filtering_by_brightness(fov_h, fov_v)

    def calculating_and_sorting_distances_of_stars(star_ra: float,
                                                   star_dec: float, stars: list) -> list:
        for i in range(len(stars)):
            temp_ra = stars[i][1]
            temp_dec = stars[i][2]
            distance = ((star_ra - temp_ra) ** 2 +
                        (star_dec - temp_dec) ** 2) ** 0.5
            stars[i].append(distance)

        for i in range(len(stars) - 1):
            for j in range(len(stars) - i - 1):
                if stars[j][-1] > stars[j + 1][-1]:
                    stars[j], stars[j + 1] = stars[j + 1], stars[j]

        return stars

    calculating_and_sorting_distances_of_stars(ra, dec, stars_in_fov)
    header = ["Id", "Ra", "Dec", "Brightness", "Distance"]
    current_time = datetime.datetime.now()
    current_timestamp = current_time.timestamp()

    with open(str(current_timestamp) + ".csv", "w") as fl:
        writer = csv.writer(fl)
        writer.writerow(header)
        writer.writerows(stars_in_fov)


if __name__ == "__main__":
    main()
