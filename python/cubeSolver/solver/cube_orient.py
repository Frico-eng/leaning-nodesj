def orient_cube(faces):
    """
    Orient 6 faces to U/D/F/B/L/R.
    Input: faces = list of 6 faces, each face is a list of 9 color names (row-major)
    Output: dict with keys 'U','D','F','B','L','R' and values = 9-color lists
    """
    # Map centers to face names
    face_map = {}
    for face in faces:
        center_color = face[4]  # center sticker
        if center_color == "white":
            face_map["U"] = face
        elif center_color == "yellow":
            face_map["D"] = face
        elif center_color == "green":
            face_map["F"] = face
        elif center_color == "blue":
            face_map["B"] = face
        elif center_color == "orange":
            face_map["L"] = face
        elif center_color == "red":
            face_map["R"] = face
        else:
            raise ValueError(f"Unknown center color: {center_color}")

    # Optional: rotate faces if needed (depending on capture orientation)
    # For now, we assume faces are top-down aligned
    # Later: implement rotation based on corner/edge matching

    return face_map
