def chunk_text_from_file(file_path, chunk_on="\n"):
    try:
        with open(file_path, "r") as f:
            text = f.read()
            return [text]
            # Split into chunks by paragraph - each blank line becomes a split point
            # strip() removes extra whitespace, and the if-check skips empty chunks
            # return [chunk.strip() for chunk in text.split(chunk_on) if chunk.strip()]
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except PermissionError:
        print(f"Permission denied to read the file {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
