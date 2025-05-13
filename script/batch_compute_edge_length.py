#!/usr/bin/env python
import sys, os, glob, csv
import pymeshlab as ml

def compute_avg_edge(mesh_path):
    ms = ml.MeshSet()
    ms.load_new_mesh(mesh_path)
    stats = ms.get_geometric_measures()
    return stats['avg_edge_length']

def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_compute_edge_length.py C:\\path\\to\\mesh_folder")
        sys.exit(1)

    mesh_folder = sys.argv[1]
    # grab all OBJ and PLY files
    patterns = ['*.ply', '*.obj']
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(mesh_folder, pat)))

    if not files:
        print(f"No .ply or .obj files found in {mesh_folder}")
        sys.exit(1)

    out_csv = os.path.join(mesh_folder, 'edge_stats.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'avg_edge_length'])
        for fn in sorted(files):
            avg = compute_avg_edge(fn)
            writer.writerow([os.path.basename(fn), f"{avg:.6f}"])
            print(f"Processed {os.path.basename(fn)} → {avg:.6f}")

    print(f"\nAll done! Results in {out_csv}")

if __name__ == "__main__":
    main()
