#!/usr/bin/env python
"""
batch_compute_num_faces.py

Finds all .ply/.obj in a folder, counts faces, writes face_counts.csv.
Usage: python batch_compute_num_faces.py C:\path\to\mesh_folder
"""
import sys, os, glob, csv
import pymeshlab as ml

def compute_face_count(mesh_path):
    ms = ml.MeshSet()
    ms.load_new_mesh(mesh_path)
    return ms.current_mesh().face_number()

def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_compute_num_faces.py C:\\path\\to\\mesh_folder")
        sys.exit(1)

    folder = sys.argv[1]
    files = []
    for pat in ('*.ply','*.obj'):
        files += glob.glob(os.path.join(folder, pat))
    if not files:
        print(f"No .ply or .obj found in {folder}")
        sys.exit(1)

    out_csv = os.path.join(folder, 'face_counts.csv')
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['filename','face_count'])
        for path in sorted(files):
            fc = compute_face_count(path)
            w.writerow([os.path.basename(path), str(fc)])
            print(f"Processed {os.path.basename(path)} → {fc}")

    print(f"\nDone! Results in {out_csv}")

if __name__ == '__main__':
    main()
