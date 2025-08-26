from solver.color_detection import detect_colors
from solver.cube_orient import orient_cube
from solver.solver import solve_cube
from utils.file_ops import load_images_from_folder  # we wrote this earlier

def start_processing(session_folder, result_label):
    faces_images = load_images_from_folder(session_folder)  # captured images
    if len(faces_images) != 6:
        result_label.config(text="Please capture 6 faces first")
        return

    # Detect colors
    detected_faces = [detect_colors(img) for img in faces_images]

    # Orient cube
    oriented = orient_cube(detected_faces)

    # Build cube string for solver
    cube_string = (
        "".join(oriented["U"]) +
        "".join(oriented["R"]) +
        "".join(oriented["F"]) +
        "".join(oriented["D"]) +
        "".join(oriented["L"]) +
        "".join(oriented["B"])
    )

    # Solve cube
    try:
        solution = solve_cube(cube_string)
        result_label.config(text=solution)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")
