from datetime import datetime
from pathlib import Path

folder = Path(r"C:\Users\paulh\OneDrive\Desktop\EU_VID")

for file in sorted(folder.iterdir()):
    if file.is_file():
        name = file.stem
        # print(name)
        date_string = name.split(" ", 1)[1]
        date = datetime.strptime(
            date_string,
            "%b %d %Y, %I %M %S %p"
        )
        print(date)
        # time = str(file)[58:68]
        # print(time[8:])
        # print(file)
        # new_name = f"{str(file)[45:-4]} {str(file)[39:44]}{file.suffix.lower()}"
        # new_path = folder / new_name

        # print(new_path)
        # file.rename(new_path)

        # print(f"{file.name} -> {new_name}")
        # number += 1


# from pathlib import Path

# file = Path("Photo Aug 18 2026, 5 41 16 PM.jpg")

# name = file.stem

# # Remove "Photo " or "Video "
# date_string = name.split(" ", 1)[1]

# date = datetime.strptime(
#     date_string,
#     "%b %d %Y, %I %M %S %p"
# )

# print(date)