import zipfile

def compress_files(file_paths, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(file_path, arcname=file_path.split("/")[-1])
