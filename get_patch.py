from build_dataset import BuildDataset

patch_labels = ["Buff","Nerf","Rework"]


for patch_ver in (patch_versions):
    patch = BuildDataset(patch_ver)
    for patch_lab in (patch_labels):
        patch.build_data(patch_lab,True)

for patch_ver in (patch_versions):
    patch = BuildDataset(patch_ver)
    for patch_lab in (patch_labels):
        patch.build_data(patch_lab,True)