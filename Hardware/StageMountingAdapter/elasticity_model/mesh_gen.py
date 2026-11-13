import gmsh
import numpy as np

gmsh.initialize()
# Load your STEP file directly
gmsh.model.occ.importShapes("mesh/beam.step")
gmsh.model.occ.synchronize()

# 1. Volume Group (All 3D bodies for gravity load)
volumes = gmsh.model.getEntities(dim=3)
gmsh.model.addPhysicalGroup(3, [v[1] for v in volumes], tag=1, name="SlabVolume")

# Find global Z bounds across the whole geometry
surfaces = gmsh.model.getEntities(dim=2)
all_zmin, all_zmax = [], []
for dim, tag in surfaces:
	bbox = gmsh.model.getBoundingBox(dim, tag)
	all_zmin.append(bbox[2])
	all_zmax.append(bbox[5])

z_bottom = min(all_zmin)
z_top = max(all_zmax)

feet_facets = []
top_facets = []

# 2. Automatically classify boundary surfaces by Z level
for dim, tag in surfaces:
	bbox = gmsh.model.getBoundingBox(dim, tag)
	# Check if face lies on the bottom plane (feet / supports)
	if np.isclose(bbox[2], z_bottom) and np.isclose(bbox[5], z_bottom):
		feet_facets.append(tag)
	# Check if face lies on the top plane (loaded surface)
	elif np.isclose(bbox[2], z_top) and np.isclose(bbox[5], z_top):
		top_facets.append(tag)

gmsh.model.addPhysicalGroup(2, feet_facets, tag=1, name="SupportFeet")
gmsh.model.addPhysicalGroup(2, top_facets, tag=2, name="LoadedSurface")

# 3. Generate 3D Mesh
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 5.0)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 20.0)
gmsh.model.mesh.generate(3)

# Save as version 4 .msh for DOLFINx
gmsh.write("mesh/beam.msh")
gmsh.finalize()
