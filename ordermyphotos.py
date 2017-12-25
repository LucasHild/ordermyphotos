import click
import exifread
import os
import shutil


def get_files(path):
    """Get a list of all files and count them"""
    files = os.listdir(path)
    # Ignore backup folder
    files = list(filter(lambda x: x != "backup_omp", files))

    length_files_start = len(files)
    return files, length_files_start


def backup(path, files):
    """Put all the photos in a subfolder called backup_omp"""
    try:
        os.mkdir(path + "/backup_omp")
    except FileExistsError:
        if input("\033[93mOverride folder backup_omp? (y/N) \033[0m") == "y":
            shutil.rmtree(path + "/backup_omp")
            os.mkdir(path + "/backup_omp")
        else:
            print("\033[91mExit\033[0m")
            exit()

    for file in files:
        shutil.copy2(path + "/" + file, path + "/backup_omp/" + file)


def get_dates(path, files):
    """Get the date of every photo and return dictionary"""
    photos = []

    for file in files:
        # Open file and get date
        with open(path + "/" + file, 'rb') as f:
            tags = exifread.process_file(f)
            date = tags["EXIF DateTimeOriginal"]

        photos.append({
            "name": file,
            "date": str(date)
        })

        os.remove(path + "/" + file)

    return photos


def order_photos(path, photos):
    """Sort photos and copy them to the root path"""
    photos.sort(key=lambda d: (d['date']))

    for index, photo in enumerate(photos):
        index += 1

        if index < 10:
            number = "000" + str(index)
        elif index < 100:
            number = "00" + str(index)
        elif index < 1000:
            number = "0" + str(index)
        else:
            number = str(index)

        shutil.copy2(path + "/backup_omp/" + photo["name"], path + "/DSC_" + number + ".JPG")


def main(path):
    print("Get files")
    files, length_files_start = get_files(path)

    print("Make backup")
    backup(path, files)

    print("Get dates")
    photos = get_dates(path, files)

    print("Order Photos")
    order_photos(path, photos)

    length_files_end = len(list(filter(lambda x: x != "backup_omp", os.listdir(path))))

    print("Number of Photos at Start: " + str(length_files_start))
    print("Number of Photos at End: " + str(length_files_end))

    print("\n\033[92mDone\033[0m")  # Green


@click.command()
@click.argument("path", type=click.Path(exists=True), default=".")
def cli(path):
    main(path)

if __name__ == "__main__":
    # Run if file is executed directly
    main(".")
